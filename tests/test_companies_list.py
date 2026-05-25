from sqlalchemy.dialects import postgresql

from app.crud.company import get_companies_query


def _compile(stmt) -> str:
    return str(
        stmt.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


class TestGetCompaniesQuery:
    def test_q_filter_uses_ilike(self):
        sql = _compile(get_companies_query(q="acme"))
        assert "ilike" in sql.lower()
        assert "acme" in sql.lower()

    def test_no_q_omits_name_filter(self):
        sql = _compile(get_companies_query())
        assert "ilike" not in sql.lower()
