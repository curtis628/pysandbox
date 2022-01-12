import argparse
import logging
from dataclasses import dataclass
from typing import Any, Optional

import requests

import pysandbox.common as common

"""Pulls commit details from GitHub APIs"""

logger = logging.getLogger(__name__)

GIT_BASE_URL = "https://api.github.com"
DEFAULT_PER_PAGE: int = 10
DEFAULT_COMMIT_NUM: int = 10
DEFAULT_OWNER: str = "psf"
DEFAULT_REPO: str = "requests"


@dataclass(frozen=True)
class Commit:
    sha: str
    author: str
    commit_date: str
    message: str

    def __str__(self) -> str:
        msg = self.message.split("\n", maxsplit=1)[0]  # Remove newline
        return f"Commit: sha={self.sha} author={self.author:30} commit_date={self.commit_date} message={msg[0:30]}..."


def parse_commit(api_body: Any) -> Commit:
    return Commit(
        api_body["sha"][0:6],
        api_body["commit"]["author"]["email"],
        api_body["commit"]["committer"]["date"],
        api_body["commit"]["message"],
    )


def pull_commits(owner: str, repo: str, num_commits: int = DEFAULT_COMMIT_NUM) -> list[Commit]:
    logger.debug(f"Pulling {num_commits} commits from {owner}/{repo}")
    next_link: Optional[str] = f"{GIT_BASE_URL}/repos/{owner}/{repo}/commits?per_page={num_commits}"
    commits_list: list[Commit] = []

    while len(commits_list) < num_commits and next_link is not None:
        logger.debug(f"Making request for: {next_link}")
        r = requests.get(next_link)
        r.raise_for_status()
        r_body = r.json()
        logger.debug(f"  Received response: {r}")

        link_header = r.headers["Link"]
        next_link = None
        for link in link_header.split(","):
            if 'rel="next"' in link:
                first_part = link.split(";")[0]
                next_link = first_part.replace("<", "").replace(">", "")
                break
        logger.debug(f"  Found {len(r_body)} commits with {next_link=} from {link_header=}")

        for commit in r_body:
            commits_list.append(parse_commit(commit))
            if len(commits_list) == num_commits:
                break

    logger.info(f"Returning {len(commits_list)} commits.")
    return commits_list


def main() -> None:
    parser = argparse.ArgumentParser("Pulls commits from GitHub API")
    parser.add_argument(
        "--commits",
        type=int,
        default=DEFAULT_COMMIT_NUM,
        help=f"The number of commits to return. Default: {DEFAULT_COMMIT_NUM}",
    )

    parser.add_argument(
        "--owner",
        default=DEFAULT_OWNER,
        help=f"The GitHub 'owner'. Default: {DEFAULT_OWNER}",
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"The GitHub 'repo'. Default: {DEFAULT_REPO}",
    )

    args = parser.parse_args()
    commit_details = pull_commits(args.owner, args.repo, args.commits)
    for detail in commit_details:
        print(f"{detail}")


if __name__ == "__main__":
    common.initialize_logging_from_file()
    main()
