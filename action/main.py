import argparse

from action.action import perform_action


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
        "--packages_ignore",
        type=str,
        help="Multiline string of packages to ignore, split by new lines.",
    )
    parser.add_argument(
        "--packages_scores_thresholds",
        type=str,
        help="SBOM scores thresholds in string format. Default is None.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    perform_action(args)


if __name__ == "__main__":
    main()
