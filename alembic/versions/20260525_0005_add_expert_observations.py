"""add expert_observations to responses

Revision ID: 20260525_0005
Revises: 20260524_0004
Create Date: 2026-05-25 00:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260525_0005"
down_revision: str | None = "20260524_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "responses",
        sa.Column(
            "expert_observations",
            sa.Text(),
            nullable=True,
            comment="Observaciones del experto. Obligatoria si verdict ∈ {complies_with_observations, does_not_comply}.",
        ),
    )


def downgrade() -> None:
    op.drop_column("responses", "expert_observations")
