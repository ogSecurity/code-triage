from .scm import SCM
from github import Github, Auth


class GithubPublic(SCM):

    def __init__(self):
        pass

    def authenticate(self, token):
        self.client = Github(auth=Auth.Token(token))

    def get_user_orgs_repos(self, user):
        return self.client.get_user(user).get_repos()

    def get_repo_tags(self, repo):
        return repo.get_tags()

    def get_repo_branches(self, repo):
        return repo.get_branches()

    def get_triage_data(self):
        repo_list = []
        for repo in self.client.get_user().get_repos():
            yield repo


        return repo_list