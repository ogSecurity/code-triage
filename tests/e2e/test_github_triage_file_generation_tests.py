import pytest
import subprocess
import os

from utils.output import RowConfiguration, TriageFile, Output


@pytest.fixture(scope="class", autouse=True)
def run_triage_tool_once_and_get_output(request):
    # Class-level setup: Run the tool to generate the output
    output_file = 'test_output.csv'
    user = 'NullMode'
    access_token = os.environ.get('TEST_GITHUB_ACCESS_TOKEN', None)

    if not access_token:
        raise ValueError("Please set the TEST_GITHUB_ACCESS_TOKEN environment variable.")

    # Delete output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Command to run the "triage" mode
    command = [
        'python', 'codetriage.py',
        '-m', 'triage',
        '-u', user,
        '-o', output_file,
        '-a', access_token,
        '-s', 'github'
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    # Ensure the tool ran successfully
    assert result.returncode == 0, f"Tool failed to run: {result.stderr}"

    # Make sure the output file exists
    assert os.path.exists(output_file), f"{output_file} not created."

    # Attach the output content to the class so it can be used by test methods
    request.cls.output_file = output_file
    request.cls.row_config = RowConfiguration()
    request.cls.triage_file = TriageFile(output_file, request.cls.row_config)

    # Teardown: Clean up after the class-level tests
    yield
    if os.path.exists(output_file):
        os.remove(output_file)


@pytest.mark.e2e
class TestGitHubTriageOutput:
    expected_repos = [
        "codetriage_empty",  # Empty repo
        "vim",  # Has been forked
        "codetriage_archived",  # Archived repo
        "zarp",  # Is a fork
        "codetriage_open_issues",  # Has open issues
        "codetriage_multiple_branches",  # Has multiple branches
        "codetriage_tags"  # Has tags
    ]

    # General tests

    def test_contains_expected_repo_names(self):
        # Test to see if each repo is in the output
        repo_names = [row.name for row in self.triage_file.get_data()]
        for repo in self.expected_repos:
            assert repo in repo_names, f"Repo '{repo}' not found in output"

    def test_owner_is_nullmode(self):
        # Test to see if each repo is owned by NullMode
        for row in self.triage_file.get_data():
            assert row.owner == 'NullMode', f"Repo '{row.name}' is not owned by NullMode"

    def test_pull_yn_is_blank(self):
        # Test to see if the pull column is blank
        for row in self.triage_file.get_data():
            assert row.pull == '', f"Pull column is blank for repo '{row.name}'"

    def test_pull_branch_tag_is_blank(self):
        # Test to see if the pull branch/tag column is blank
        for row in self.triage_file.get_data():
            assert row.pull_branch_tag == '', f"Pull branch/tag column is blank for repo '{row.name}'"

    def test_notes_is_blank(self):
        # Test to see if the notes column is blank
        for row in self.triage_file.get_data():
            assert row.notes == '', f"Notes column is blank for repo '{row.name}'"

    def test_empty_is_boolean(self):
        # Test to see if the empty column is a boolean
        for row in self.triage_file.get_data():
            assert row.empty in [True, False], f"Empty column is not a boolean for repo '{row.name}'"

    def test_archived_is_boolean(self):
        # Test to see if the archived column is a boolean
        for row in self.triage_file.get_data():
            assert row.archived in [True, False], f"Archived column is not a boolean for repo '{row.name}'"

    def test_fork_is_boolean_str(self):
        # Test to see if the fork column is a boolean
        for row in self.triage_file.get_data():
            assert row.fork in [True, False], f"Fork column is not a boolean str for repo '{row.name}'"

    # Description can be blank, so no need to test

    def test_forks_count_is_integer(self):
        # Test to see if the forks count column is an integer
        for row in self.triage_file.get_data():
            try:
                int(row.forks)
            except ValueError:
                assert False, f"Forks count column is not an integer for repo '{row.name}'"

    def test_open_issues_count_is_integer(self):
        # Test to see if the open issues count column is an integer
        for row in self.triage_file.get_data():
            try:
                int(row.open_issues)
            except ValueError:
                assert False, f"Open issues count column is not an integer for repo '{row.name}'"

    def test_updated_at_is_not_null(self):
        # Test to see if the updated at column is a datetime
        for row in self.triage_file.get_data():
            assert row.last_updated, f"Last updated column is null for repo '{row.name}'"

    def test_url_is_string_and_not_null(self):
        # Test to see if the URL column is a string
        for row in self.triage_file.get_data():
            assert isinstance(row.url, str), f"URL column is not a string for repo '{row.name}'"
            assert row.url, f"URL column is null for repo '{row.name}'"

    def test_clone_url_is_string_and_not_null(self):
        # Test to see if the clone URL column is a string
        for row in self.triage_file.get_data():
            assert isinstance(row.clone_url, str), f"Clone URL column is not a string for repo '{row.name}'"
            assert row.clone_url, f"Clone URL column is null for repo '{row.name}'"

    def test_default_branch_is_string_and_not_null(self):
        # Test to see if the default branch column is a string and not null
        for row in self.triage_file.get_data():
            assert isinstance(row.default_branch, str), f"Default branch column is not a string for repo '{row.name}'"
            assert row.default_branch != '', f"Default branch column is null for repo '{row.name}'"

    def test_branch_list_is_not_null(self):  # Unless the repo is empty
        # Test to see if the branch list column is not null
        for row in self.triage_file.get_data():
            if row.name:
                continue # Skip the empty repo
            assert row.branch_list != '', f"Branch list column is null for repo '{row.name}'"


    # Repo specific tests

    def test_codetriage_empty_is_marked_empty(self):
        # Test to see if the codetriage_empty repo is marked as empty
        for row in self.triage_file.get_data():
            if row.name == "codetriage_empty":
                assert row.empty is True, "codetriage_empty repo not marked as empty"

    def test_vim_has_been_forked(self):
        # Test to see if the vim repo has been forked a number of times
        for row in self.triage_file.get_data():
            if row.name == "vim":
                assert int(row.forks) > 0, "vim repo has not been forked"

    def test_codetriage_archived_is_marked_archived(self):
        # Test to see if the codetriage_archived repo is marked as archived
        for row in self.triage_file.get_data():
            if row.name == "codetriage_archived":
                assert row.archived is True, "codetriage_archived repo not marked as archived"

    def test_codetriage_archived_has_no_open_issues(self):
        # Test to see if the codetriage_archived repo has no open issues
        for row in self.triage_file.get_data():
            if row.name == "codetriage_archived":
                assert row.open_issues == 0, "codetriage_archived repo has open issues"

    def test_codetriage_archived_has_no_tags(self):
        # Test to see if the codetriage_archived repo has no tags
        for row in self.triage_file.get_data():
            if row.name == "codetriage_archived":
                assert row.tags == 0, "codetriage_archived repo has tags"
                assert row.latest_tag == '', "codetriage_archived repo has a latest tag"

    def test_zarp_is_a_fork(self):
        # Test to see if the zarp repo is marked as a fork
        for row in self.triage_file.get_data():
            if row.name == "zarp":
                assert row.fork is True, "zarp repo not marked as a fork"

    def test_codetriage_open_issues_has_open_issues(self):
        # Test to see if the codetriage_open_issues repo has open issues
        for row in self.triage_file.get_data():
            if row.name == "codetriage_open_issues":
                assert int(row.open_issues) > 0, "codetriage_open_issues repo has no open issues"

    def test_codetriage_multiple_branches_has_multiple_branches(self):
        # Test to see if the codetriage_multiple_branches repo has multiple branches
        for row in self.triage_file.get_data():
            if row.name == "codetriage_multiple_branches":
                assert ',' in row.branch_list, "codetriage_multiple_branches repo has only one branch"

    def test_codetriage_tags_has_tags(self):
        # Test to see if the codetriage_tags repo has tags
        for row in self.triage_file.get_data():
            if row.name == "codetriage_tags":
                assert int(row.tags) > 0, "codetriage_tags repo has no tags"

    def test_codetriage_tags_has_latest_tag(self):
        # Test to see if the codetriage_tags repo has a latest tag
        for row in self.triage_file.get_data():
            if row.name == "codetriage_tags":
                assert row.latest_tag == '0.0.2', "codetriage_tags repo has no latest tag marked 0.0.2"
