import git

def is_repo_on_branch(repo_path: str, branch_name: str) -> bool:
    """
    Check if the current branch of the git repository matches the passed-in branch name.

    :param repo_path: Path to the git repository.
    :param branch_name: The branch name to check against the current branch.
    :return: True if the current branch matches, False otherwise.
    """
    try:
        repo = git.Repo(repo_path)
        current_branch = repo.active_branch.name
        return current_branch == branch_name
    except Exception as e:
        print(f"Error checking branch: {e}")
        return False


def is_repo_at_tag(repo_path: str, tag_name: str) -> bool:
    """
    Check if the current commit of the git repository matches the passed-in tag.

    :param repo_path: Path to the git repository.
    :param tag_name: The tag name to check.
    :return: True if the current commit matches the given tag, False otherwise.
    """
    try:
        repo = git.Repo(repo_path)
        # Get the tag object by name
        tag_commit = repo.tags[tag_name].commit
        # Check if the current commit (HEAD) matches the tag's commit
        current_commit = repo.head.commit
        return current_commit == tag_commit
    except Exception as e:
        print(f"Error checking tag: {e}")
        return False


def get_branch_list(repo_path: str) -> int:
    """
    Get the list of branches in a git repository.

    :param repo_path: Path to the git repository.
    :return: The list of branches in the repository.
    """
    try:
        repo = git.Repo(repo_path)
        local_branches = repo.git.branch('--list').splitlines()
        return len(local_branches)
    except Exception as e:
        print(f"Error getting branches: {e}")
        return None