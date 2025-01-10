from typing import List, Optional
from pydantic import BaseModel


class ExternalRef(BaseModel):
    """
    Represents an external reference for a package.

    Attributes:
        referenceCategory (str): The category of reference (e.g., 'PACKAGE-MANAGER').
        referenceLocator (str): A locator for the external resource (e.g., 'pkg:gem/rails@6.0.1').
        referenceType (str): The type of reference (e.g., 'purl').
    """

    referenceCategory: str
    referenceLocator: str
    referenceType: str


class Package(BaseModel):
    """
    Represents a package within the SBOM.

    Attributes:
        SPDXID (str): A unique SPDX identifier for the package (e.g., 'SPDXRef-Package').
        name (str): The name of the package (e.g., 'rubygems:github/github').
        versionInfo (str): The version of the package (e.g., '1.0.0').
        downloadLocation (str): The location where the package can be downloaded, or 'NOASSERTION'.
        filesAnalyzed (bool): Whether the files have been analyzed (e.g., False).
        licenseConcluded (Optional[str]): The concluded license for the package (e.g., 'MIT').
        licenseDeclared (Optional[str]): The declared license for the package (e.g., 'NOASSERTION').
        supplier (str): The distribution source of the package (e.g., 'NOASSERTION').
        copyrightText (Optional[str]): The copyright holders and dates (e.g., 'Copyright (c) 1985 GitHub.com').
        externalRefs (Optional[List[ExternalRef]]): External references related to the package.
    """

    SPDXID: str
    name: str
    filesAnalyzed: bool
    versionInfo: Optional[str] = None
    downloadLocation: Optional[str] = None
    licenseConcluded: Optional[str] = None
    licenseDeclared: Optional[str] = None
    supplier: Optional[str] = None
    copyrightText: Optional[str] = None
    externalRefs: Optional[List[ExternalRef]] = None


class CreationInfo(BaseModel):
    """
    Information about the creation of the SBOM document.

    Attributes:
        created (str): The date and time the document was created (e.g., '2021-11-03T00:00:00Z').
        creators (List[str]): The tools used to create the document (e.g., 'GitHub').
    """

    created: str
    creators: List[str]


class SBOM(BaseModel):
    """
    Represents the full SBOM document.

    Attributes:
        SPDXID (str): The SPDX identifier for the document (e.g., 'SPDXRef-DOCUMENT').
        spdxVersion (str): The version of the SPDX specification (e.g., 'SPDX-2.3').
        creationInfo (CreationInfo): Information about the creation of the document.
        name (str): The name of the SPDX document (e.g., 'github/github').
        dataLicense (str): The license under which the document is licensed (e.g., 'CC0-1.0').
        documentDescribes (List[str]): The name of the repository the document describes (e.g., 'github/github').
        documentNamespace (str): The namespace URL of the document
        (e.g., 'https://github.com/example/dependency_graph/sbom-123').
        packages (List[Package]): A list of packages included in the SBOM.
    """

    SPDXID: str
    spdxVersion: str
    creationInfo: CreationInfo
    name: str
    dataLicense: str
    documentNamespace: str
    packages: List[Package]
    documentDescribes: List[str] = []


class SBOMResponse(BaseModel):
    """
    Represents the response from the GitHub SBOM API containing the SBOM.

    Attributes:
        sbom (SBOM): The SBOM document and its associated data.
    """

    sbom: SBOM
