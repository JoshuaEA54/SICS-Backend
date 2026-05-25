import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from app import crud
from app.core.config import settings
from app.core.enums import ReportStatus
from app.db.session import SessionLocal
from app.models.user import User
from app.services.report.context import build_report_context
from app.services.report.pdf import html_to_pdf
from app.services.report.render import render_report_html

logger = logging.getLogger(__name__)


def generate_report_task(eval_id: uuid.UUID, expert_user_id: uuid.UUID) -> None:
    """Background task: render PDF and update report_status on the evaluation.

    Opens its own DB session so it can run independently of the request cycle.
    """
    db = SessionLocal()
    try:
        evaluation = crud.evaluation.get_evaluation(db, eval_id)
        expert = db.execute(select(User).where(User.id == expert_user_id)).scalar_one()

        context = build_report_context(db, evaluation, expert)
        html = render_report_html(context)

        output_dir = Path(settings.REPORTS_FOLDER)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{eval_id}.pdf"

        html_to_pdf(html, output_path)

        evaluation.report_status = ReportStatus.ready
        evaluation.report_path = str(output_path)
        evaluation.report_generated_at = datetime.now(timezone.utc)
        evaluation.report_error = None
        db.commit()

        logger.info("Report generated for evaluation %s → %s", eval_id, output_path)

    except Exception as exc:
        logger.exception("Failed to generate report for evaluation %s", eval_id)
        try:
            evaluation = crud.evaluation.get_evaluation(db, eval_id)
            evaluation.report_status = ReportStatus.failed
            evaluation.report_error = str(exc)[:500]
            db.commit()
        except Exception:
            logger.exception("Could not update report_status to failed for evaluation %s", eval_id)
    finally:
        db.close()
