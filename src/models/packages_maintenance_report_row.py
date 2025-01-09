from typing import List

from pydantic import BaseModel

from src.arguments.action_arguments import MaintenanceMetricSlug
from src.clients.package_maintenance.model import PackageMetadata


class PackagesMaintenanceReportRow(BaseModel):
    """
    Represents a row in the maintenance report.
    :param package: PackageMetadata - package metadata.
    :param below_threshold_metrics: List[MaintenanceMetricSlug] - list of metrics that are below the threshold.
    """

    package: PackageMetadata
    below_threshold_metrics: List[MaintenanceMetricSlug]

    def is_maintenance_below_threshold(self) -> bool:
        """
        Checks if any of the metrics are below the threshold.
        """
        return len(self.below_threshold_metrics) > 0
