"""Tests for manual report email delivery."""

import json
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.core.enums import EvaluationStatus, ReportStatus, UserRole
from app.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ServiceUnavailableError,
)
from app.schemas.evaluation import ReportRecipientItem
from app.services import email as email_service
from app.services import review as review_service


def _evaluation(
    *,
    status=EvaluationStatus.reviewed,
    report_status=ReportStatus.ready,
    report_path: str | None = None,
    report_email_sent_at=None,
        report_email_sent_to=None,
        company_id=None,
        last_group_id=None,
    ):
    return SimpleNamespace(
        id=uuid.uuid4(),
        company_id=company_id or uuid.uuid4(),
        last_group_id=last_group_id,
        status=status,
        report_status=report_status,
        report_path=report_path,
        report_error=None,
        report_email_sent_at=report_email_sent_at,
        report_email_sent_to=report_email_sent_to,
        reviewed_at=datetime(2026, 5, 25, tzinfo=timezone.utc),
        submitted_at=datetime(2026, 5, 20, tzinfo=timezone.utc),
        created_at=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )


def _expert():
    return SimpleNamespace(id=uuid.uuid4(), name="Experta SICS", role=UserRole.expert)


class TestSerializeSentTo:
    def test_roundtrip(self):
        raw = email_service.serialize_sent_to(["b@x.com", "a@x.com"])
        assert email_service.deserialize_sent_to(raw) == ["a@x.com", "b@x.com"]

    def test_none_for_empty(self):
        assert email_service.deserialize_sent_to(None) is None

    def test_accepts_list(self):
        assert email_service.deserialize_sent_to(["b@x.com", "a@x.com"]) == [
            "b@x.com",
            "a@x.com",
        ]


class TestResolveReportRecipients:
    @patch("app.services.email.crud.user.get_company_rep_by_company_id")
    @patch("app.services.email.crud.company.get_contacts_query")
    def test_deduplicates_case_insensitive(self, mock_contacts_query, mock_rep):
        db = MagicMock()
        evaluation = _evaluation()
        mock_rep.return_value = SimpleNamespace(email="Rep@Empresa.com")
        contact = SimpleNamespace(name="Juan", email="rep@empresa.com")
        db.scalars.return_value.all.return_value = [contact]
        mock_contacts_query.return_value = MagicMock()

        recipients = email_service.resolve_report_recipients(db, evaluation)
        assert len(recipients) == 1
        assert recipients[0].email == "Rep@Empresa.com"


class TestSendEvaluationReport:
    @patch("app.services.email.crud.evaluation.mark_report_email_sent")
    @patch("app.services.email.send_report_email")
    @patch("app.services.email.render_report_email_html", return_value="<html/>")
    @patch("app.services.email.build_report_email_props", return_value={})
    @patch("app.services.email.resolve_report_recipients")
    @patch("app.services.email.crud.company.get_company_display_labels", return_value=("Acme", "Tech"))
    def test_success_persists_sent_fields(
        self,
        _labels,
        mock_recipients,
        _props,
        _render,
        _send,
        mock_mark,
    ):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(b"%PDF-1.4")
            pdf_path = tmp.name

        db = MagicMock()
        evaluation = _evaluation(report_path=pdf_path)
        expert = _expert()
        mock_recipients.return_value = [
            email_service.ReportRecipient(email="a@empresa.com", label="Representante")
        ]

        result = email_service.send_evaluation_report(db, evaluation, expert)

        assert result.sent_to == ["a@empresa.com"]
        mock_mark.assert_called_once()
        Path(pdf_path).unlink(missing_ok=True)

    def test_409_when_already_sent(self):
        db = MagicMock()
        evaluation = _evaluation(
            report_email_sent_at=datetime.now(timezone.utc),
            report_path="x.pdf",
        )
        with pytest.raises(ConflictError):
            email_service.send_evaluation_report(db, evaluation, _expert())

    def test_400_when_not_ready(self):
        evaluation = _evaluation(report_status=ReportStatus.generating)
        with pytest.raises(BadRequestError):
            email_service.send_evaluation_report(MagicMock(), evaluation, _expert())

    def test_404_when_pdf_missing_on_disk(self):
        evaluation = _evaluation(report_path="missing/file.pdf")
        with pytest.raises(NotFoundError):
            email_service.send_evaluation_report(MagicMock(), evaluation, _expert())

    @patch("app.services.email.resolve_report_recipients", return_value=[])
    def test_400_without_recipients(self, _recipients):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(b"%PDF")
            pdf_path = tmp.name
        evaluation = _evaluation(report_path=pdf_path)
        with pytest.raises(BadRequestError):
            email_service.send_evaluation_report(MagicMock(), evaluation, _expert())
        Path(pdf_path).unlink(missing_ok=True)

    @patch("app.services.email.send_report_email", side_effect=ServiceUnavailableError("smtp"))
    @patch("app.services.email.render_report_email_html", return_value="<html/>")
    @patch("app.services.email.build_report_email_props", return_value={})
    @patch("app.services.email.resolve_report_recipients")
    @patch("app.services.email.crud.company.get_company_display_labels", return_value=("Acme", None))
    def test_502_on_smtp_failure(self, _labels, mock_recipients, _props, _render, _send):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(b"%PDF")
            pdf_path = tmp.name
        evaluation = _evaluation(report_path=pdf_path)
        mock_recipients.return_value = [
            email_service.ReportRecipient(email="a@x.com", label="Representante")
        ]
        with pytest.raises(ServiceUnavailableError):
            email_service.send_evaluation_report(MagicMock(), evaluation, _expert())
        Path(pdf_path).unlink(missing_ok=True)


class TestEnrichVisibility:
    @patch("app.services.review.list_responses", return_value=[])
    @patch("app.services.review.crud.company.get_company_display_labels", return_value=("Acme", "Tech"))
    def test_company_rep_hides_sent_to(self, _labels, _responses):
        db = MagicMock()
        evaluation = _evaluation()
        evaluation.report_email_sent_to = json.dumps(["a@x.com", "b@x.com"])
        evaluation.report_email_sent_at = datetime.now(timezone.utc)
        company_user = SimpleNamespace(role=UserRole.company_rep)

        result = review_service.enrich_evaluation_read(db, evaluation, current_user=company_user)

        assert result.report_email_sent_at is not None
        assert result.report_email_sent_to is None

    @patch("app.services.review.list_responses", return_value=[])
    @patch("app.services.review.crud.company.get_company_display_labels", return_value=("Acme", "Tech"))
    def test_expert_sees_sent_to(self, _labels, _responses):
        db = MagicMock()
        evaluation = _evaluation()
        evaluation.report_email_sent_to = json.dumps(["a@x.com"])
        expert_user = SimpleNamespace(role=UserRole.expert)

        result = review_service.enrich_evaluation_read(db, evaluation, current_user=expert_user)

        assert result.report_email_sent_to == ["a@x.com"]


class TestGetReportRecipientsResponse:
    @patch("app.services.email.resolve_report_recipients")
    def test_maps_labels(self, mock_resolve):
        mock_resolve.return_value = [
            email_service.ReportRecipient(email="a@x.com", label="Representante")
        ]
        items = email_service.get_report_recipients_response(MagicMock(), _evaluation())
        assert items == [ReportRecipientItem(email="a@x.com", label="Representante")]
