"""Tests for expert_observations on response verdict updates."""

import uuid
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from app.core.enums import EvaluationStatus, ResponseVerdict
from app.core.exceptions import BadRequestError
from app.schemas.evaluation import ResponseVerdictUpdate
from app.services import compliance, review as review_service


def _response(
    *,
    answer: bool,
    verdict: ResponseVerdict | None = None,
    expert_observations: str | None = None,
    response_id=None,
):
    return SimpleNamespace(
        id=response_id or uuid.uuid4(),
        answer=answer,
        verdict=verdict,
        expert_observations=expert_observations,
        reviewed_at=None,
    )


def _evaluation(*, status=EvaluationStatus.submitted):
    return SimpleNamespace(
        id=uuid.uuid4(),
        status=status,
        reviewed_at=None,
        report_status=None,
        report_error=None,
        company_id=uuid.uuid4(),
    )


class TestResponseVerdictUpdateSchema:
    def test_complies_with_observations_requires_text(self):
        with pytest.raises(ValidationError):
            ResponseVerdictUpdate(
                verdict=ResponseVerdict.complies_with_observations,
                expert_observations=None,
            )

    def test_complies_with_observations_rejects_blank(self):
        with pytest.raises(ValidationError):
            ResponseVerdictUpdate(
                verdict=ResponseVerdict.complies_with_observations,
                expert_observations="   ",
            )

    def test_complies_with_observations_accepts_text(self):
        data = ResponseVerdictUpdate(
            verdict=ResponseVerdict.complies_with_observations,
            expert_observations="Falta documentación firmada.",
        )
        assert data.expert_observations == "Falta documentación firmada."

    def test_complies_rejects_expert_observations(self):
        with pytest.raises(ValidationError):
            ResponseVerdictUpdate(
                verdict=ResponseVerdict.complies,
                expert_observations="texto no permitido",
            )

    def test_complies_accepts_without_observations(self):
        data = ResponseVerdictUpdate(verdict=ResponseVerdict.complies)
        assert data.expert_observations is None


class TestUpdateResponseVerdictWithObservations:
    @patch("app.services.review.get_response_for_expert_verdict")
    def test_persists_expert_observations(self, mock_get):
        db = MagicMock()
        response = _response(answer=True, verdict=None)
        mock_get.return_value = (response, _evaluation())
        data = ResponseVerdictUpdate(
            verdict=ResponseVerdict.does_not_comply,
            expert_observations="Evidencia insuficiente.",
        )

        review_service.update_response_verdict(db, response.id, data)

        assert response.verdict == ResponseVerdict.does_not_comply
        assert response.expert_observations == "Evidencia insuficiente."
        db.commit.assert_called_once()

    @patch("app.services.review.get_response_for_expert_verdict")
    def test_complies_clears_expert_observations_on_response(self, mock_get):
        db = MagicMock()
        response = _response(
            answer=True,
            verdict=ResponseVerdict.complies_with_observations,
            expert_observations="Observación previa.",
        )
        mock_get.return_value = (response, _evaluation())
        data = ResponseVerdictUpdate(verdict=ResponseVerdict.complies)

        review_service.update_response_verdict(db, response.id, data)

        assert response.verdict == ResponseVerdict.complies
        assert response.expert_observations is None


class TestFinalizeReviewWithObservations:
    @patch("app.services.review.list_responses")
    @patch("app.services.review.get_evaluation_for_expert_finalize")
    def test_finalize_fails_when_observations_missing(self, mock_get_eval, mock_list):
        evaluation = _evaluation()
        mock_get_eval.return_value = evaluation
        mock_list.return_value = [
            _response(
                answer=True,
                verdict=ResponseVerdict.complies_with_observations,
                expert_observations=None,
            ),
        ]

        with pytest.raises(BadRequestError, match="observaciones del experto"):
            review_service.finalize_review(MagicMock(), evaluation.id)

    @patch("app.services.review.list_responses")
    @patch("app.services.review.get_evaluation_for_expert_finalize")
    def test_finalize_succeeds_when_observations_present(self, mock_get_eval, mock_list):
        db = MagicMock()
        evaluation = _evaluation()
        mock_get_eval.return_value = evaluation
        mock_list.return_value = [
            _response(
                answer=True,
                verdict=ResponseVerdict.does_not_comply,
                expert_observations="No cumple el control.",
            ),
            _response(answer=False),
        ]

        result = review_service.finalize_review(db, evaluation.id)

        assert result.status == EvaluationStatus.reviewed


class TestComplianceHelpers:
    def test_verdict_requires_expert_observations(self):
        assert compliance.verdict_requires_expert_observations(
            ResponseVerdict.complies_with_observations
        )
        assert compliance.verdict_requires_expert_observations(ResponseVerdict.does_not_comply)
        assert not compliance.verdict_requires_expert_observations(ResponseVerdict.complies)
        assert not compliance.verdict_requires_expert_observations(None)

    def test_has_missing_expert_observations(self):
        responses = [
            _response(
                answer=True,
                verdict=ResponseVerdict.complies_with_observations,
                expert_observations="  ",
            ),
            _response(
                answer=True,
                verdict=ResponseVerdict.complies,
                expert_observations=None,
            ),
        ]
        assert compliance.has_missing_expert_observations(responses)
