from release_notes.pull_request import ProdReleasePR
from release_notes.tests.conftest import github_api, fixture_pr_issue


def test_latest_pr_issue():
    prod_release_pr = ProdReleasePR(github_api, fixture_pr_issue)
    pr_num = prod_release_pr.latest_pr_issue
    assert isinstance(pr_num, str)
    assert pr_num.isdigit()
    assert len(pr_num) in range(1, 6)


def test_request_pr_issue():
    prod_release_pr = ProdReleasePR(github_api, fixture_pr_issue)
    pr_issue = prod_release_pr.request_pr_issue()
    assert isinstance(pr_issue, dict)
    assert pr_issue.get("number") == int(fixture_pr_issue)


def test_request_pr_commits():
    prod_release_pr = ProdReleasePR(github_api, fixture_pr_issue)
    pr_commits = list(prod_release_pr.request_pr_commits())
    linked_fixture_prs = sorted(["3", "4"])
    linked_pull_requests = sorted([pr_num for commit_msg, pr_num in pr_commits])

    print(linked_fixture_prs, "\n", linked_pull_requests)
    assert linked_fixture_prs == linked_pull_requests

    for commit_msg, pr_num in pr_commits:
        print(pr_num, "\n", commit_msg)
        assert isinstance(commit_msg, str)
        assert isinstance(pr_num, str)
        assert pr_num.isdigit()
        assert "Merge pull request" in commit_msg
