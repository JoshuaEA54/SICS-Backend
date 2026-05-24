from types import SimpleNamespace

from app.core.enums import ResponseVerdict
from app.services import compliance


def _response(*, answer: bool, verdict: ResponseVerdict | None = None):
    return SimpleNamespace(answer=answer, verdict=verdict)


class TestResponseIsCompliant:
    def test_no_when_company_said_no(self):
        assert compliance.response_is_compliant(_response(answer=False)) is False

    def test_no_when_yes_without_verdict(self):
        assert compliance.response_is_compliant(_response(answer=True, verdict=None)) is False

    def test_yes_when_complies(self):
        assert compliance.response_is_compliant(_response(answer=True, verdict=ResponseVerdict.complies)) is True

    def test_yes_when_complies_with_observations(self):
        assert compliance.response_is_compliant(
            _response(answer=True, verdict=ResponseVerdict.complies_with_observations)
        ) is True

    def test_no_when_expert_rejects(self):
        assert compliance.response_is_compliant(
            _response(answer=True, verdict=ResponseVerdict.does_not_comply)
        ) is False


class TestCalculateCompliancePercentage:
    def test_all_comply(self):
        responses = [_response(answer=True, verdict=ResponseVerdict.complies) for _ in range(30)]
        assert compliance.calculate_compliance_percentage(responses) == 100.0

    def test_all_no_without_verdicts(self):
        responses = [_response(answer=False) for _ in range(30)]
        assert compliance.calculate_compliance_percentage(responses) == 0.0

    def test_half_and_half(self):
        yes = [_response(answer=True, verdict=ResponseVerdict.complies) for _ in range(15)]
        no = [_response(answer=False) for _ in range(15)]
        assert compliance.calculate_compliance_percentage(yes + no) == 50.0

    def test_empty_responses(self):
        assert compliance.calculate_compliance_percentage([]) == 0.0


class TestReviewProgress:
    def test_progress_counts_only_yes_answers(self):
        responses = [
            _response(answer=True, verdict=ResponseVerdict.complies),
            _response(answer=True, verdict=None),
            _response(answer=False),
        ]
        completed, required = compliance.calculate_review_progress(responses)
        assert required == 2
        assert completed == 1

    def test_has_pending_verdicts(self):
        responses = [_response(answer=True, verdict=None)]
        assert compliance.has_pending_verdicts(responses) is True

    def test_no_pending_when_all_no(self):
        responses = [_response(answer=False) for _ in range(5)]
        assert compliance.has_pending_verdicts(responses) is False
