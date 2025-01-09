from typing import Optional, List

from src.clients.package_maintenance.model import MaintenanceMetric
from src.models.packages_maintenance_report import PackagesMaintenanceReport
from src.models.packages_maintenance_report_row import PackagesMaintenanceReportRow
from src.view.markdown_document import MarkdownDocument

NA = "`*`"


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
        report.text(f"`{NA}` - Data not available or not enough to calculate score")

    def _render_found_packages_row(self, row: PackagesMaintenanceReportRow) -> List[str]:
        below_threshold = row.is_maintenance_below_threshold()
        package = row.package
        binary_repository = package.binary_repository
        source_repository = package.source_repository

        type = self._render_colored_code_conditionally(binary_repository.type, "red", below_threshold)
        id = self._render_colored_code_conditionally(binary_repository.id, "red", below_threshold)
        version = self._render_code(binary_repository.latest_version)
        urls = self._render_url("binary", binary_repository.url)
        release_recency = self._render_maintenance_metric(binary_repository.release_recency)

        commits_recency = NA
        commits_frequency = NA
        issues_lifetime = NA
        issues_open_percentage = NA
        pull_requests_lifetime = NA
        pull_requests_open_percentage = NA

        if source_repository:
            urls = f"{urls} / {self._render_url('source', source_repository.url)}"
            commits_recency = self._render_maintenance_metric(source_repository.commits_recency)
            commits_frequency = self._render_maintenance_metric(source_repository.commits_frequency)
            issues_lifetime = self._render_maintenance_metric(source_repository.issues_lifetime)
            issues_open_percentage = self._render_maintenance_metric(source_repository.issues_open_percentage)
            pull_requests_lifetime = self._render_maintenance_metric(source_repository.pull_requests_lifetime)
            pull_requests_open_percentage = self._render_maintenance_metric(
                source_repository.pull_requests_open_percentage
            )

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

    def _render_maintenance_metric(self, metric: Optional[MaintenanceMetric]):
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

        score_rendered = self._render_colored_code(score, score_color)
        return f"{value} / {score_rendered}"

    def _render_code(self, text: str):
        return f"<code>{text}</code>"

    def _render_colored_code(self, text: str, color: str):
        return f'<code style="color: {color}">{text}</code>'

    def _render_colored_code_conditionally(self, text: str, color: str, condition: bool):
        if condition:
            return self._render_colored_code(text, color)
        return self._render_code(text)

    def _render_url(self, name: str, url: str):
        return f"[{name}]({url})"

    def _render_missing_packages(self, report):
        missing_data_packages = self._report.missing_data_packages()
        if missing_data_packages:
            report.text("")
            report.heading("Missing data packages", level=3)
            report.text("The following packages are missing maintenance data in the package-maintenance.dev index")
            report.text("")
            report.table(
                headers=["Type", "Namespace", "Name"],
                rows=[[package.type, package.namespace or NA, package.name] for package in missing_data_packages],
            )

    def _report_footer(self, report: MarkdownDocument) -> None:
        report.text("\n")
        report.text("This report was generated by the Package Maintenance Report Action.")
        report.text(
            "For more information, visit [action documentation](https://github.com/package-maintenance-dev/github-action)."
        )
