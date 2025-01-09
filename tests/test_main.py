import pytest
import sys
from unittest.mock import patch

from main import parse_arguments
from src.arguments.action_arguments import MaintenanceMetricSlug, MaintenanceMetricScore
from src.arguments.parse_action_arguments import _parse_packages_scores_thresholds


def test_parse_packages_scores_thresholds():
    thresholds_str = 'source_commit_frequency:B,binary_release_recency:A'
    expected_dict = {
        MaintenanceMetricSlug.source_commit_frequency: MaintenanceMetricScore.B,
        MaintenanceMetricSlug.binary_release_recency: MaintenanceMetricScore.A
    }
    result = _parse_packages_scores_thresholds(thresholds_str)
    assert result == expected_dict


def test_invalid_packages_scores_thresholds():
    with pytest.raises(ValueError, match="Both key and value must be non-empty."):
        _parse_packages_scores_thresholds('source_commit_frequency:,binary_release_recency:A')


def test_parse_arguments():
    test_args = [
        'script_name',
        '--github_repository', 'owner/repo',
        '--github_token', 'testtoken',
        '--packages_ignore', 'pkg1\npkg2\npkg3',
        '--packages_scores_thresholds', 'source_commit_frequency:B,binary_release_recency:A'
    ]

    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        owner, repo = args.github_repository.split('/')
        assert owner.strip() == 'owner'
        assert repo.strip() == 'repo'
        assert args.github_token == 'testtoken'
        assert args.packages_ignore == 'pkg1\npkg2\npkg3'
        packages_scores_thresholds = _parse_packages_scores_thresholds(args.packages_scores_thresholds)
        assert packages_scores_thresholds == {
            MaintenanceMetricSlug.source_commit_frequency: MaintenanceMetricScore.B,
            MaintenanceMetricSlug.binary_release_recency: MaintenanceMetricScore.A
        }


def test_no_ignore_packages():
    test_args = [
        'script_name',
        '--github_repository', 'owner/repo',
        '--github_token', 'testtoken',
        '--packages_scores_thresholds', 'source_commit_frequency:B,binary_release_recency:A'
    ]

    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()

        owner, repo = args.github_repository.split('/')
        assert owner.strip() == 'owner'
        assert repo.strip() == 'repo'
        assert args.github_token == 'testtoken'
        assert args.packages_ignore is None
        packages_scores_thresholds = _parse_packages_scores_thresholds(args.packages_scores_thresholds)
        assert packages_scores_thresholds == {
            MaintenanceMetricSlug.source_commit_frequency: MaintenanceMetricScore.B,
            MaintenanceMetricSlug.binary_release_recency: MaintenanceMetricScore.A
        }


def test_multiline_ignore_packages():
    test_args = [
        'script_name',
        '--github_repository', 'owner/repo',
        '--github_token', 'testtoken',
        '--packages_ignore', 'pkg1\npkg2\npkg3'
    ]

    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        ignore_packages = args.packages_ignore.split('\n')

        owner, repo = args.github_repository.split('/')
        assert owner.strip() == 'owner'
        assert repo.strip() == 'repo'
        assert ignore_packages == ['pkg1', 'pkg2', 'pkg3']
        assert args.packages_scores_thresholds is None
