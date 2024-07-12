from abc import ABC, abstractmethod, abstractproperty
import pygit2
import csv


# Abstract class for source control system (SCM) interface
class SCM(ABC):

    @abstractproperty
    client = None

    def __init__(self):
        pass

    @abstractmethod
    def authenticate(self, token):
        pass

    @abstractmethod
    def get_user_orgs_repos(self, user):
        pass

    @abstractmethod
    def get_repo_branches(self, repo):
        pass

    @abstractmethod
    def get_tags(self, repo):
        pass

    @abstractmethod
    def get_triage_data(self):
        pass


