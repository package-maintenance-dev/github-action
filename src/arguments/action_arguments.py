from enum import Enum
from typing import Optional, Annotated

from packageurl import PackageURL
from pydantic import BaseModel, SkipValidation  # type: ignore[attr-defined]

DEFAULT_SCORE_THRESHOLD = "B"


class MaintenanceMetricSlug(Enum):
    binary_release_recency = "binary_release_recency"
    source_commit_frequency = "source_commit_frequency"
    source_commit_recency = "source_commit_recency"
    issues_lifetime = "source_issues_lifetime"
    issues_open_percentage = "issues_open_percentage"
    pull_requests_lifetime = "pull_requests_lifetime"
    pull_requests_open_percentage = "pull_requests_open_percentage"


def default_packages_scores_thresholds():
    return {
        MaintenanceMetricSlug.binary_release_recency: DEFAULT_SCORE_THRESHOLD,
        MaintenanceMetricSlug.source_commit_frequency: DEFAULT_SCORE_THRESHOLD,
        MaintenanceMetricSlug.source_commit_recency: DEFAULT_SCORE_THRESHOLD,
    }


class MaintenanceMetricScore(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class ActionArguments(BaseModel):
    github_repository_owner: str
    github_repository_name: str
    github_token: Optional[str] = None
    packages_ignore: Annotated[list["PackageURL"], SkipValidation] = []
    packages_scores_thresholds: dict[MaintenanceMetricSlug, MaintenanceMetricScore] = (
        default_packages_scores_thresholds()
    )
