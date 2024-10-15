import csv
import pytest
import subprocess
import os


@pytest.fixture(scope="class", autouse=True)
def run_triage_tool_once_and_get_output(request):
    # Class-level setup: Run the tool to generate the output
    output_file = 'test_output.csv'
    user = 'NullMode'
    access_token = os.environ.get('TEST_GITHUB_ACCESS_TOKEN', None)

    if not access_token:
        raise ValueError("Please set the TEST_GITHUB_ACCESS_TOKEN environment variable.")

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

    # Load the content of the output csv file using csv.reader
    with open(output_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        output_content = list(csv_reader)

    # Attach the output content to the class so it can be used by test methods
    request.cls.output_file = output_file
    request.cls.output_content = output_content

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
        repo_names = [row[0] for row in self.output_content[1:]]
        for repo in self.expected_repos:
            assert repo in repo_names, f"Repo '{repo}' not found in output"

    def test_owner_is_nullmode(self):
        # Test to see if each repo is owned by NullMode
        for row in self.output_content[1:]:
            assert row[1] == 'NullMode', f"Repo '{row[0]}' is not owned by NullMode"

    def test_pull_yn_is_blank(self):
        # Test to see if the pull column is blank
        for row in self.output_content[1:]:
            assert row[2] == '', f"Pull column is not blank for repo '{row[0]}'"

    def test_pull_branch_tag_is_blank(self):
        # Test to see if the pull branch/tag column is blank
        for row in self.output_content[1:]:
            assert row[3] == '', f"Pull branch/tag column is not blank for repo '{row[0]}'"

    def test_notes_is_blank(self):
        # Test to see if the notes column is blank
        for row in self.output_content[1:]:
            assert row[4] == '', f"Notes column is not blank for repo '{row[0]}'"

    def test_empty_is_boolean(self):
        # Test to see if the empty column is a boolean
        for row in self.output_content[1:]:
            assert row[5] in {'True', 'False'}, f"Empty column is not a boolean for repo '{row[0]}'"

    def test_archived_is_boolean(self):
        # Test to see if the archived column is a boolean
        for row in self.output_content[1:]:
            assert row[6] in {'True', 'False'}, f"Archived column is not a boolean for repo '{row[0]}'"

    def test_fork_is_boolean(self):
        # Test to see if the fork column is a boolean
        for row in self.output_content[1:]:
            assert row[7] in {'True', 'False'}, f"Fork column is not a boolean for repo '{row[0]}'"

    # Description can be blank, so no need to test

    def test_forks_count_is_integer(self):
        # Test to see if the forks count column is an integer
        for row in self.output_content[1:]:
            try:
                int(row[9])
            except ValueError:
                assert False, f"Forks count column is not an integer for repo '{row[0]}'"

    def test_open_issues_count_is_integer(self):
        # Test to see if the open issues count column is an integer
        for row in self.output_content[1:]:
            try:
                int(row[10])
            except ValueError:
                assert False, f"Open issues count column is not an integer for repo '{row[0]}'"

    def test_updated_at_is_datetime(self):
        # Test to see if the updated at column is a datetime
        for row in self.output_content[1:]:
            try:
                int(row[11])
            except ValueError:
                assert False, f"Updated at column is not a datetime for repo '{row[0]}'"

    def test_url_is_string_and_not_null(self):
        # Test to see if the URL column is a string
        for row in self.output_content[1:]:
            assert isinstance(row[12], str), f"URL column is not a string for repo '{row[0]}'"
            assert row[12], f"URL column is null for repo '{row[0]}'"

    def test_clone_url_is_string_and_not_null(self):
        # Test to see if the clone URL column is a string
        for row in self.output_content[1:]:
            assert isinstance(row[13], str), f"Clone URL column is not a string for repo '{row[0]}'"
            assert row[13], f"Clone URL column is null for repo '{row[0]}'"

    def test_default_branch_is_string_and_not_null(self):
        # Test to see if the default branch column is a string and not null
        for row in self.output_content[1:]:
            assert isinstance(row[14], str), f"Default branch column is not a string for repo '{row[0]}'"
            assert row[14], f"Default branch column is null for repo '{row[0]}'"

    def test_branch_list_is_string_and_not_null(self):  # Unless the repo is empty
        # Test to see if the branch list column is a string and not null
        for row in self.output_content[1:]:
            if row[5] == 'True':
                continue
            assert isinstance(row[15], str), f"Branch list column is not a string for repo '{row[0]}'"

    # Repo specific tests

    def test_codetriage_empty_is_marked_empty(self):
        # Test to see if the codetriage_empty repo is marked as empty
        for row in self.output_content[1:]:
            if row[0] == "codetriage_empty":
                print(row)
                assert row[5] == 'True', "codetriage_empty repo not marked as empty"

    def test_vim_has_been_forked(self):
        # Test to see if the vim repo has been forked a number of times
        for row in self.output_content[1:]:
            if row[0] == "vim":
                assert int(row[9]) > 0, "vim repo has not been forked"

    def test_codetriage_archived_is_marked_archived(self):
        # Test to see if the codetriage_archived repo is marked as archived
        for row in self.output_content[1:]:
            if row[0] == "codetriage_archived":
                assert row[6] == 'True', "codetriage_archived repo not marked as archived"

    def test_zarp_is_a_fork(self):
        # Test to see if the zarp repo is marked as a fork
        for row in self.output_content[1:]:
            if row[0] == "zarp":
                assert row[7] == 'True', "zarp repo not marked as a fork"

    def test_codetriage_open_issues_has_open_issues(self):
        # Test to see if the codetriage_open_issues repo has open issues
        for row in self.output_content[1:]:
            if row[0] == "codetriage_open_issues":
                assert int(row[10]) > 0, "codetriage_open_issues repo has no open issues"

    def test_codetriage_multiple_branches_has_multiple_branches(self):
        # Test to see if the codetriage_multiple_branches repo has multiple branches
        for row in self.output_content[1:]:
            if row[0] == "codetriage_multiple_branches":
                assert ',' in row[15], "codetriage_multiple_branches repo has only one branch"

    def test_codetriage_tags_has_tags(self):
        # Test to see if the codetriage_tags repo has tags
        for row in self.output_content[1:]:
            if row[0] == "codetriage_tags":
                assert int(row[16]) > 0, "codetriage_tags repo has no tags"

    def test_codetriage_tags_has_latest_tag(self):
        # Test to see if the codetriage_tags repo has a latest tag
        for row in self.output_content[1:]:
            if row[0] == "codetriage_tags":
                assert row[17] == '0.0.2', "codetriage_tags repo has no latest tag marked 0.0.2"
