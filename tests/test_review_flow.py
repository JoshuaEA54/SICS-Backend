from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import uuid

import pytest

from app.core.enums import EvaluationStatus, ResponseVerdict
from app.core.exceptions import BadRequestError
from app.services import review as review_service


def _response(*, answer: bool, verdict: ResponseVerdict | None = None, response_id=None):
    return SimpleNamespace(
        id=response_id or uuid.uuid4(),
        answer=answer,
        verdict=verdict,
        reviewed_at=None,
    )


def _evaluation(*, status=EvaluationStatus.submitted):
    return SimpleNamespace(
        id=uuid.uuid4(),
        status=status,
        reviewed_at=None,
        company_id=uuid.uuid4(),
    )


class TestUpdateResponseVerdict:
    @patch('app.services.review.get_response_for_expert_verdict')
    def test_rejects_verdict_when_company_said_no(self, mock_get):
        response = _response(answer=False)
        mock_get.return_value = (response, _evaluation())

        with pytest.raises(BadRequestError):
            review_service.update_response_verdict(
                MagicMock(),
                response.id,
                SimpleNamespace(verdict=ResponseVerdict.complies),
            )

    @patch('app.services.review.get_response_for_expert_verdict')
    def test_sets_verdict_when_company_said_yes(self, mock_get):
        db = MagicMock()
        response = _response(answer=True, verdict=None)
        mock_get.return_value = (response, _evaluation())

        review_service.update_response_verdict(
            db,
            response.id,
            SimpleNamespace(verdict=ResponseVerdict.complies_with_observations),
        )

        assert response.verdict == ResponseVerdict.complies_with_observations
        assert response.reviewed_at is not None
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(response)


class TestFinalizeReview:
    @patch('app.services.review.list_responses')
    @patch('app.services.review.get_evaluation_for_expert_finalize')
    def test_finalize_fails_with_pending_verdicts(self, mock_get_eval, mock_list):
        evaluation = _evaluation()
        mock_get_eval.return_value = evaluation
        mock_list.return_value = [
            _response(answer=True, verdict=ResponseVerdict.complies),
            _response(answer=True, verdict=None),
        ]

        with pytest.raises(BadRequestError):
            review_service.finalize_review(MagicMock(), evaluation.id)

    @patch('app.services.review.list_responses')
    @patch('app.services.review.get_evaluation_for_expert_finalize')
    def test_finalize_succeeds_when_all_verdicts_present(self, mock_get_eval, mock_list):
        db = MagicMock()
        evaluation = _evaluation()
        mock_get_eval.return_value = evaluation
        mock_list.return_value = [
            _response(answer=True, verdict=ResponseVerdict.complies),
            _response(answer=False),
        ]

        result = review_service.finalize_review(db, evaluation.id)

        assert result.status == EvaluationStatus.reviewed
        assert result.reviewed_at is not None
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(evaluation)
