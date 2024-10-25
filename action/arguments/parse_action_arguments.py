"""
Module containing the function to parse the action arguments into the corresponding typesafe model.
"""

import os
from typing import Optional

import argparse
from packageurl import PackageURL

from action.arguments.action_arguments import (
    PackageMetricScore,
    PackageMetric,
    ActionArguments,
    default_packages_scores_thresholds,
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
    github_repository = args.github_repository or os.environ["GITHUB_REPOSITORY"]
    try:
        owner, repo = map(str.strip, github_repository.split("/"))
        if not owner or not repo:
            raise ValueError("Both owner and repo must be non-empty.")
    except ValueError:
        raise ValueError(
            "Invalid format for GitHub repository. It should be in the form 'owner/repo'."
        )
    return owner, repo


def _parse_packages_ignore(args: argparse.Namespace) -> list[PackageURL]:
    if args.packages_ignore is None:
        return []

    packages_ignore = []
    for package in args.packages_ignore.split("\n"):
        package = package.strip()
        if not package:
            continue
        try:
            packages_ignore.append(PackageURL.from_string(package))
        except ValueError:
            raise ValueError(f"Invalid package URL: {package}")

    return packages_ignore


def _parse_packages_scores_thresholds(
    thresholds: Optional[str],
) -> dict[PackageMetric, PackageMetricScore]:
    if not thresholds:
        return default_packages_scores_thresholds()

    thresholds_dict = {}
    for entry in thresholds.split(","):
        key, value = map(str.strip, entry.split(":"))
        if not key or not value:
            raise ValueError("Both key and value must be non-empty.")
        sbom_metric = PackageMetric(key.lower())
        sbom_score = PackageMetricScore(value.upper())
        thresholds_dict[sbom_metric] = sbom_score
    return thresholds_dict
