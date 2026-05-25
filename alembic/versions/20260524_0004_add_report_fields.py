"""add report fields to evaluations

Revision ID: 20260524_0004
Revises: 20260412_0003
Create Date: 2026-05-24 00:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260524_0004"
down_revision: str | None = "20260412_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "evaluations",
        sa.Column(
            "report_status",
            sa.String(20),
            nullable=True,
            comment="generating | ready | failed. Solo relevante cuando status = reviewed.",
        ),
    )
    op.add_column(
        "evaluations",
        sa.Column(
            "report_path",
            sa.Text(),
            nullable=True,
            comment="Ruta relativa en disco. Ej: data/reports/{uuid}.pdf",
        ),
    )
    op.add_column(
        "evaluations",
        sa.Column(
            "report_generated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="Momento en que el job terminó con éxito.",
        ),
    )
    op.add_column(
        "evaluations",
        sa.Column(
            "report_error",
            sa.Text(),
            nullable=True,
            comment="Mensaje breve si report_status = failed. No expuesto a la empresa.",
        ),
    )
    op.create_check_constraint(
        "ck_evaluations_report_status",
        "evaluations",
        "report_status IN ('generating', 'ready', 'failed')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_evaluations_report_status", "evaluations", type_="check")
    op.drop_column("evaluations", "report_error")
    op.drop_column("evaluations", "report_generated_at")
    op.drop_column("evaluations", "report_path")
    op.drop_column("evaluations", "report_status")
