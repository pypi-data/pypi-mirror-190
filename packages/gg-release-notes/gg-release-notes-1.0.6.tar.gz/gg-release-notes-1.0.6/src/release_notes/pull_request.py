import re
from typing import Optional, Generator

from ghapi.all import GhApi

from release_notes.config.github_config import GithubAPIConfig


class ProdReleasePR:
    def __init__(
        self, github_configuration: GithubAPIConfig, issue_num: Optional[str] = None
    ):
        """

        Args:
            github_configuration (GithubAPIConfig): Configuration for Github API
            issue_num (Optional[str]): Number of the PR to get data from. Defaults to None.
        """
        self.github_configuration = github_configuration
        self.github_api: GhApi = github_configuration.github_api

        if issue_num:
            self.issue_num = issue_num
        else:
            self.issue_num = self.latest_pr_issue

    @property
    def latest_pr_issue(self) -> str:
        print("Searching for most recent PR...")
        prs = [
            pr
            for pr in self.github_api.pulls.list(
                state="all", per_page=100, sort="updated", direction="desc"
            )
            if self.github_configuration.github_prod_release_label
            in [label.get("name") for label in pr.get("labels")]
        ]
        if prs:
            newest_pr = str(prs[0].get("number"))
            print(f"Latest PR issue number: {newest_pr}")
            return newest_pr
        else:
            raise Exception("No PRs found.")

    def request_pr_issue(self) -> dict:
        """Helper function to get issue data from a PR."""
        return self.github_api.issues.get(self.issue_num)

    def issue_body(self):
        return str(self.request_pr_issue().get("body", "SENTINEL_STRING"))

    def request_pr_commits(self, max_range: int = 100) -> Generator:
        """Helper function to get commits from a PR.

        Args:
            max_range (int): max range of pages to get commits from. Defaults to 100.

        Yields:
            Generator:containing tuples of commit message and pr number
        """
        print(f"Getting commits from PR: {self.issue_num}")
        for i in range(1, max_range):
            listed_commits = list(
                self.github_api.pulls.list_commits(
                    pull_number=self.issue_num, page=i, sort="updated", direction="desc"
                )
            )
            if listed_commits:
                for commit in listed_commits:
                    commit_msg = commit["commit"].get("message", "")
                    if commit_msg and "Merge pull request" in commit_msg:
                        pr_num = re.findall("\d\d?\d?\d?\d?", commit_msg)
                        commit_msg = commit_msg.replace("\n", " ")
                        if pr_num:
                            yield commit_msg, pr_num[0].strip(" ")
            else:
                break
        print("Done getting commits from PR.")
