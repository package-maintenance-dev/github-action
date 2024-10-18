import typing

import requests

from action.clients.package_maintenance.model import PackagesRequest, PackagesResponse


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
    url = "https://api.example.com/api/v0/packages"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload.model_dump_json(), headers=headers)

    if response.status_code == 200:
        return PackagesResponse.model_validate(response.json())
    else:
        response.raise_for_status()
