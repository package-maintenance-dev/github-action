from enum import Enum
from typing import Optional, Annotated

from packageurl import PackageURL
from pydantic import BaseModel, SkipValidation


class PackageMetric(Enum):
    binary_release_recency = "binary_release_recency"
    source_commit_frequency = "source_commit_frequency"
    source_commit_recency = "source_commit_recency"
    issues_lifetime = "source_issues_lifetime"
    issues_open_percentage = "issues_open_percentage"
    pull_requests_lifetime = "pull_requests_lifetime"
    pull_requests_open_percentage = "pull_requests_open_percentage"


def default_packages_scores_thresholds():
    default_score_threshold = "B"
    return {
        PackageMetric.binary_release_recency: default_score_threshold,
        PackageMetric.source_commit_frequency: default_score_threshold,
        PackageMetric.source_commit_recency: default_score_threshold,
        PackageMetric.issues_lifetime: default_score_threshold,
        PackageMetric.issues_open_percentage: default_score_threshold,
        PackageMetric.pull_requests_lifetime: default_score_threshold,
        PackageMetric.pull_requests_open_percentage: default_score_threshold,
    }


class PackageMetricScore(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class ActionArguments(BaseModel):
    github_repository_owner: str
    github_repository_name: str
    github_token: Optional[str] = None
    packages_ignore: Annotated[list["PackageURL"], SkipValidation] = []
    packages_scores_thresholds: dict[PackageMetric, PackageMetricScore] = (
        default_packages_scores_thresholds()
    )
