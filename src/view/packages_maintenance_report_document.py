from typing import Optional, List, Set

from src.arguments.action_arguments import MaintenanceMetricSlug
from src.clients.package_maintenance.model import MaintenanceMetric
from src.models.packages_maintenance_report import PackagesMaintenanceReport
from src.models.packages_maintenance_report_row import PackagesMaintenanceReportRow
from src.view.markdown_document import MarkdownDocument
from src.view.markdown_utils import render_colored_code, render_url, render_colored_code_conditionally, render_code

NA = "`*`"
RED_WARNING = render_colored_code("⚠", "red")


class PackagesMaintenanceReportDocument:
    """
    Represents a markdown document for a package maintenance report.
    """

    def __init__(self, report: PackagesMaintenanceReport):
        self._report = report

    def render(self) -> str:
        """
        Renders the report as a markdown string.
        """
        report = MarkdownDocument()
        self._render_header(report)
        self._render_found_packages(report)
        self._render_missing_packages(report)
        self._report_footer(report)

        content = report.get_content()
        return content

    def _render_header(self, report: MarkdownDocument) -> None:
        report.heading("Package maintenance report", level=3)
        report.text(
            "This report provides brief information about current repository dependencies maintenance status.\n"
        )

    def _render_found_packages(self, report: MarkdownDocument) -> None:
        report.heading("Found packages", level=3)
        report.text("")
        headers = [
            "Type",
            "Id",
            "Latest version",
            "URLs",
            "Release recency",
            "Commits recency",
            "Commits frequency",
            "Issues lifetime",
            "Issues open percentage",
            "Pull requests lifetime",
            "Pull requests open percentage",
        ]

        rows = [self._render_found_packages_row(package) for package in self._report.found_packages()]

        report.table(headers=headers, rows=rows)
        report.text(f"`{NA}` - Data is not available or is not enough to calculate a score;")
        report.text(f"{RED_WARNING} - A package maintenance score is below the threshold;")

    def _render_found_packages_row(self, row: PackagesMaintenanceReportRow) -> List[str]:
        below_threshold = row.is_maintenance_below_threshold()
        package = row.package
        binary_repository = package.binary_repository

        type = render_colored_code_conditionally(binary_repository.type, "red", below_threshold)
        id = render_colored_code_conditionally(binary_repository.id, "red", below_threshold)
        version = render_code(binary_repository.latest_version)
        urls = self._render_urls(row)
        release_recency = self._render_binary_release_recency(row)
        commits_recency = self._render_source_commits_recency(row)
        commits_frequency = self._render_source_commits_frequency(row)
        issues_lifetime = self._render_issues_lifetime(row)
        issues_open_percentage = self._render_issues_open_percentage(row)
        pull_requests_lifetime = self._render_pull_requests_lifetime(row)
        pull_requests_open_percentage = self._render_source_pull_requests_open_percentage(row)

        return [
            type,
            id,
            version,
            urls,
            release_recency,
            commits_recency,
            commits_frequency,
            issues_lifetime,
            issues_open_percentage,
            pull_requests_lifetime,
            pull_requests_open_percentage,
        ]

    def _render_urls(self, row: PackagesMaintenanceReportRow):
        binary_url = render_url("binary", row.package.binary_repository.url)
        source_repository = row.package.source_repository
        if source_repository:
            source_url = render_url("source", source_repository.url)
            return f"{binary_url} / {source_url}"
        return binary_url

    def _render_source_commits_frequency(self, row: PackagesMaintenanceReportRow):
        repository = row.package.source_repository
        commit_frequency = repository.commits_frequency if repository else None
        return self._render_maintenance_metric(
            commit_frequency, MaintenanceMetricSlug.source_commit_frequency, row.below_threshold_metrics
        )

    def _render_binary_release_recency(self, row: PackagesMaintenanceReportRow):
        return self._render_maintenance_metric(
            row.package.binary_repository.release_recency,
            MaintenanceMetricSlug.binary_release_recency,
            row.below_threshold_metrics,
        )

    def _render_source_commits_recency(self, row: PackagesMaintenanceReportRow):
        repository = row.package.source_repository
        commits_recency = repository.commits_recency if repository else None
        return self._render_maintenance_metric(
            commits_recency, MaintenanceMetricSlug.source_commit_recency, row.below_threshold_metrics
        )

    def _render_issues_lifetime(self, row: PackagesMaintenanceReportRow):
        repository = row.package.source_repository
        issues_lifetime = repository.issues_lifetime if repository else None
        return self._render_maintenance_metric(
            issues_lifetime, MaintenanceMetricSlug.issues_lifetime, row.below_threshold_metrics
        )

    def _render_issues_open_percentage(self, row: PackagesMaintenanceReportRow):
        repository = row.package.source_repository
        issues_open_percentage = repository.issues_open_percentage if repository else None
        return self._render_maintenance_metric(
            issues_open_percentage, MaintenanceMetricSlug.issues_open_percentage, row.below_threshold_metrics
        )

    def _render_pull_requests_lifetime(self, row: PackagesMaintenanceReportRow):
        repository = row.package.source_repository
        pull_requests_lifetime = repository.pull_requests_lifetime if repository else None
        return self._render_maintenance_metric(
            pull_requests_lifetime, MaintenanceMetricSlug.pull_requests_lifetime, row.below_threshold_metrics
        )

    def _render_source_pull_requests_open_percentage(self, row: PackagesMaintenanceReportRow):
        repository = row.package.source_repository
        pull_requests_open_percentage = repository.pull_requests_open_percentage if repository else None
        return self._render_maintenance_metric(
            pull_requests_open_percentage,
            MaintenanceMetricSlug.pull_requests_open_percentage,
            row.below_threshold_metrics,
        )

    def _render_maintenance_metric(
        self,
        metric: Optional[MaintenanceMetric],
        slug: MaintenanceMetricSlug,
        below_threshold_metrics: Set[MaintenanceMetricSlug],
    ) -> str:
        if metric is None:
            return NA

        value = metric.value
        score = metric.score
        score_color = ""
        if score == "A":
            score_color = "green"
        if score == "B":
            score_color = "yellow"
        if score == "C":
            score_color = "orange"
        if score == "D":
            score_color = "red"

        score_rendered = render_colored_code(score, score_color)
        below_threshold = slug in below_threshold_metrics
        error_sign = RED_WARNING if below_threshold else ""
        rendered_metric = f"{error_sign} {value} / {score_rendered}"
        return rendered_metric

    def _render_missing_packages(self, report):
        missing_data_packages = self._report.missing_data_packages()
        if not missing_data_packages:
            return

        report.empty_line()
        report.heading("Missing data packages", level=3)
        report.text("The following packages are missing maintenance data in the package-maintenance.dev index")
        report.empty_line()
        report.table(
            headers=["Type", "Namespace", "Name"],
            rows=[[package.type, package.namespace or NA, package.name] for package in missing_data_packages],
        )

    def _report_footer(self, report: MarkdownDocument) -> None:
        report.empty_line()
        report.text("This report was generated by the Package Maintenance Report Action.")
        report.text(
            "For more information, visit [action documentation](https://github.com/package-maintenance-dev/github-action)."
        )
