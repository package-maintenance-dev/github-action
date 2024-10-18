import pytest
import sys
from unittest.mock import patch

from action.main import parse_arguments


def test_parse_arguments():
    test_args = [
        'script_name',
        '--github_repository', 'owner/repo',
        '--github_token', 'testtoken',
        '--sbom_ignore_packages', 'pkg1\npkg2\npkg3',
        '--sbom_scores_thresholds', 'source.commit.frequency:B,binary.release.recency:A'
    ]

    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()

        assert args.github_repository == 'owner/repo'
        assert args.github_token == 'testtoken'
        assert args.sbom_ignore_packages == 'pkg1\npkg2\npkg3'
        assert args.sbom_scores_thresholds == 'source.commit.frequency:B,binary.release.recency:A'

def test_missing_required_argument():
    test_args = [
        'script_name'
    ]

    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as exc_info:
            parse_arguments()

        assert exc_info.type == SystemExit

def test_no_ignore_packages():
    test_args = [
        'script_name',
        '--github_repository', 'owner/repo',
        '--github_token', 'testtoken',
        '--sbom_scores_thresholds', 'source.commit.frequency:B,binary.release.recency:A'
    ]

    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()

        assert args.github_repository == 'owner/repo'
        assert args.github_token == 'testtoken'
        assert args.sbom_ignore_packages is None
        assert args.sbom_scores_thresholds == 'source.commit.frequency:B,binary.release.recency:A'

def test_multiline_ignore_packages():
    test_args = [
        'script_name',
        '--github_repository', 'owner/repo',
        '--github_token', 'testtoken',
        '--sbom_ignore_packages', 'pkg1\npkg2\npkg3'
    ]

    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        ignore_packages = args.sbom_ignore_packages.split('\n')

        assert args.github_repository == 'owner/repo'
        assert args.github_token == 'testtoken'
        assert ignore_packages == ['pkg1', 'pkg2', 'pkg3']
        assert args.sbom_scores_thresholds is None
