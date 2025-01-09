import pytest
from unittest.mock import patch

from src.clients.package_maintenance.client import fetch_packages
from src.clients.package_maintenance.model import PackagesRequest, PackagesResponse


@pytest.fixture
def mock_packages_response():
    return {
        "packages": [
            {
                "binary_repository": {
                    "id": "example-package-id",
                    "type": "maven",
                    "latest_version": "1.0.0",
                    "latest_version_published_at": "2021-11-03T00:00:00Z",
                    "name": "example-package",
                    "description": "A sample package",
                    "url": "https://repo.example.com/package",
                    "source_repository_original_url": "https://github.com/example/repo",
                    "source_repository_normal_url": None,
                    "source_repository_id": None,
                    "source_repository_type": None,
                    "release_recency": {
                        "value": 10,
                        "score": "A"
                    }
                },
                "source_repository": None
            }
        ]
    }


@patch('requests.post')
def test_fetch_packages_success(mock_post, mock_packages_response):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_packages_response

    payload = PackagesRequest(
        packages=[{"binary_repository_type": "maven", "binary_repository_id": "example-package-id"}]
    )

    response = fetch_packages(payload)

    assert isinstance(response, PackagesResponse)
    assert response.packages[0].binary_repository.name == "example-package"
    assert response.packages[0].binary_repository.release_recency.score == "A"
    assert response.packages[0].binary_repository.release_recency.value == 10
