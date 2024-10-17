import shutil
import pytest
import subprocess
import os

from tests.conftest import folder_exits, folder_empty
from utils.git_helpers import is_repo_on_branch, is_repo_at_tag, get_branch_list
from utils.output import RowConfiguration, TriageFile, Output, Row


@pytest.fixture(scope="class", autouse=True)
def generate_completed_triage_file(request):
    # Class-level setup: Run the tool to generate the output
    output_file = 'test_output.csv'
    destination_folder = 'repos-test'
    access_token = os.environ.get('TEST_GITHUB_ACCESS_TOKEN', None)

    if not access_token:
        raise ValueError("Please set the TEST_GITHUB_ACCESS_TOKEN environment variable.")

    # Delete output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Delete repo folder if it exists
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)

    row_config = RowConfiguration()
    triage_file = Output(row_config, output_file)

    # Build the triage file using columns used in the pull mode
    row = Row(row_config)
    row.name = "codetriage_empty"
    row.owner = "NullMode"
    row.pull = "Y"
    row.pull_branch_tag = ""
    row.clone_url = "https://github.com/NullMode/codetriage_empty.git"
    row.default_branch = ""
    triage_file.add_row(row)

    row = Row(row_config)
    row.name = "codetriage_archived"
    row.owner = "NullMode"
    row.pull = "Y"
    row.clone_url = "https://github.com/NullMode/codetriage_archived.git"
    row.default_branch = "main"
    triage_file.add_row(row)

    row = Row(row_config)
    row.name = "codetriage_multiple_branches"
    row.owner = "NullMode"
    row.pull = "Y"
    row.pull_branch_tag = "main2"
    row.clone_url = "https://github.com/NullMode/codetriage_multiple_branches.git"
    row.default_branch = "main"
    triage_file.add_row(row)

    row = Row(row_config)
    row.name = "codetriage_tags"
    row.owner = "NullMode"
    row.pull = "Y"
    row.pull_branch_tag = "0.0.1"
    row.clone_url = "https://github.com/NullMode/codetriage_tags.git"
    row.default_branch = "main"
    triage_file.add_row(row)

    row = Row(row_config)
    row.name = "zarp"
    row.owner = "NullMode"
    row.pull = "n"
    row.clone_url = "https://github.com/NullMode/zarp.git"
    row.default_branch = "master"
    triage_file.add_row(row)

    row = Row(row_config)
    row.name = "vim"
    row.owner = "NullMode"
    row.pull = ""
    row.clone_url = "https://github.com/NullMode/vim.git"
    row.default_branch = "master"
    triage_file.add_row(row)

    row = Row(row_config)
    row.name = "codetriage_multiple_branches_2"
    row.owner = "NullMode"
    row.pull = "Y"
    row.pull_branch_tag = "*"
    row.clone_url = "https://github.com/NullMode/codetriage_multiple_branches_2.git"
    row.default_branch = "main"
    triage_file.add_row(row)

    triage_file.write()

    # Command to run the "triage" mode
    command = [
        'python', 'codetriage.py',
        '-m', 'pull',
        '-t', output_file,
        '-d', destination_folder,
        '-a', access_token,
        '-s', 'github'
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    # write output to file
    with open('test_output.txt', 'w') as f:
        f.write(result.stdout)
        f.write(result.stderr)

    # Ensure the tool ran successfully
    assert result.returncode == 0, f"Tool failed to run: {result.stderr}"

    request.cls.destination_folder = destination_folder

    # Teardown: Clean up after the class-level tests
    yield
    if os.path.exists(output_file):
        os.remove(output_file)
        shutil.rmtree(destination_folder)


@pytest.mark.e2e
class TestGitHubTriageOutput:
    def test_empty_repo_pulled(self):
        folder = os.path.join(self.destination_folder, 'codetriage_empty')
        assert folder_exits(folder), "Empty repo not pulled, should pull but have nothing in it"

    def test_archived_repo_pulled_default_branch(self):
        folder = os.path.join(self.destination_folder, 'codetriage_archived')
        assert folder_exits(folder), "Archived repo was not pulled"
        assert is_repo_on_branch(folder, 'main'), "Archived repo was not pulled on the default branch"

    def test_correct_branch_pulled_from_multiple_branch_repo(self):
        folder = os.path.join(self.destination_folder, 'codetriage_multiple_branches')
        assert folder_exits(folder), "Multiple branch repo was not pulled"
        assert is_repo_on_branch(folder, 'main2'), "Incorrect branch pulled for multiple branch repo"

    def test_correct_tag_pulled(self):
        folder = os.path.join(self.destination_folder, 'codetriage_tags')
        assert folder_exits(folder), "Tags repo was not pulled"
        assert is_repo_at_tag(folder, '0.0.1'), "Incorrect tag pulled for tags repo"

    def test_repo_not_pulled_if_pull_is_no(self):
        folder = os.path.join(self.destination_folder, 'zarp')
        assert not folder_exits(folder), "Repo was pulled when it should not have been"

    def test_repo_not_pulled_if_pull_is_blank(self):
        folder = os.path.join(self.destination_folder, 'vim')
        assert not folder_exits(folder), "Repo was pulled when it should not have been"

    def test_all_branches_pulled(self):
        folder = os.path.join(self.destination_folder, 'codetriage_multiple_branches_2')
        assert folder_exits(folder), "Multiple branch repo was not pulled"
        assert get_branch_list(folder) == 3, "Expected 3 branches to be pulled for code triage multiple branches 2"