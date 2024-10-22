import logging

from action.arguments.action_arguments import ActionArguments
from action.domain.packages_maintenance_retriever import PackagesMaintenanceRetriever
from action.domain.packages_retriever import PackagesRetriever

logger = logging.getLogger(__name__)


def perform_action(arguments: ActionArguments):
    packages_retriever = PackagesRetriever.create(arguments)
    packages_maintenance_retriever = PackagesMaintenanceRetriever()

    packages_urls = packages_retriever.get_packages_urls_to_check()
    packages_maintenance = packages_maintenance_retriever.get_packages_maintenance(
        packages_urls
    )
    print(packages_maintenance)
