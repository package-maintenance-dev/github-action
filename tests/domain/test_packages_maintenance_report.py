from typing import List

from packageurl import PackageURL

from src.arguments.action_arguments import PackageMetric, PackageMetricScore, ActionArguments
from src.clients.package_maintenance.model import PackageMetadata, MaintenanceMetric, BinaryRepository
from src.domain.packages_maintenance_report import PackagesMaintenanceReport


def test_missing_data_packages():
    packages = [
        PackageURL(type="maven", namespace="com.example", name="example-package"),
        PackageURL(type="maven", namespace="com.example-2", name="example-package-2")
    ]
    packages_maintenance: List[PackageMetadata] = [
        PackageMetadata(
            binary_repository=BinaryRepository(
                type="maven",
                id="com.example:example-package",
                latest_version="1.0.0",
                latest_version_published_at="2021-11-03T00:00:00Z",
                name=None,
                description=None,
                url="https://repo.example.com/package",
                source_repository_original_url=None,
                source_repository_normal_url=None,
                source_repository_id=None,
                source_repository_type=None,
                release_recency=MaintenanceMetric(score="A", value=100)
            ),
            source_repository=None
        )
    ]
    action_arguments = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="repo",
        packages_scores_thresholds={}
    )

    report = PackagesMaintenanceReport.create(packages, packages_maintenance, action_arguments)
    missing = report.missing_data_packages()

    assert len(missing) == 1
    assert missing[0].name == "example-package-2"


def test_below_threshold_packages():
    packages = [PackageURL(type="maven", namespace="com.example", name="example-package")]
    maintenance_metric = MaintenanceMetric(score="C", value=75)
    package_metadata = PackageMetadata(
        binary_repository=BinaryRepository(
            type="maven",
            id="example-package",
            latest_version="1.0.0",
            latest_version_published_at="2021-11-03T00:00:00Z",
            name=None,
            description=None,
            url="https://repo.example.com/package",
            source_repository_original_url=None,
            source_repository_normal_url=None,
            source_repository_id=None,
            source_repository_type=None,
            release_recency=maintenance_metric
        ),
        source_repository=None
    )

    action_arguments = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="repo",
        packages_scores_thresholds={
            PackageMetric.binary_release_recency: PackageMetricScore("B")
        }
    )

    report = PackagesMaintenanceReport.create(packages, [package_metadata], action_arguments)
    below_threshold = report.below_threshold_packages()

    assert len(below_threshold) == 1
    assert below_threshold[0][0].binary_repository.id == "example-package"
    assert below_threshold[0][1] == PackageMetric.binary_release_recency
    assert below_threshold[0][2].score == "C"


def test_get_package_metric_none():
    packages = [PackageURL(type="maven", namespace="com.example", name="example-package")]
    maintenance_metric = MaintenanceMetric(score="C", value=75)
    package_metadata = PackageMetadata(
        binary_repository=BinaryRepository(
            type="maven",
            id="example-package",
            latest_version="1.0.0",
            latest_version_published_at="2021-11-03T00:00:00Z",
            name=None,
            description=None,
            url="https://repo.example.com/package",
            source_repository_original_url=None,
            source_repository_normal_url=None,
            source_repository_id=None,
            source_repository_type=None,
            release_recency=maintenance_metric
        ),
        source_repository=None
    )

    action_arguments = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="repo",
        packages_scores_thresholds={}
    )

    report = PackagesMaintenanceReport.create(packages, [package_metadata], action_arguments)
    assert report._get_package_metric(package_metadata, PackageMetric.issues_lifetime) is None
