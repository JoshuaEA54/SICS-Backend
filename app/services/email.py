from __future__ import annotations

import json
import logging
import shutil
import smtplib
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.enums import EvaluationStatus, ReportStatus
from app.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ServiceUnavailableError,
)
from app.models.evaluation import Evaluation
from app.models.user import User
from app.schemas.evaluation import ReportRecipientItem, SendReportResponse
from app.services import compliance
from app.services.report.constants import BAND_CONFIG, LOGO_PATH, get_band
from app.services.report.filename import build_report_download_filename

logger = logging.getLogger(__name__)

RENDER_SCRIPT = "scripts/render-report-email.mts"
RENDER_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class ReportRecipient:
    email: str
    label: str


def serialize_sent_to(emails: list[str]) -> str:
    return json.dumps(sorted(emails))


def deserialize_sent_to(raw: str | list[str] | None) -> list[str] | None:
    if raw is None:
        return None
    if isinstance(raw, list):
        return [str(item) for item in raw]
    if not raw.strip():
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, list):
        return None
    return [str(item) for item in parsed]


def resolve_report_recipients(db: Session, evaluation: Evaluation) -> list[ReportRecipient]:
    items: list[ReportRecipient] = []

    rep = crud.user.get_company_rep_by_company_id(db, evaluation.company_id)
    if rep and rep.email.strip():
        items.append(ReportRecipient(email=rep.email.strip(), label="Representante"))

    contacts = db.scalars(crud.company.get_contacts_query(evaluation.company_id)).all()
    for contact in contacts:
        email = contact.email.strip()
        if email:
            items.append(ReportRecipient(email=email, label=f"Contacto: {contact.name}"))

    seen: set[str] = set()
    unique: list[ReportRecipient] = []
    for item in items:
        key = item.email.lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return sorted(unique, key=lambda r: r.email.lower())


def build_report_email_props(
    db: Session,
    evaluation: Evaluation,
    expert: User,
) -> dict:
    company_name, _ = crud.company.get_company_display_labels(db, evaluation.company_id)
    responses = crud.evaluation.list_responses(db, evaluation.id)
    percentage = compliance.calculate_compliance_percentage(responses)
    band = get_band(percentage)
    band_cfg = BAND_CONFIG[band]

    reviewed_at = evaluation.reviewed_at
    reviewed_at_fmt = reviewed_at.strftime("%d/%m/%Y") if reviewed_at else "N/D"

    return {
        "companyName": company_name or "Empresa",
        "compliancePercentage": round(percentage, 1),
        "complianceLabel": band_cfg["label"],
        "complianceColor": band_cfg["color"],
        "expertName": expert.name,
        "reviewedAt": reviewed_at_fmt,
        "appUrl": f"{settings.FRONTEND_URL.rstrip('/')}/evaluaciones",
        "logoSrc": "cid:logo",
    }


def _frontend_dir() -> Path:
    frontend_dir = Path(settings.FRONTEND_DIR)
    if not frontend_dir.is_absolute():
        backend_dir = Path(__file__).resolve().parent.parent.parent
        frontend_dir = (backend_dir / frontend_dir).resolve()
    return frontend_dir


def _render_script_path() -> Path:
    return _frontend_dir() / RENDER_SCRIPT


def _resolve_npx() -> str:
    npx = shutil.which("npx")
    if not npx:
        raise ServiceUnavailableError("Node/npx no encontrado en PATH")
    return npx


def render_report_email_html(props: dict) -> str:
    script_path = _render_script_path()
    if not script_path.exists():
        raise ServiceUnavailableError(f"No se encontró el script de correo: {script_path}")

    npx = _resolve_npx()

    try:
        result = subprocess.run(
            [npx, "tsx", str(script_path)],
            input=json.dumps(props),
            capture_output=True,
            encoding="utf-8",
            timeout=RENDER_TIMEOUT_SECONDS,
            cwd=str(_frontend_dir()),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ServiceUnavailableError("Tiempo de espera agotado al renderizar el correo") from exc
    except OSError as exc:
        raise ServiceUnavailableError("No se pudo ejecutar Node para renderizar el correo") from exc

    if result.returncode != 0:
        logger.error("render-report-email failed: %s", result.stderr)
        raise ServiceUnavailableError("Error al renderizar la plantilla del correo")

    html = result.stdout.strip()
    if not html:
        raise ServiceUnavailableError("La plantilla del correo devolvió HTML vacío")
    return html


def send_report_email(
    *,
    recipients: list[str],
    subject: str,
    html_body: str,
    pdf_path: Path,
    attachment_filename: str,
) -> None:
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        raise ServiceUnavailableError("SMTP no configurado")

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    from_header = settings.SMTP_FROM or settings.SMTP_USER
    if "<" in from_header and ">" in from_header:
        msg["From"] = from_header
    else:
        msg["From"] = formataddr(("SICS", settings.SMTP_USER))
    msg["To"] = ", ".join(recipients)

    msg.attach(MIMEText(html_body, "html", "utf-8"))

    if LOGO_PATH.exists():
        with LOGO_PATH.open("rb") as logo_file:
            logo_part = MIMEImage(logo_file.read(), _subtype="png")
        logo_part.add_header("Content-ID", "<logo>")
        logo_part.add_header("Content-Disposition", "inline", filename="logo.png")
        msg.attach(logo_part)

    with pdf_path.open("rb") as pdf_file:
        pdf_part = MIMEApplication(pdf_file.read(), _subtype="pdf")
    pdf_part.add_header("Content-Disposition", "attachment", filename=attachment_filename)
    msg.attach(pdf_part)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            if settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, recipients, msg.as_string())
    except smtplib.SMTPException as exc:
        logger.exception("SMTP send failed")
        raise ServiceUnavailableError("No se pudo enviar el correo") from exc


def get_report_recipients_response(
    db: Session, evaluation: Evaluation
) -> list[ReportRecipientItem]:
    return [
        ReportRecipientItem(email=item.email, label=item.label)
        for item in resolve_report_recipients(db, evaluation)
    ]


def send_evaluation_report(
    db: Session,
    evaluation: Evaluation,
    expert: User,
) -> SendReportResponse:
    if evaluation.status != EvaluationStatus.reviewed:
        raise BadRequestError("La evaluación debe estar revisada")
    if evaluation.report_status != ReportStatus.ready:
        raise BadRequestError("El informe no está listo para enviar")
    if evaluation.report_email_sent_at is not None:
        raise ConflictError("El informe ya fue enviado por correo")
    if not evaluation.report_path:
        raise NotFoundError("El archivo de informe no se encontró en el servidor")

    pdf_path = Path(evaluation.report_path)
    if not pdf_path.exists():
        raise NotFoundError("El archivo de informe no se encontró en el servidor")

    recipient_items = resolve_report_recipients(db, evaluation)
    recipient_emails = [item.email for item in recipient_items]
    if not recipient_emails:
        raise BadRequestError("No hay destinatarios para enviar el informe")

    company_name, _ = crud.company.get_company_display_labels(db, evaluation.company_id)
    props = build_report_email_props(db, evaluation, expert)
    html = render_report_email_html(props)
    filename = build_report_download_filename(company_name or "empresa", evaluation.reviewed_at)
    subject = f"Informe SICS: {company_name or 'Empresa'}"

    send_report_email(
        recipients=recipient_emails,
        subject=subject,
        html_body=html,
        pdf_path=pdf_path,
        attachment_filename=filename,
    )

    sent_at = datetime.now(timezone.utc)
    crud.evaluation.mark_report_email_sent(
        db,
        evaluation.id,
        sent_at=sent_at,
        sent_to=recipient_emails,
    )

    return SendReportResponse(sent_at=sent_at, sent_to=recipient_emails)
