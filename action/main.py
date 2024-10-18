import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process SBOM and GitHub repository data."
    )

    parser.add_argument(
        "--github_repository",
        type=str,
        required=True,
        help="GitHub repository in the form of owner/repo.",
    )
    parser.add_argument(
        "--github_token",
        type=str,
        help="GitHub token for authentication. Default is None.",
    )
    parser.add_argument(
        "--sbom_ignore_packages",
        type=str,
        help="Multiline string of packages to ignore, split by new lines.",
    )
    parser.add_argument(
        "--sbom_scores_thresholds",
        type=str,
        help="SBOM scores thresholds in string format. Default is None.",
    )

    return parser.parse_args()


def parse_sbom_scores_thresholds(thresholds_str):
    thresholds_dict = {}
    for entry in thresholds_str.split(","):
        key, value = map(str.strip, entry.split(":"))
        if not key or not value:
            raise ValueError("Both key and value must be non-empty.")
        thresholds_dict[key] = value.upper()
    return thresholds_dict


def main():
    args = parse_arguments()

    try:
        owner, repo = map(str.strip, args.github_repository.split("/"))
        if not owner or not repo:
            raise ValueError("Both owner and repo must be non-empty.")
    except ValueError:
        raise ValueError(
            "Invalid format for GitHub repository. It should be in the form 'owner/repo'."
        )

    if args.sbom_ignore_packages:
        sbom_ignore_packages = args.sbom_ignore_packages.split("\n")
    else:
        sbom_ignore_packages = None

    if args.sbom_scores_thresholds:
        sbom_scores_thresholds = parse_sbom_scores_thresholds(
            args.sbom_scores_thresholds
        )
    else:
        sbom_scores_thresholds = None

    print("GitHub Repository Owner:", owner)
    print("GitHub Repository Name:", repo)
    print("GitHub Token:", args.github_token)
    print("SBOM Ignore Packages:", sbom_ignore_packages)
    print("SBOM Scores Thresholds:", sbom_scores_thresholds)


if __name__ == "__main__":
    main()
