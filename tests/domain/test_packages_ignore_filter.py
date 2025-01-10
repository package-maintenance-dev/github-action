from packageurl import PackageURL

from src.models.packages_ignore_filter import PackagesIgnoreFilter
from src.arguments.action_arguments import ActionArguments


def test_allow_all_packages_if_no_argument_provided():
    args = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="name",
        packages_ignore=[])
    filter_instance = PackagesIgnoreFilter.create(args)

    purl = PackageURL(type="maven", namespace="com.example", name="example-package")
    assert not filter_instance.ignore(purl)


def test_ignore_packages_matching_type():
    args = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="name",
        packages_ignore=[
            PackageURL(type="maven", namespace="*", name="*")
        ]
    )
    filter_instance = PackagesIgnoreFilter.create(args)

    purl = PackageURL(type="maven", namespace="com.example", name="example-package")
    assert filter_instance.ignore(purl)


def test_ignore_packages_matching_type_namespace():
    args = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="name",
        packages_ignore=[
            PackageURL(type="maven", namespace="com.example", name="*")
        ]
    )
    filter_instance = PackagesIgnoreFilter.create(args)

    purl = PackageURL(type="maven", namespace="com.example", name="example-package")
    assert filter_instance.ignore(purl)

    purl_different_namespace = PackageURL(type="maven", namespace="com.other", name="example-package")
    assert not filter_instance.ignore(purl_different_namespace)


def test_ignore_packages_matching_type_namespace_name():
    args = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="name",
        packages_ignore=[
            PackageURL(type="maven", namespace="com.example", name="example-package")
        ]
    )
    filter_instance = PackagesIgnoreFilter.create(args)

    purl = PackageURL(type="maven", namespace="com.example", name="example-package")
    assert filter_instance.ignore(purl)

    purl_different_name = PackageURL(type="maven", namespace="com.example", name="different-package")
    assert not filter_instance.ignore(purl_different_name)


def test_version_has_no_effect():
    args = ActionArguments(
        github_repository_owner="owner",
        github_repository_name="name",
        packages_ignore=[
            PackageURL(type="maven", namespace="com.example", name="example-package")
        ]
    )
    filter_instance = PackagesIgnoreFilter.create(args)

    purl_with_version = PackageURL(type="maven", namespace="com.example", name="example-package", version="1.0.0")
    assert filter_instance.ignore(purl_with_version)

    purl_with_different_version = PackageURL(type="maven", namespace="com.example", name="example-package",
                                             version="2.0.0")
    assert filter_instance.ignore(purl_with_different_version)
