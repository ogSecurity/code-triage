from .scm import SCM, Repository, Branch, Tag
from github import Auth
from github import Github as gh
from github.GithubException import GithubException
from sys import exit
from pygit2 import GitError

import shutil
import os
import logging
import pygit2

logging.basicConfig(level=logging.INFO)

class Github(SCM):
    def __init__(self):
        super().__init__()
        self._scm = 'github'

    @staticmethod
    def authentication_options() -> list:
        return [{'access_token': ['access_token']}]

    def authenticate(self):
        if not self.auth_configuration:
            logging.error("No authentication configuration provided.")
            exit(1)

        if 'access_token' in self.auth_configuration:
            self.client = gh(auth=Auth.Token(self.auth_configuration['access_token']))

    def get_repos(self, user):
        repos = self.client.get_user(user).get_repos()
        return_repos = []

        count = 1
        for repo in repos:
            logging.info(f"Processing repo: {repo.name}...({count}/{repos.totalCount})")
            logging.info(f"Gathering branch information for {repo.name}...")
            tmp_branches = repo.get_branches()
            logging.info(f"Gathering tag information for {repo.name}...")
            tag_count, latest_tag, tags = self.get_tags_info(repo)
            branches = []
            for branch in tmp_branches:
                branches.append(Branch(branch.name))

            return_repos.append(
                Repository(repo.name,
                           repo.owner.login,
                           repo.default_branch,
                           branches,
                           self.is_repo_empty(repo),
                           repo.archived,
                           repo.fork,
                           str(repo.description),  # Description can be None, force to string
                           repo.forks_count,
                           self.get_str_datetime(repo.updated_at),
                           repo.html_url,
                           repo.clone_url,
                           tag_count,
                           latest_tag,
                           tags,
                           repo.open_issues_count
               )
            )
            count += 1
        return return_repos

    def is_repo_empty(self, repo):
        try:
            # Check if the repository size is zero
            if repo.size == 0:
                return True
            # Check if the repository has any branches
            branches = repo.get_branches()
            if branches.totalCount == 0:
                return True
            # If the repository has branches, check if it has any commits
            if repo.get_commits().totalCount == 0:
                return True
            return False
        except GithubException as e:
            print(f"An error occurred: {e}")
            return False

    def get_repo_tags(self, repo):
        return repo.get_tags()

    def get_repo_branches(self, repo):
        return repo.get_branches()

    def get_tags_info(self, repo):
        count = 0
        latest_tag = ""
        all_tags = []
        try:
            tags = repo.get_tags()
            count = tags.totalCount
            if count > 0:
                latest_tag = tags[0].name
                all_tags = [Tag(tag.name) for tag in tags]
        except GithubException as e:
            logging.error(f"An error getting tags for {repo.name}: {e}")
            return count, latest_tag, all_tags
        return count, latest_tag, all_tags

    def get_triage_data(self):
        repo_list = []
        for repo in self.client.get_user().get_repos():
            yield repo

        return repo_list

    def pull_repo(self, owner, repo_name, clone_url, branch, destination_folder):
        try:
            # Checkout all branches
            if branch == '*':
                repo_path = os.path.join(destination_folder, repo_name)
                repo = pygit2.clone_repository(clone_url, repo_path)
                remote = repo.remotes['origin']
                remote.fetch()

                for branch_name in repo.listall_references():
                    try:
                        if branch_name.startswith('refs/remotes/origin/'):
                            branch = branch_name.replace('refs/remotes/origin/', '')
                            if branch not in repo.branches.local:
                                repo.create_branch(branch, repo.revparse_single(branch_name))
                    except KeyError as e:
                        if "reference 'refs/remotes/" in str(e) and "' not found" in str(e):
                            logging.error(f"No branches found for {repo_name}, skipping")
                            continue
                    except GitError as e:
                        if "'HEAD' is not a valid branch name" in str(e):
                            continue
                        logging.error(f"An error occurred cloning {repo_name}: {e}")
                        exit(1)
            else:
                repo_path = os.path.join(destination_folder, repo_name)
                try:
                    pygit2.clone_repository(clone_url, repo_path, checkout_branch=branch)
                except KeyError as e:
                    if "reference 'refs/remotes/" in str(e) and "' not found" in str(e):
                        # No branches found - treat as a tag
                        tag_repo = pygit2.clone_repository(clone_url, repo_path)
                        for remote in tag_repo.remotes:
                            remote.fetch([f"refs/tags/*:refs/tags/*"])
                        try:
                            tag_ref = tag_repo.references.get(f'refs/tags/{branch}')
                            tag_commit = tag_ref.peel()  # This gets the commit the tag points to
                        except AttributeError:
                            # Delete folder and error
                            shutil.rmtree(repo_path)
                            raise KeyError(f"No branch or tag '{branch}' not found for {repo_name}")

                        # Checkout the tag
                        tag_repo.checkout_tree(tag_commit)
                        tag_repo.set_head(tag_commit.id)
        except KeyError as e:
            logging.error(f"{e} - skipping")
            return False
        except ValueError as e:
            logging.error(f"An error occurred cloning {repo_name}: {e}, skipping")
            return False
        return True


