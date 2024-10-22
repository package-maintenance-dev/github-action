import pytest
from unittest.mock import patch
from packageurl import PackageURL
from action.arguments.action_arguments import ActionArguments
from action.clients.github.model import SBOMResponse, Package, SBOM, CreationInfo, ExternalRef
from action.domain.packages_retriever import PackagesRetriever


@pytest.fixture
def mock_sbom_response() -> SBOMResponse:
    return SBOMResponse(
        sbom=SBOM(
            SPDXID='SPDXRef-DOCUMENT',
            spdxVersion='SPDX-2.3',
            creationInfo=CreationInfo(
                created='2021-11-03T00:00:00Z',
                creators=['GitHub']
            ),
            name='github/github',
            dataLicense='CC0-1.0',
            documentDescribes=['github/github'],
            documentNamespace='',
            packages=[
                Package(
                    SPDXID = "SPDXRef-Package-1",
                    name = "example-package",
                    versionInfo = "1.0.0",
                    downloadLocation = "https://example.com/example-package-1.0.0.jar",
                    filesAnalyzed = True,
                    licenseConcluded = None,
                    licenseDeclared = None,
                    supplier= "GitHub",
                    copyrightText = None,
                    externalRefs=[
                        ExternalRef(
                            referenceCategory='package-manager',
                            referenceLocator='pkg:maven/com.example/example-package@1.0.0',
                            referenceType='purl'
                        )
                    ]
                )
            ]
        )
    )


@patch('action.domain.packages_retriever.fetch_github_sbom')
def test_get_packages_urls_to_check(fetch_github_sbom, mock_sbom_response: SBOMResponse):
    fetch_github_sbom.return_value = mock_sbom_response

    args = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="repo",
        github_token="token",
        packages_ignore=[]
    )
    retriever = PackagesRetriever.create(args)
    packages_urls = retriever.get_packages_urls_to_check()

    assert len(packages_urls) == 1
    assert isinstance(packages_urls[0], PackageURL)

    assert packages_urls[0].type == "maven"
    assert packages_urls[0].namespace == "com.example"
    assert packages_urls[0].name == "example-package"
    assert packages_urls[0].version == "1.0.0"


@patch('action.domain.packages_retriever.fetch_github_sbom')
def test_ignore_packages(fetch_github_sbom, mock_sbom_response: SBOMResponse):
    fetch_github_sbom.return_value = mock_sbom_response

    args = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="repo",
        github_token="token",
        packages_ignore=[PackageURL(type="maven", namespace="com.example", name="example-package")]
    )
    retriever = PackagesRetriever.create(args)

    packages_urls = retriever.get_packages_urls_to_check()

    assert len(packages_urls) == 0
