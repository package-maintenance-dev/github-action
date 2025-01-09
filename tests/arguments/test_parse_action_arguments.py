import pytest
from argparse import Namespace
from packageurl import PackageURL
from src.arguments.action_arguments import MaintenanceMetricSlug, MaintenanceMetricScore, ActionArguments
from src.arguments.parse_action_arguments import _parse_github_repository, _parse_packages_ignore, \
    _parse_packages_scores_thresholds, parse_action_arguments


def test_parse_github_repository():
    args = Namespace(github_repository="owner/repo")
    owner, repo = _parse_github_repository(args)
    assert owner == "owner"
    assert repo == "repo"

    args_invalid = Namespace(github_repository="invalid_format")
    with pytest.raises(ValueError, match="Invalid format for GitHub repository"):
        _parse_github_repository(args_invalid)

def test_parse_packages_ignore():
    args = Namespace(packages_ignore="pkg:pip/example\npkg:maven/com.example/example")
    result = _parse_packages_ignore(args)
    assert len(result) == 2
    assert result[0] == PackageURL(type="pip", name="example")
    assert result[1] == PackageURL(type="maven", namespace="com.example", name="example")

    args_invalid = Namespace(packages_ignore="invalid_package")
    with pytest.raises(ValueError, match="Invalid package URL"):
        _parse_packages_ignore(args_invalid)

def test_parse_packages_scores_thresholds():
    thresholds = "source_commit_frequency:A,binary_release_recency:B"
    result = _parse_packages_scores_thresholds(thresholds)
    assert len(result) == 2
    assert result[MaintenanceMetricSlug("source_commit_frequency")] == MaintenanceMetricScore("A")
    assert result[MaintenanceMetricSlug("binary_release_recency")] == MaintenanceMetricScore("B")

    thresholds_invalid = "invalid:"
    with pytest.raises(ValueError, match="Both key and value must be non-empty"):
        _parse_packages_scores_thresholds(thresholds_invalid)

def test_parse_action_arguments():
    args = Namespace(
        github_repository="owner/repo",
        github_token="token",
        packages_ignore="pkg:pip/example\npkg:maven/com.example/example",
        packages_scores_thresholds="source_commit_frequency:A,binary_release_recency:B",
    )
    result = parse_action_arguments(args)
    assert result.github_repository_owner == "owner"
    assert result.github_repository_name == "repo"
    assert len(result.packages_ignore) == 2
    assert result.packages_scores_thresholds[MaintenanceMetricSlug("source_commit_frequency")] == MaintenanceMetricScore("A")
