import typing
from typing import Optional

import requests

from action.clients.github.model import SBOMResponse


@typing.no_type_check
def fetch_github_sbom(
    owner: str, repo: str, token: Optional[str] = None
) -> SBOMResponse:
    """
    Fetches the SBOM for a given GitHub repository and parses it into a Pydantic model.

    Args:
        owner (str): The owner of the repository.
        repo (str): The repository name.
        token (Optional[str]): The GitHub personal access token. Default is None.

    Returns:
        SBOMResponse: The parsed SBOM data as a Pydantic model.

    Example curl request:
        curl -L \\
          -H "Accept: application/vnd.github+json" \\
          -H "Authorization: Bearer <YOUR-TOKEN>" \\
          -H "X-GitHub-Api-Version: 2022-11-28" \\
          https://api.github.com/repos/OWNER/REPO/dependency-graph/sbom

    More details can be found in GitHub's official documentation:
    https://docs.github.com/en/rest/dependency-graph/sboms?apiVersion=2022-11-28#export-a-software-bill-of-materials-sbom-for-a-repository
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/dependency-graph/sbom"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return SBOMResponse.model_validate(response.json())
    else:
        response.raise_for_status()
