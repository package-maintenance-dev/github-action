"""
Module containing the function to parse the action arguments into the corresponding typesafe model.
"""

from typing import Optional

import argparse

from action.models.action_arguments import (
    PackageMetricScore,
    PackageMetric,
    ActionArguments,
)


def parse_action_arguments(args: argparse.Namespace) -> ActionArguments:
    github_owner, github_repo = _parse_github_repository(args)
    github_token = args.github_token
    packages_ignore = _parse_packages_ignore(args)
    packages_scores_thresholds = _parse_packages_scores_thresholds(
        args.packages_scores_thresholds
    )

    action_arguments = ActionArguments(
        github_repository_owner=github_owner,
        github_repository_name=github_repo,
        github_token=github_token,
        packages_ignore=packages_ignore,
        packages_scores_thresholds=packages_scores_thresholds,
    )
    return action_arguments


def _parse_github_repository(args: argparse.Namespace) -> tuple[str, str]:
    try:
        owner, repo = map(str.strip, args.github_repository.split("/"))
        if not owner or not repo:
            raise ValueError("Both owner and repo must be non-empty.")
    except ValueError:
        raise ValueError(
            "Invalid format for GitHub repository. It should be in the form 'owner/repo'."
        )
    return owner, repo


def _parse_packages_ignore(args: argparse.Namespace) -> Optional[list[str]]:
    if args.packages_ignore:
        packages_ignore = args.packages_ignore.split("\n")
    else:
        packages_ignore = None
    return packages_ignore


def _parse_packages_scores_thresholds(
    thresholds: Optional[str],
) -> Optional[dict[PackageMetric, PackageMetricScore]]:
    if not thresholds:
        return None

    thresholds_dict = {}
    for entry in thresholds.split(","):
        key, value = map(str.strip, entry.split(":"))
        if not key or not value:
            raise ValueError("Both key and value must be non-empty.")
        sbom_metric = PackageMetric(key.lower())
        sbom_score = PackageMetricScore(value.upper())
        thresholds_dict[sbom_metric] = sbom_score
    return thresholds_dict
