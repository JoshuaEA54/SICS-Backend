from enum import Enum


class UserRole(str, Enum):
    company_rep = "company_rep"
    expert = "expert"


class AuthFlow(str, Enum):
    expert = "expert"
    existing_company = "existing_company"
    new_company = "new_company"


class EvaluationStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    reviewed = "reviewed"


class ResponseVerdict(str, Enum):
    complies = "complies"
    complies_with_observations = "complies_with_observations"
    does_not_comply = "does_not_comply"


class ControlCriticality(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
