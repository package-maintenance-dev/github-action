import logging
import typing

import requests

from src.clients.package_maintenance.model import PackagesRequest, PackagesResponse

API_HOST = "https://package-maintenance.dev"

logger = logging.getLogger(__name__)


@typing.no_type_check
def fetch_packages(payload: PackagesRequest) -> PackagesResponse:
    """
    Fetches a bulk of binary packages along with corresponding source repositories.

    Args:
        payload (PackagesRequestApiModel): The request payload containing a list of packages.

    Returns:
        PackagesApiModel: The response containing found package and source repository metadata.

    Raises:
        Exception: If the API returns any non success status code.
    """
    url = f"{API_HOST}/api/v0/packages"
    headers = {"Content-Type": "application/json"}
    json = payload.model_dump()
    response = requests.post(url, json=json, headers=headers)

    if response.status_code == 200:
        json = response.json()
        return PackagesResponse.model_validate(json)
    else:
        logger.error("Failed to fetch packages. Response body: %s", response.text)
        response.raise_for_status()
