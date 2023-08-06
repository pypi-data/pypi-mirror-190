import datetime

from release_notes.version import ReleaseVersion
from release_notes.config.github_config import GithubAPIConfig


class PromptConfig:
    """Prompt configuration used for the GPT generation"""

    def __init__(self, github_config: GithubAPIConfig):
        """

        Args:
            github_config (GithubAPIConfig): Github configuration
        """
        self.github_config = github_config
        self.release_version = ReleaseVersion(github_config)

    @property
    def prompt_internal_release(self):
        """Prompt for the internal release notes"""
        return f"""
                Write release notes for internal use in {self.github_config.owner} for the repository {self.github_config.repository}.
                Use the PR numbers to generate hrefs to the PR's in the github release notes. Make a bullet point for each PR.
                Leave out any introductions, and only write about the changes.
                for the following issue titles:
                """

    @property
    def prompt_client_release(self):
        """Prompt for the client release notes"""
        return f"""
                Write release notes as a user story for clients of {self.github_config.owner} for the repository {self.github_config.repository}. The release notes need to be appriopriate for an in-app changelog and LinkedIn post. 
                Leave out any introductions, and only write about the changes.
                Write the release notes descriptive, and add relevant information if something is not specific enough.
                Leave out anything that is not relevant for a client of {self.github_config.owner}.
                Write about the following issue titles:
                """

    @property
    def release_notes_end_text(self):
        """End of the release notes, which will be added to the generated release notes"""
        return f"""
        \n\nIncludes the following PR's:\n"""

    @property
    def solved_issues(self):
        """Solved issues, which will be added to the generated release notes"""
        return f"""
        \n\nSolved issues:\n"""

    @property
    def prompt_config(self):
        """Determines which prompt to use for the openai API"""
        return {
            "client_release": self.prompt_client_release,
            "internal_release": self.prompt_internal_release,
        }
