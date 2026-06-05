"""One-off script: render evaluation_report.html to PDF for a given evaluation."""

import sys
import uuid
from pathlib import Path

from sqlalchemy import select

from app import crud
from app.core.config import settings
from app.core.enums import UserRole
from app.db.session import SessionLocal
from app.models.user import User
from app.services.report.context import build_report_context
from app.services.report.pdf import html_to_pdf
from app.services.report.render import render_report_html

DEFAULT_EVAL_ID = "4ea65b84-2b59-41c0-b6ae-67535f4e8632"


def main() -> None:
    eval_id = uuid.UUID(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EVAL_ID)

    db = SessionLocal()
    try:
        evaluation = crud.evaluation.get_evaluation(db, eval_id)
        expert = db.execute(
            select(User).where(User.role == UserRole.expert).limit(1)
        ).scalar_one_or_none()
        if expert is None:
            raise SystemExit("No hay usuario experto en la base de datos")

        context = build_report_context(db, evaluation, expert)
        html = render_report_html(context)

        out_dir = Path(settings.REPORTS_FOLDER)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{eval_id}.pdf"
        html_to_pdf(html, out_path)

        print(f"PDF generado: {out_path.resolve()}")
        print(f"Tamaño: {out_path.stat().st_size:,} bytes")
        print(f"Empresa: {context['company'].name}")
        print(f"Cumplimiento: {context['compliance_pct_fmt']}%")
    finally:
        db.close()


if __name__ == "__main__":
    main()
