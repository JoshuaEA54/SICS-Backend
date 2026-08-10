"""make control_groups.criticality not null with default low

Revision ID: 20260809_0007
Revises: 20260526_0006
Create Date: 2026-08-09 00:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from app.core.enums import ControlCriticality

revision: str = "20260809_0007"
down_revision: str | None = "20260526_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("UPDATE control_groups SET criticality = 'low' WHERE criticality IS NULL")
    op.alter_column(
        "control_groups",
        "criticality",
        existing_type=sa.Enum(
            ControlCriticality, native_enum=False, create_constraint=True, name="ck_control_groups_criticality"
        ),
        nullable=False,
        server_default="low",
    )


def downgrade() -> None:
    op.alter_column(
        "control_groups",
        "criticality",
        existing_type=sa.Enum(
            ControlCriticality, native_enum=False, create_constraint=True, name="ck_control_groups_criticality"
        ),
        nullable=True,
        server_default=None,
    )
