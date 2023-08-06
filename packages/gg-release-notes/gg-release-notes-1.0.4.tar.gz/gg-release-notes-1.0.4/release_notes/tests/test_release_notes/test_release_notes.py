from release_notes.generate_release_notes import ReleaseNotes
from release_notes.tests.conftest import (
    test_env_config,
    github_api,
    prompt_config,
    prod_release_pr,
)


def test_create_prompt_batches():
    github_release = ReleaseNotes(test_env_config, github_api, prod_release_pr, token_limit=1300)
    batch_size = 10
    expected_batches = 1
    batched_prompt, prompt_issues_descriptions = github_release._create_prompt_batches(
        batch_size
    )

    assert len(batched_prompt) == expected_batches
    assert len(batched_prompt[0]) <= batch_size

    print("Batched prompt: ", batched_prompt)
    print("Issue descriptions: ", prompt_issues_descriptions)


def test_create_release_notes():
    github_release = ReleaseNotes(test_env_config, prompt_config, prod_release_pr, token_limit=1300)
    release = github_release.create_release_notes()
    assert isinstance(release, dict)

    for key in ("internal_release", "client_release"):
        print("\n", key.replace("_", " "), ":\n")
        print("Prompt:\n", release.get(key).get("prompt"))
        print("Response:\n", release.get(key).get("response"))

        assert key in release.keys()
        assert isinstance(release.get(key).get("response"), str)
        assert (
            len(release.get(key).get("response"))
            > 200
        )
