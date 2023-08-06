from release_notes.pull_request import ProdReleasePR

from release_notes.version import ReleaseVersion
from release_notes.config.github_config import GithubAPIConfig
from release_notes.config.env_config import EnvConfig
from release_notes.config.prompt_config import PromptConfig


# Configurations
test_env_config = EnvConfig(".env.test")
github_api = GithubAPIConfig("DataWiz40", "gg-release-example", test_env_config)
prompt_config = PromptConfig(github_api)

# Version
version = ReleaseVersion(github_api)

# Pull Request
fixture_pr_issue = "5"
prod_release_pr = ProdReleasePR(github_api, fixture_pr_issue)
