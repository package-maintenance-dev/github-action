import logging
import os

import argparse

from src.arguments.parse_action_arguments import parse_action_arguments
from src.models.packages_maintenance_report import PackagesMaintenanceReport
from src.service.packages_maintenance_retriever import PackagesMaintenanceRetriever
from src.service.packages_retriever import PackagesRetriever
from src.view.packages_maintenance_report_document import PackagesMaintenanceReportDocument

logger = logging.getLogger(__name__)


def perform_action(raw_arguments: argparse.Namespace):
    """
    Perform action based on the arguments: fetch packages URLs, fetch maintenance data, generate and print report.
    """
    arguments = parse_action_arguments(raw_arguments)

    packages_retriever = PackagesRetriever.create(arguments)
    packages_maintenance_retriever = PackagesMaintenanceRetriever()

    packages_urls = packages_retriever.get_packages_urls_to_check()
    packages_maintenance = packages_maintenance_retriever.get_packages_maintenance(packages_urls)
    report = PackagesMaintenanceReport.create(
        packages=packages_urls,
        packages_maintenance=packages_maintenance,
        action_arguments=arguments,
    )
    document = PackagesMaintenanceReportDocument(report)

    summary_file = os.getenv("GITHUB_STEP_SUMMARY")

    # Check if the environment variable exists
    report_markdown = document.render()
    if summary_file:
        with open(summary_file, "a") as f:
            f.write(report_markdown)
    else:
        print(f"GITHUB_STEP_SUMMARY is not set. Printing the report to stdout: \n{report_markdown}")
