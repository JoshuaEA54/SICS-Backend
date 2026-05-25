from app.core.enums import ResponseVerdict
from app.models.evaluation import Response

_COMPLIES_VERDICTS = frozenset(
    {ResponseVerdict.complies, ResponseVerdict.complies_with_observations}
)

def response_is_compliant(response: Response) -> bool:
    if not response.answer:
        return False
    return response.verdict in _COMPLIES_VERDICTS


def calculate_compliance_percentage(responses: list[Response]) -> float:
    if not responses:
        return 0.0
    compliant = sum(1 for r in responses if response_is_compliant(r))
    return round(100 * compliant / len(responses), 1)


def calculate_review_progress(responses: list[Response]) -> tuple[int, int]:
    """Returns (completed, required) for controls where the company answered yes."""
    required = [r for r in responses if r.answer]
    completed = sum(1 for r in required if r.verdict is not None)
    return completed, len(required)


def has_pending_verdicts(responses: list[Response]) -> bool:
    return any(r.answer and r.verdict is None for r in responses)
