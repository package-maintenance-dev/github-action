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


def main():
    args = parse_arguments()

    if args.sbom_ignore_packages:
        sbom_ignore_packages = args.sbom_ignore_packages.split("\n")
    else:
        sbom_ignore_packages = None

    print("GitHub Repository:", args.github_repository)
    print("GitHub Token:", args.github_token)
    print("SBOM Ignore Packages:", sbom_ignore_packages)
    print("SBOM Scores Thresholds:", args.sbom_scores_thresholds)


if __name__ == "__main__":
    main()
