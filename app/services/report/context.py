from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import crud
from app.models.controls import Control, ControlGroup
from app.models.evaluation import Evaluation, Response
from app.models.user import User
from app.services.compliance import calculate_compliance_percentage, response_is_compliant
from app.services.report.constants import BAND_CONFIG, LOGO_PATH, get_band
from app.services.report.types import ControlRow, GroupData


def _fmt_dt(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return dt.strftime("%d/%m/%Y %H:%M")


def _fmt_date(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return dt.strftime("%d/%m/%Y")


def build_report_context(
    db: Session,
    evaluation: Evaluation,
    expert: User,
) -> dict:
    company = crud.company.get_company(db, evaluation.company_id)
    _, sector_name = crud.company.get_company_display_labels(db, evaluation.company_id)
    responses: list[Response] = crud.evaluation.list_responses(db, evaluation.id)

    response_map: dict[str, Response] = {r.control_id: r for r in responses}

    groups_orm = db.scalars(
        select(ControlGroup).order_by(ControlGroup.id)
    ).all()
    controls_orm = db.scalars(
        select(Control).order_by(Control.group_id, Control.id)
    ).all()

    controls_by_group: dict[str, list[Control]] = {}
    for control in controls_orm:
        controls_by_group.setdefault(control.group_id, []).append(control)

    groups: list[GroupData] = []
    for g in groups_orm:
        rows: list[ControlRow] = []
        for c in controls_by_group.get(g.id, []):
            resp = response_map.get(c.id)
            rows.append(ControlRow(
                control_id=c.id,
                control_name=c.name,
                answer=resp.answer if resp else False,
                verdict=resp.verdict.value if resp and resp.verdict else None,
                compliant=response_is_compliant(resp) if resp else False,
                observations=resp.observations if resp else None,
                expert_observations=resp.expert_observations if resp else None,
            ))
        if rows:
            groups.append(GroupData(
                id=g.id,
                name=g.name,
                criticality=g.criticality.value if g.criticality else None,
                rows=rows,
            ))

    percentage = calculate_compliance_percentage(responses)
    compliant_count = sum(1 for r in responses if response_is_compliant(r))
    band = get_band(percentage)
    band_cfg = BAND_CONFIG[band]

    return {
        "company": company,
        "sector_name": sector_name or "—",
        "expert": expert,
        "created_at_fmt": _fmt_date(evaluation.created_at),
        "submitted_at_fmt": _fmt_date(evaluation.submitted_at),
        "reviewed_at_fmt": _fmt_date(evaluation.reviewed_at),
        "generated_at_fmt": _fmt_dt(datetime.now(timezone.utc)),
        "compliance_pct_fmt": f"{percentage:.1f}",
        "compliance_band": band,
        "compliance_label": band_cfg["label"],
        "compliance_description": band_cfg["description"],
        "compliant_count": compliant_count,
        "total_controls": len(responses),
        "logo_path": str(LOGO_PATH.resolve()) if LOGO_PATH.is_file() else None,
        "groups": groups,
    }
