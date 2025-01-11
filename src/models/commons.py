from typing import Optional, Tuple

from packageurl import PackageURL

MAVEN_PACKAGE_TYPE = "maven"
PYPI_PACKAGE_TYPE = "pypi"
SUPPORTED_PACKAGE_TYPES = [MAVEN_PACKAGE_TYPE, PYPI_PACKAGE_TYPE]


def package_url_to_repository_id(package_url: PackageURL) -> Optional[Tuple[str, str]]:
    """
    Converts a PackageURL to a binary repository ID if the package type is supported.
    Returns None if the package type is not supported.
    """
    match package_url.type:
        case package_type if package_type == MAVEN_PACKAGE_TYPE:
            return package_type, f"{package_url.namespace}:{package_url.name}"
        case package_type if package_type == PYPI_PACKAGE_TYPE:
            return package_type, package_url.name
        case _:
            return None
