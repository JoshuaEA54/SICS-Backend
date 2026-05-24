from sqlalchemy.dialects import postgresql

from app.core.enums import EvaluationStatus
from app.crud import evaluation as evaluation_crud
from app.crud.evaluation import get_evaluations_query


def _compile(stmt) -> str:
    return str(
        stmt.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


class TestGetEvaluationsQuery:
    def test_exclude_draft_adds_filter(self):
        sql = _compile(get_evaluations_query(exclude_draft=True))
        assert "draft" in sql.lower()

    def test_expert_requesting_draft_status_yields_empty(self):
        sql = _compile(
            get_evaluations_query(
                status=EvaluationStatus.draft,
                exclude_draft=True,
            )
        )
        assert "false" in sql.lower() or "1 = 0" in sql.lower() or "0 = 1" in sql.lower()

    def test_sector_id_filter(self):
        sql = _compile(get_evaluations_query(sector_id=3))
        assert "sector_id" in sql.lower()
        assert "companies" in sql.lower()

    def test_default_order_uses_status_priority(self):
        sql = _compile(get_evaluations_query())
        assert "CASE" in sql.upper()


class TestGetEvaluationStatusCounts:
    def test_counts_submitted_and_reviewed(self):
        from unittest.mock import MagicMock

        db = MagicMock()
        db.scalar.side_effect = [12, 8]
        counts = evaluation_crud.get_evaluation_status_counts(db, exclude_draft=True)
        assert counts == {"pending": 12, "reviewed": 8}
        assert db.scalar.call_count == 2
