import logging
from typing import List

from packageurl import PackageURL

from action.clients.package_maintenance.client import fetch_packages
from action.clients.package_maintenance.model import (
    PackageRequest,
    PackagesRequest,
    PackagesResponse,
    PackageMetadata,
)
from action.domain.commons import package_url_to_repository_id
from action.utils.list_utils import grouped

# package-maintenance.dev API has a limit of 100 packages per request. Hence, we need to split the list of packages
# into chunks of 100 packages each.
PACKAGE_MAINTENANCE_API_MAX_SIZE = 100

logger = logging.getLogger(__name__)


class PackagesMaintenanceRetriever:
    """
    Retrieves maintenance metadata for a list of packages based on the package-maintenance.dev API.
    """

    def get_packages_maintenance(
        self, packages_urls: List[PackageURL]
    ) -> List[PackageMetadata]:
        grouped_packages_urls = grouped(
            input_list=packages_urls, size=PACKAGE_MAINTENANCE_API_MAX_SIZE
        )
        all_packages_maintenance: List[PackageMetadata] = []
        for group in grouped_packages_urls:
            logger.info(
                f"Retrieving maintenance metadata for group of {len(group)} packages..."
            )
            packages_maintenance = self._get_packages_maintenance(packages_urls)
            all_packages_maintenance.extend(packages_maintenance)
        return all_packages_maintenance

    def _get_packages_maintenance(
        self, packages_urls: List[PackageURL]
    ) -> List[PackageMetadata]:
        packages: List[PackageRequest] = []
        for package_url in packages_urls:
            binary_repository_type_id = package_url_to_repository_id(package_url)
            if binary_repository_type_id:
                binary_repository_type, binary_repository_id = binary_repository_type_id
                package = PackageRequest(
                    binary_repository_type=binary_repository_type,
                    binary_repository_id=binary_repository_id,
                )
                packages.append(package)
            else:
                logger.info(
                    f"Package '{package_url}' has an unsupported type '{package_url.type}'. Skipping..."
                )
        packages_request = PackagesRequest(packages=packages)
        response: PackagesResponse = fetch_packages(packages_request)
        return response.packages
