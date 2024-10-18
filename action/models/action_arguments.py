from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PackageMetric(Enum):
    BINARY_RELEASE_RECENCY = "binary_release_recency"
    source_commit_frequency = "source_commit_frequency"
    source_commit_recency = "source_commit_recency"
    issues_lifetime = "source_issues_lifetime"
    issues_open_percentage = "issues_open_percentage"
    pull_requests_lifetime = "pull_requests_lifetime"
    pull_requests_open_percentage = "pull_requests_open_percentage"


class PackageMetricScore(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class ActionArguments(BaseModel):
    github_repository_owner: str
    github_repository_name: str
    github_token: Optional[str]
    packages_ignore: Optional[list[str]]
    packages_scores_thresholds: Optional[dict[PackageMetric, PackageMetricScore]]
