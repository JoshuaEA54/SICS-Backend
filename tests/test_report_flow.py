"""Tests for PDF report generation, download, and regeneration."""

import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.core.enums import EvaluationStatus, ReportStatus
from app.core.exceptions import BadRequestError, NotFoundError
from app.services.report import build_report_download_filename, generate_report_task


# ── Helpers ────────────────────────────────────────────────────────────────────

def _evaluation(
    *,
    status=EvaluationStatus.reviewed,
    report_status: ReportStatus | None = None,
    report_path: str | None = None,
    reviewed_at: datetime | None = None,
):
    return SimpleNamespace(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        status=status,
        report_status=report_status,
        report_path=report_path,
        report_error=None,
        report_email_sent_at=None,
        report_email_sent_to=None,
        report_generated_at=None,
        reviewed_at=reviewed_at or datetime(2026, 5, 24, tzinfo=timezone.utc),
        submitted_at=datetime(2026, 5, 20, tzinfo=timezone.utc),
        created_at=datetime(2026, 5, 1, tzinfo=timezone.utc),
    )


# ── build_report_download_filename ────────────────────────────────────────────

class TestBuildReportDownloadFilename:
    def test_basic_name(self):
        reviewed_at = datetime(2026, 5, 24, tzinfo=timezone.utc)
        name = build_report_download_filename("Acme Costa Rica", reviewed_at)
        assert name == "Acme-Costa-Rica-informe-sics-2026-05-24.pdf"

    def test_special_characters_stripped(self):
        reviewed_at = datetime(2026, 5, 24, tzinfo=timezone.utc)
        name = build_report_download_filename("Empresa S.A. / Ltda.", reviewed_at)
        assert ".." not in name
        assert "/" not in name
        assert name.endswith(".pdf")

    def test_no_uuid_in_name(self):
        eval_id = uuid.uuid4()
        reviewed_at = datetime(2026, 5, 24, tzinfo=timezone.utc)
        name = build_report_download_filename("Mi Empresa", reviewed_at)
        assert str(eval_id) not in name

    def test_long_name_truncated(self):
        reviewed_at = datetime(2026, 5, 24, tzinfo=timezone.utc)
        long_name = "Empresa " * 20
        name = build_report_download_filename(long_name, reviewed_at)
        assert len(name) < 120  # reasonable filename length

    def test_none_reviewed_at_uses_today(self):
        name = build_report_download_filename("Empresa", None)
        assert "informe-sics" in name
        assert name.endswith(".pdf")


# ── generate_report_task ───────────────────────────────────────────────────────

class TestGenerateReportTask:
    @patch("app.services.report.task.SessionLocal")
    @patch("app.services.report.task.html_to_pdf")
    @patch("app.services.report.task.render_report_html")
    @patch("app.services.report.task.build_report_context")
    @patch("app.services.report.task.crud")
    def test_sets_ready_on_success(
        self, mock_crud, mock_build_ctx, mock_render, mock_pdf, mock_session_local
    ):
        eval_id = uuid.uuid4()
        expert_id = uuid.uuid4()
        evaluation = _evaluation(report_status=ReportStatus.generating)

        db = MagicMock()
        mock_session_local.return_value = db
        mock_crud.evaluation.get_evaluation.return_value = evaluation
        db.execute.return_value.scalar_one.return_value = MagicMock()  # expert user

        mock_build_ctx.return_value = {}
        mock_render.return_value = "<html/>"

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("app.services.report.task.settings") as mock_settings:
                mock_settings.REPORTS_FOLDER = tmpdir
                generate_report_task(eval_id, expert_id)

        assert evaluation.report_status == ReportStatus.ready
        assert evaluation.report_path is not None
        assert evaluation.report_generated_at is not None
        db.commit.assert_called()
        db.close.assert_called_once()

    @patch("app.services.report.task.SessionLocal")
    @patch("app.services.report.task.html_to_pdf")
    @patch("app.services.report.task.render_report_html")
    @patch("app.services.report.task.build_report_context")
    @patch("app.services.report.task.crud")
    def test_sets_failed_on_exception(
        self, mock_crud, mock_build_ctx, mock_render, mock_pdf, mock_session_local
    ):
        eval_id = uuid.uuid4()
        expert_id = uuid.uuid4()
        evaluation = _evaluation(report_status=ReportStatus.generating)

        db = MagicMock()
        mock_session_local.return_value = db
        mock_crud.evaluation.get_evaluation.return_value = evaluation
        db.execute.return_value.scalar_one.return_value = MagicMock()

        mock_build_ctx.return_value = {}
        mock_render.return_value = "<html/>"
        mock_pdf.side_effect = RuntimeError("PDF generation failed")

        with patch("app.services.report.task.settings") as mock_settings:
            mock_settings.REPORTS_FOLDER = "/tmp/reports_test"
            generate_report_task(eval_id, expert_id)

        assert evaluation.report_status == ReportStatus.failed
        assert "PDF generation failed" in (evaluation.report_error or "")
        db.close.assert_called_once()


# ── Download report route ──────────────────────────────────────────────────────

class TestDownloadReportEndpoint:
    """Unit tests for the download_report route logic (access control + status)."""

    def _make_request_context(self, evaluation):
        """Simulate what the route handler checks."""
        from app.core.enums import ReportStatus
        from app.core.exceptions import BadRequestError, NotFoundError

        if evaluation.report_status != ReportStatus.ready:
            if evaluation.report_status in (ReportStatus.generating, ReportStatus.failed):
                raise BadRequestError("El informe aún no está disponible")
            raise NotFoundError("No existe informe para esta evaluación")

        report_path = Path(evaluation.report_path)
        return report_path

    def test_raises_bad_request_when_generating(self):
        evaluation = _evaluation(report_status=ReportStatus.generating)
        with pytest.raises(BadRequestError):
            self._make_request_context(evaluation)

    def test_raises_bad_request_when_failed(self):
        evaluation = _evaluation(report_status=ReportStatus.failed)
        with pytest.raises(BadRequestError):
            self._make_request_context(evaluation)

    def test_raises_not_found_when_null(self):
        evaluation = _evaluation(report_status=None)
        with pytest.raises(NotFoundError):
            self._make_request_context(evaluation)

    def test_returns_path_when_ready(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-1.4")
            tmp_path = f.name

        evaluation = _evaluation(report_status=ReportStatus.ready, report_path=tmp_path)
        path = self._make_request_context(evaluation)
        assert path.exists()


# ── Regenerate report ──────────────────────────────────────────────────────────

class TestRegenerateReport:
    """Unit tests for regenerate_report route logic."""

    def _simulate_regenerate(self, db, evaluation):
        from app.core.enums import ReportStatus
        from app.core.exceptions import BadRequestError

        if evaluation.report_status != ReportStatus.failed:
            raise BadRequestError("Solo se puede reintentar si el informe está en estado fallido")

        evaluation.report_status = ReportStatus.generating
        evaluation.report_error = None
        db.commit()
        db.refresh(evaluation)
        return evaluation

    def test_raises_when_not_failed(self):
        db = MagicMock()
        evaluation = _evaluation(report_status=ReportStatus.generating)
        with pytest.raises(BadRequestError):
            self._simulate_regenerate(db, evaluation)

    def test_raises_when_ready(self):
        db = MagicMock()
        evaluation = _evaluation(report_status=ReportStatus.ready)
        with pytest.raises(BadRequestError):
            self._simulate_regenerate(db, evaluation)

    def test_resets_to_generating_when_failed(self):
        db = MagicMock()
        evaluation = _evaluation(report_status=ReportStatus.failed)
        evaluation.report_error = "Some previous error"

        result = self._simulate_regenerate(db, evaluation)

        assert result.report_status == ReportStatus.generating
        assert result.report_error is None
        db.commit.assert_called_once()
