import logging

import argparse

from action.arguments.parse_action_arguments import parse_action_arguments
from action.domain.packages_maintenance_report import PackagesMaintenanceReport
from action.domain.packages_maintenance_retriever import PackagesMaintenanceRetriever
from action.domain.packages_retriever import PackagesRetriever

logger = logging.getLogger(__name__)


def perform_action(raw_arguments: argparse.Namespace):
    """
    Perform action based on the arguments: fetch packages URLs, fetch maintenance data, generate and print report.
    """
    arguments = parse_action_arguments(raw_arguments)

    packages_retriever = PackagesRetriever.create(arguments)
    packages_maintenance_retriever = PackagesMaintenanceRetriever()

    packages_urls = packages_retriever.get_packages_urls_to_check()
    packages_maintenance = packages_maintenance_retriever.get_packages_maintenance(
        packages_urls
    )
    report = PackagesMaintenanceReport.create(
        packages=packages_urls,
        packages_maintenance=packages_maintenance,
        action_arguments=arguments,
    )
    print(report.render())
