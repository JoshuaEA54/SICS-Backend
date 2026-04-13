"""create initial schema

Revision ID: 20260329_0001
Revises:
Create Date: 2026-03-29 00:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from app.core.enums import ControlCriticality, EvaluationStatus, ResponseVerdict, UserRole

# revision identifiers, used by Alembic.
revision: str = "20260329_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── Geografía ────────────────────────────────────────────────

    op.create_table(
        "provinces",
        sa.Column("id", sa.SmallInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(60), nullable=False),
        sa.UniqueConstraint("name", name="uq_provinces_name"),
    )

    op.create_table(
        "cantons",
        sa.Column("id", sa.SmallInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("province_id", sa.SmallInteger(), sa.ForeignKey("provinces.id"), nullable=False),
        sa.UniqueConstraint("name", "province_id", name="uq_cantons_name_province"),
    )

    op.create_table(
        "districts",
        sa.Column("id", sa.SmallInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("canton_id", sa.SmallInteger(), sa.ForeignKey("cantons.id"), nullable=False),
        sa.UniqueConstraint("name", "canton_id", name="uq_districts_name_canton"),
    )

    # ── Catálogos de empresa ─────────────────────────────────────

    op.create_table(
        "sectors",
        sa.Column("id", sa.SmallInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.UniqueConstraint("name", name="uq_sectors_name"),
    )

    op.create_table(
        "employee_ranges",
        sa.Column("id", sa.SmallInteger(), primary_key=True, autoincrement=True),
        sa.Column("label", sa.String(20), nullable=False),
        sa.UniqueConstraint("label", name="uq_employee_ranges_label"),
    )

    # ── Empresas ─────────────────────────────────────────────────

    op.create_table(
        "companies",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("sector_id", sa.SmallInteger(), sa.ForeignKey("sectors.id"), nullable=False),
        sa.Column("employee_range_id", sa.SmallInteger(), sa.ForeignKey("employee_ranges.id"), nullable=False),
        sa.Column("district_id", sa.SmallInteger(), sa.ForeignKey("districts.id"), nullable=False),
        sa.Column("branch_count", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("name", name="uq_companies_name"),
    )

    # ── Usuarios ─────────────────────────────────────────────────

    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(200), nullable=False),
        sa.Column("job_title", sa.String(150), nullable=True),
        sa.Column("role", sa.Enum(UserRole, native_enum=False, create_constraint=True, name="ck_users_role"), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("company_id", name="uq_users_company_id"),
    )

    # ── Contactos ────────────────────────────────────────────────

    op.create_table(
        "contacts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(200), nullable=False),
        sa.Column("job_title", sa.String(150), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    # ── Catálogo de controles ────────────────────────────────────

    op.create_table(
        "control_groups",
        sa.Column("id", sa.String(10), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("criticality", sa.Enum(ControlCriticality, native_enum=False, create_constraint=True, name="ck_control_groups_criticality"), nullable=True),
    )

    op.create_table(
        "controls",
        sa.Column("id", sa.String(20), primary_key=True),
        sa.Column("group_id", sa.String(10), sa.ForeignKey("control_groups.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "standards",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(20), nullable=False),
        sa.UniqueConstraint("name", name="uq_standards_name"),
    )

    op.create_table(
        "control_standard_refs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("control_id", sa.String(20), sa.ForeignKey("controls.id"), nullable=False),
        sa.Column("standard_id", sa.Integer(), sa.ForeignKey("standards.id"), nullable=False),
        sa.Column("ref_code", sa.String(100), nullable=False),
        sa.UniqueConstraint("control_id", "standard_id", "ref_code", name="uq_control_standard_ref"),
    )

    # ── Evaluaciones ─────────────────────────────────────────────

    op.create_table(
        "evaluations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("status", sa.Enum(EvaluationStatus, native_enum=False, create_constraint=True, name="ck_evaluations_status"), nullable=False, server_default=sa.text("'draft'")),
        sa.Column("last_group_id", sa.String(10), sa.ForeignKey("control_groups.id"), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    # ── Respuestas ───────────────────────────────────────────────

    op.create_table(
        "responses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("evaluations.id"), nullable=False),
        sa.Column("control_id", sa.String(20), sa.ForeignKey("controls.id"), nullable=False),
        sa.Column("answer", sa.Boolean(), nullable=False),
        sa.Column("observations", sa.Text(), nullable=True),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("verdict", sa.Enum(ResponseVerdict, native_enum=False, create_constraint=True, name="ck_responses_verdict"), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("evaluation_id", "control_id", name="uq_responses_evaluation_control"),
    )

    # ── Evidencia ────────────────────────────────────────────────

    op.create_table(
        "evidence",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("response_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("responses.id"), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("file_name", sa.String(300), nullable=False),
        sa.Column("file_type", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("evidence")
    op.drop_table("responses")
    op.drop_table("evaluations")
    op.drop_table("control_standard_refs")
    op.drop_table("standards")
    op.drop_table("controls")
    op.drop_table("control_groups")
    op.drop_table("contacts")
    op.drop_table("users")
    op.drop_table("companies")
    op.drop_table("employee_ranges")
    op.drop_table("sectors")
    op.drop_table("districts")
    op.drop_table("cantons")
    op.drop_table("provinces")
