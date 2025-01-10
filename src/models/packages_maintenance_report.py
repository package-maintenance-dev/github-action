from typing import List, Set, Optional, Tuple

from packageurl import PackageURL

from src.models.packages_maintenance_report_row import PackagesMaintenanceReportRow
from src.arguments.action_arguments import (
    MaintenanceMetricSlug,
    MaintenanceMetricScore,
    ActionArguments,
)
from src.clients.package_maintenance.model import PackageMetadata, MaintenanceMetric
from src.models.commons import package_url_to_repository_id


class PackagesMaintenanceReport:
    @staticmethod
    def create(
        packages: List[PackageURL],
        packages_maintenance: List[PackageMetadata],
        action_arguments: ActionArguments,
    ) -> "PackagesMaintenanceReport":
        return PackagesMaintenanceReport(packages, packages_maintenance, action_arguments.packages_scores_thresholds)

    """
    Represents a report based on a repository packages (fetched from dependency graph GitHub API) and
    corresponding maintenance metadata (fetched from package-maintenance.dev API).

    This report provides following information:
    - List of all packages that including the information about the metrics that are below the threshold.
    - List of packages that are missing maintenance data in the package-maintenance.dev index.
    """

    def __init__(
        self,
        packages: List["PackageURL"],
        packages_maintenance: List[PackageMetadata],
        packages_scores_thresholds: dict[MaintenanceMetricSlug, MaintenanceMetricScore],
    ):
        self._packages = packages
        self._packages_maintenance = packages_maintenance
        self._packages_scores_thresholds = packages_scores_thresholds

    def missing_data_packages(self) -> Set["PackageURL"]:
        """
        Returns a list of packages that are missing maintenance data in the package-maintenance.dev index.
        """
        packages_maintenance_ids: Set[Tuple[str, str]] = set()
        for package_maintenance in self._packages_maintenance:
            packages_maintenance_ids.add(
                (
                    package_maintenance.binary_repository.type,
                    package_maintenance.binary_repository.id,
                )
            )

        missing_data_packages = set()
        for package_url in self._packages:
            binary_repository_type_id = package_url_to_repository_id(package_url)
            if binary_repository_type_id:
                binary_repository_type, binary_repository_id = binary_repository_type_id
                package_id = (
                    binary_repository_type,
                    binary_repository_id,
                )
                if package_id not in packages_maintenance_ids:
                    missing_data_packages.add(package_url)
        return missing_data_packages

    def found_packages(self) -> List[PackagesMaintenanceReportRow]:
        """
        Returns a list of all packages that including the information about the metrics that are below the threshold.
        """
        found_packages = [self._create_row(package) for package in self._packages_maintenance]
        return found_packages

    def _create_row(self, package: PackageMetadata) -> PackagesMaintenanceReportRow:
        below_threshold_metrics = self._get_below_threshold_metrics(package)
        return PackagesMaintenanceReportRow(package=package, below_threshold_metrics=below_threshold_metrics)

    def _get_below_threshold_metrics(self, package: PackageMetadata) -> Set[MaintenanceMetricSlug]:
        below_threshold_metrics: Set[MaintenanceMetricSlug] = set()
        for threshold in self._packages_scores_thresholds.items():
            threshold_metric, threshold_score = threshold
            package_metric = self._get_package_metric(package, threshold_metric)
            if package_metric is None:
                continue
            # Check if the metric value is below the threshold. Because score is in range from A to D
            # the direct alphabetical comparison is not applicable, and we need to reverse it.
            metric_value_below_threshold = threshold_score.value < package_metric.score

            if metric_value_below_threshold:
                below_threshold_metrics.add(threshold_metric)
        return below_threshold_metrics

    def _get_package_metric(
        self, package: PackageMetadata, metric: MaintenanceMetricSlug
    ) -> Optional[MaintenanceMetric]:
        source_repository = package.source_repository
        match metric:
            case MaintenanceMetricSlug.binary_release_recency:
                return package.binary_repository.release_recency
            case MaintenanceMetricSlug.source_commit_frequency:
                return source_repository.commits_frequency if source_repository else None
            case MaintenanceMetricSlug.source_commit_recency:
                return source_repository.commits_recency if source_repository else None
            case MaintenanceMetricSlug.issues_lifetime:
                return source_repository.issues_lifetime if source_repository else None
            case MaintenanceMetricSlug.issues_open_percentage:
                return source_repository.issues_open_percentage if source_repository else None
            case MaintenanceMetricSlug.pull_requests_lifetime:
                return source_repository.pull_requests_lifetime if source_repository else None
            case MaintenanceMetricSlug.pull_requests_open_percentage:
                return source_repository.pull_requests_open_percentage if source_repository else None
            case _:
                return None
