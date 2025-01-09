import logging
from typing import Optional, List

from packageurl import PackageURL

from src.arguments.action_arguments import ActionArguments
from src.clients.github.client import fetch_github_sbom
from src.clients.github.model import SBOMResponse, Package, ExternalRef
from src.models.packages_ignore_filter import PackagesIgnoreFilter

logger = logging.getLogger(__name__)


class PackagesRetriever:
    """
    Retrieves list of packages URLs to check for maintenance scores based on SBOM and action arguments.
    Internally, it retrieves SBOM for a given repository and filters out packages based on external reference
    type (purl), package type (maven, npm, etc.) and `packages_ignore` action argument.
    Packages that match the criteria are returned as a list of package URLs.
    """

    @staticmethod
    def create(arguments: ActionArguments):
        """
        Create new packages retriever from arguments

        :param arguments: action arguments to supplied to the action.
        :return: constructed packages retriever.
        """
        packages_ignore_filter = PackagesIgnoreFilter.create(arguments)
        return PackagesRetriever(
            owner=arguments.github_repository_owner,
            name=arguments.github_repository_name,
            token=arguments.github_token,
            packages_ignore_filter=packages_ignore_filter,
        )

    def __init__(
        self,
        owner: str,
        name: str,
        token: Optional[str],
        packages_ignore_filter: PackagesIgnoreFilter,
    ):
        self._owner = owner
        self._name = name
        self._token = token
        self._packages_ignore_filter = packages_ignore_filter

    def get_packages_urls_to_check(self) -> List["PackageURL"]:
        """
        Get list of packages URLs to check for maintenance scores based on SBOM and action arguments.
        :return: list of package URLs to check
        """
        sbom = fetch_github_sbom(
            owner=self._owner,
            repo=self._name,
            token=self._token,
        )

        packages_urls = self._get_packages_urls_to_check(sbom)
        return packages_urls

    def _get_packages_urls_to_check(self, sbom: SBOMResponse) -> List["PackageURL"]:
        sbom_all_packages_urls: List["PackageURL"] = []
        for package in sbom.sbom.packages:
            packages_urls = self._get_package_external_refs(package)
            sbom_all_packages_urls.extend(packages_urls)
        return sbom_all_packages_urls

    def _get_package_external_refs(self, package: Package) -> List["PackageURL"]:
        packages_urls: List["PackageURL"] = []
        external_refs = package.externalRefs or []
        for external_ref in external_refs:
            package_url = self._get_package_url_from_external_ref(package, external_ref)
            if package_url:
                packages_urls.append(package_url)
        return packages_urls

    def _get_package_url_from_external_ref(self, package: Package, external_ref: ExternalRef) -> Optional["PackageURL"]:
        if external_ref.referenceType != "purl":
            logger.info(
                f"Package '{package.name}' has an unsupported reference type '{external_ref.referenceType}'. Skipping..."
            )
            return None

        purl = PackageURL.from_string(external_ref.referenceLocator)
        ignore = self._packages_ignore_filter.ignore(purl)
        if ignore:
            logger.info(f"Package '{package.name}' is ignored. Skipping...")
            return None

        return purl
