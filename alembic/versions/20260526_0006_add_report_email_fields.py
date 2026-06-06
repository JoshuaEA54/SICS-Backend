"""add report email fields to evaluations

Revision ID: 20260526_0006
Revises: 20260525_0005
Create Date: 2026-05-26 00:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260526_0006"
down_revision: str | None = "20260525_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "evaluations",
        sa.Column(
            "report_email_sent_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="Último envío manual del informe PDF por correo.",
        ),
    )
    op.add_column(
        "evaluations",
        sa.Column(
            "report_email_sent_to",
            sa.Text(),
            nullable=True,
            comment="JSON array de emails del último envío manual del informe.",
        ),
    )


def downgrade() -> None:
    op.drop_column("evaluations", "report_email_sent_to")
    op.drop_column("evaluations", "report_email_sent_at")
