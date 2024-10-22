from typing import List, Optional

from pydantic import BaseModel


class MaintenanceMetric(BaseModel):
    """
    Represents an abstract metric that quantifies the maintenance activity
    of a package or repository. It includes both an absolute value
    (e.g., number of releases or commits) and a relative score (e.g., A, B, C, D).

    Attributes:
        value (int): Recency value of the release. Example: 10.
        score (str): Maintenance score of the repository. Example: 'A'.
    """

    value: int
    score: str


class BinaryRepository(BaseModel):
    """
    Represents metadata and maintenance metrics for a package published
    in a binary repository, including its versioning, repository URLs, and recency scoring.

    Attributes:
        id (str): Unique identifier for the package. Example: 'example-package-id'.
        type (str): Type of the binary repository. Example: 'maven'.
        latest_version (str): Latest version of the package. Example: '1.0.0'.
        latest_version_published_at (str): Publish date time of a package in ISO-8601 format.
            Example: '2021-11-03T00:00:00Z'.
        name (Optional[str]): Name of the package. Example: 'example-package'.
        description (Optional[str]): Description of the package. Example: 'A sample package'.
        url (str): URL to the binary repository. Example: 'https://repo.example.com/package'.
        source_repository_original_url (Optional[str]): Original source repository URL.
            Example: 'https://github.com/example/repo'.
        source_repository_normal_url (Optional[str]): Normalized source repository URL.
        source_repository_id (Optional[str]): ID of the source repository.
        source_repository_type (Optional[str]): Type of the source repository.
        release_recency (MaintenanceMetric): Metric representing the recency of the latest release.
    """

    id: str
    type: str
    latest_version: str
    latest_version_published_at: str
    name: Optional[str]
    description: Optional[str]
    url: str
    source_repository_original_url: Optional[str]
    source_repository_normal_url: Optional[str]
    source_repository_id: Optional[str]
    source_repository_type: Optional[str]
    release_recency: MaintenanceMetric


class SourceRepository(BaseModel):
    """
    Represents metadata and various maintenance metrics for a source code repository,
    including commit activity, issues, and pull request statistics.

    Attributes:
        id (str): Unique identifier for the repository. Example: 'github-repo-id'.
        type (str): Type of the source repository. Example: 'github'.
        name (str): Name of the repository. Example: 'example-repo'.
        description (Optional[str]): Description of the repository. Example: 'Sample GitHub repo'.
        url (str): URL to the source repository. Example: 'https://github.com/example/repo'.
        is_archived (bool): Indicates if the repository is archived.
        is_disabled (bool): Indicates if the repository is disabled.
        is_fork (bool): Indicates if the repository is a fork of another repository.
        is_locked (bool): Indicates if the repository is locked.
        created_at (str): Creation date of the repository in ISO-8601 format.
        updated_at (str): Last update timestamp of the repository in ISO-8601 format.
        archived_at (Optional[str]): Archiving date of the repository.
        stars_count (int): Number of stars the repository has.
        languages: str
        commits_frequency: Optional[MaintenanceMetric]
        commits_recency: Optional[MaintenanceMetric]
        issues_lifetime: Optional[MaintenanceMetric]
        issues_open_percentage: Optional[MaintenanceMetric]
        pull_requests_lifetime: Optional[MaintenanceMetric]
        pull_requests_open_percentage: Optional[MaintenanceMetric]
    """

    id: str
    type: str
    name: str
    description: Optional[str]
    url: str
    is_archived: bool
    is_disabled: bool
    is_fork: bool
    is_locked: bool
    created_at: str
    updated_at: str
    archived_at: Optional[str]
    stars_count: int
    languages: str
    commits_frequency: Optional[MaintenanceMetric]
    commits_recency: Optional[MaintenanceMetric]
    issues_lifetime: Optional[MaintenanceMetric]
    issues_open_percentage: Optional[MaintenanceMetric]
    pull_requests_lifetime: Optional[MaintenanceMetric]
    pull_requests_open_percentage: Optional[MaintenanceMetric]


class PackageMetadata(BaseModel):
    """
    Represents a found package by binary repository ID and type. It might contain metadata about
    published packages from both binary repositories and corresponding source code repositories.

    Attributes:
        binary_repository (BinaryRepository): Metadata from the corresponding binary repository.
        source_repository (Optional[SourceRepository]): Metadata from the corresponding source repository.
    """

    binary_repository: BinaryRepository
    source_repository: Optional[SourceRepository]


class PackagesResponse(BaseModel):
    """
    Represents the response containing a list of found packages based on the request.

    Attributes:
        packages (List[PackageMetadata]): List of found packages.
    """

    packages: List[PackageMetadata]


class PackageRequest(BaseModel):
    """
    Represents single package to fetch corresponding source repository and metadata.

    Attributes:
        binary_repository_type (str): Type of the binary repository. Example: 'maven'.
        binary_repository_id (str): Unique identifier for the package. Example: 'example-package-id'.
    """

    binary_repository_type: str
    binary_repository_id: str


class PackagesRequest(BaseModel):
    """
    Represents a request containing a list of binary packages to fetch
    corresponding source repositories and metadata.

    Attributes:
        packages (List[PackageRequest]): List of binary package identifiers. Maximum length is 100.
    """

    packages: List[PackageRequest]
