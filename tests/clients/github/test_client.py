from unittest.mock import patch

import pytest

from src.clients.github.client import fetch_github_sbom
from src.clients.github.model import SBOMResponse


@pytest.fixture
def mock_github_response():
    return {
        "sbom": {
            "SPDXID": "SPDXRef-DOCUMENT",
            "spdxVersion": "SPDX-2.3",
            "creationInfo": {
                "created": "2021-09-01T00:00:00Z",
                "creators": [
                    "Tool: GitHub.com-Dependency-Graph"
                ]
            },
            "name": "github/example",
            "dataLicense": "CC0-1.0",
            "documentDescribes": [
                "github/example"
            ],
            "documentNamespace": "https://github.com/github/example/dependency_graph/sbom-abcdef123456",
            "packages": [
                {
                    "SPDXID": "SPDXRef-Package",
                    "name": "rubygems:rails",
                    "versionInfo": "1.0.0",
                    "downloadLocation": "NOASSERTION",
                    "filesAnalyzed": False,
                    "licenseConcluded": "MIT",
                    "licenseDeclared": "MIT",
                    "supplier": "NOASSERTION",
                    "copyrightText": "Copyright (c) 1985 GitHub.com"
                }
            ]
        }
    }

@patch('requests.get')
def test_fetch_github_sbom(mock_get, mock_github_response):
    # Mock the response from requests.get
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_github_response

    # Call the function
    sbom_response = fetch_github_sbom('github', 'example', 'your-token')

    # Assert that the response is correctly parsed into the SBOMResponse model
    assert isinstance(sbom_response, SBOMResponse)
    assert sbom_response.sbom.name == "github/example"
    assert sbom_response.sbom.packages[0].name == "rubygems:rails"
    assert sbom_response.sbom.packages[0].licenseConcluded == "MIT"

