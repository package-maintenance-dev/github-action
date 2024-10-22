from typing import List, Set, Optional, Tuple

from packageurl import PackageURL

from action.arguments.action_arguments import (
    PackageMetric,
    PackageMetricScore,
    ActionArguments,
)
from action.clients.package_maintenance.model import PackageMetadata, MaintenanceMetric


class PackagesMaintenanceReport:
    @staticmethod
    def create(
        packages: List[PackageURL],
        packages_maintenance: List[PackageMetadata],
        action_arguments: ActionArguments,
    ) -> "PackagesMaintenanceReport":
        return PackagesMaintenanceReport(
            packages, packages_maintenance, action_arguments.packages_scores_thresholds
        )

    """
    Represents a report based on a repository packages (fetched from dependency graph GitHub API) and
    corresponding maintenance metadata (fetched from package-maintenance.dev API).

    This report provides following information:
    - List of packages that falls below the maintenance score threshold.
    """

    def __init__(
        self,
        packages: List["PackageURL"],
        packages_maintenance: List[PackageMetadata],
        packages_scores_thresholds: dict[PackageMetric, PackageMetricScore],
    ):
        self._packages = packages
        self._packages_maintenance = packages_maintenance
        self._packages_scores_thresholds = packages_scores_thresholds

    def render(self) -> str:
        """
        Renders the report as a markdown string.
        """
        report = ""
        missing_data_packages = self.missing_data_packages()
        if missing_data_packages:
            report += "## Missing data packages\n"
            for missing_data_package in missing_data_packages:
                report += f"- {missing_data_package}\n"
            report += "\n"

        below_threshold_packages = self.below_threshold_packages()
        if below_threshold_packages:
            report += "## Below threshold packages\n"
            for package, metric, package_metric in below_threshold_packages:
                report += f"- {package} - {metric}: {package_metric.score}\n"
            report += "\n"

        return report

    def missing_data_packages(self) -> List["PackageURL"]:
        """
        Returns a string representation of missing data packages.
        """
        packages_maintenance_ids: Set[Tuple[str, str]] = set()
        for package_maintenance in self._packages_maintenance:
            packages_maintenance_ids.add(
                (
                    package_maintenance.binary_repository.type,
                    package_maintenance.binary_repository.id,
                )
            )

        missing_data_packages = []
        for package in self._packages:
            if (package.type, package.name) not in packages_maintenance_ids:
                missing_data_packages.append(package)
        return missing_data_packages

    def below_threshold_packages(
        self,
    ) -> List[Tuple[PackageMetadata, PackageMetric, MaintenanceMetric]]:
        """
        Returns a string representation of packages that falls below the maintenance score threshold.
        """
        below_threshold_packages = []
        for package in self._packages_maintenance:
            for (
                threshold_metric,
                threshold_score,
            ) in self._packages_scores_thresholds.items():
                package_metric = self._get_package_metric(package, threshold_metric)
                if package_metric is None:
                    continue
                threshold = threshold_score.value
                value = package_metric.score
                # Check if the metric value is below the threshold. Because score is in range from A to D
                # the direct alphabetical comparison is not applicable, and we need to reverse it.
                metric_value_below_threshold = threshold < value

                if metric_value_below_threshold:
                    bellow_threshold = (
                        package,
                        threshold_metric,
                        package_metric,
                    )
                    below_threshold_packages.append(bellow_threshold)
        return below_threshold_packages

    def _get_package_metric(
        self, package: PackageMetadata, metric: PackageMetric
    ) -> Optional[MaintenanceMetric]:
        source_repository = package.source_repository
        match metric:
            case PackageMetric.binary_release_recency:
                return package.binary_repository.release_recency
            case PackageMetric.source_commit_frequency:
                return (
                    source_repository.commits_frequency if source_repository else None
                )
            case PackageMetric.source_commit_recency:
                return source_repository.commits_recency if source_repository else None
            case PackageMetric.issues_lifetime:
                return source_repository.issues_lifetime if source_repository else None
            case PackageMetric.issues_open_percentage:
                return (
                    source_repository.issues_open_percentage
                    if source_repository
                    else None
                )
            case PackageMetric.pull_requests_lifetime:
                return (
                    source_repository.pull_requests_lifetime
                    if source_repository
                    else None
                )
            case PackageMetric.pull_requests_open_percentage:
                return (
                    source_repository.pull_requests_open_percentage
                    if source_repository
                    else None
                )
            case _:
                return None
