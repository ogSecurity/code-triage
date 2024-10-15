from abc import ABC, abstractmethod

import logging
import sys

logging.basicConfig(level=logging.INFO)


class Repository:
    def __init__(self, name, owner, default_branch, branch_list, is_empty, is_archived, is_fork, description, forks_count, updated_at, url, clone_url, tag_count, latest_tag, tags, open_issues_count):
        self.name = name
        self.owner = owner
        self.default_branch = default_branch
        self.branches = branch_list
        self.is_empty = is_empty
        self.is_archived = is_archived
        self.is_fork = is_fork
        self.description = description
        self.forks_count = forks_count
        self.updated_at = updated_at
        self.url = url
        self.clone_url = clone_url
        self.tag_count = tag_count
        self.latest_tag = latest_tag
        self.tags = []
        self.open_issues_count = open_issues_count


class Branch:
    def __init__(self, name):
        self.name = name


class Tag:
    def __init__(self, name):
        self.name = name


# Abstract class for source control system (SCM) interface
class SCM(ABC):
    def __init__(self):
        self._client = None
        self._auth_configuration = {}

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client) -> None:
        self._client = client

    """
    Returns a dictionary of authentication options for the SCM.
    Should return a list of dictionaries with the key as the authentication 
    type and the value a list of expected cli options that should 
    be present in the args object.
    """
    @staticmethod
    @abstractmethod
    def authentication_options() -> dict:
        pass

    @property
    def scm(self):
        return self._scm

    @property
    def auth_configuration(self):
        return self._auth_configuration

    @auth_configuration.setter
    def auth_configuration(self, auth_configuration):
        self._auth_configuration = auth_configuration

    @auth_configuration.getter
    def auth_configuration(self):
        return self._auth_configuration

    def get_auth_type(self):
        return self.auth_configuration.keys()[0]

    @abstractmethod
    def authenticate(self) -> None:
        pass

    @abstractmethod
    def get_repos(self, user):
        pass

    @abstractmethod
    def get_repo_branches(self, repo):
        pass

    @abstractmethod
    def get_tags_info(self, repo):
        pass

    @abstractmethod
    def get_triage_data(self):
        pass

    @abstractmethod
    def pull_repo(self, repo):
        pass

    def validate_auth_options(self, args) -> list:
        valid_auth_options = []
        auth_options = self.authentication_options()

        if not auth_options:
            logging.error(f"Unsupported SCM type: {args.scm}")
            sys.exit(1)

        # Iterate over each set of authentication options
        for options in auth_options:
            config = {}
            all_valid = True

            for option in options:
                value = getattr(args, option, None)
                if value:
                    # If it is an access token that's been provided, check
                    # if it is a file and read the contents, else treat it as the token
                    if option == 'access_token':
                        try:
                            with open(value, 'r') as file:
                                value = file.read().strip()
                        except FileNotFoundError:
                            logging.warning(f"Access token not referenced as a file - consider using a file to keep your API key out of your command history.")
                            pass

                    config[option] = value
                else:
                    all_valid = False
                    break

            if all_valid:
                valid_auth_options.append(config)

        # Log error if no valid configurations were found
        if not valid_auth_options:
            valid_options_str = "/".join(",".join(values) for values in auth_options[0].values())
            logging.error(f"Missing options for {args.scm} - valid options are: {valid_options_str}")
            sys.exit(1)

        # If multiple opions are provided, prompt user to select which one to use
        if len(valid_auth_options) > 1:
            print("Multiple valid authentication options found.")
            for index, config in enumerate(valid_auth_options, start=1):
                print(f"{index}. {config}")

            selection = int(input("Enter the number of the desired configuration: ")) - 1
            valid_auth_options = [valid_auth_options[selection]]
        else:
            valid_auth_options = valid_auth_options[0]

        return valid_auth_options

    def prompt_for_credentials(self, args) -> dict:
        auth_options = self.authentication_options()

        # Display the available authentication methods to the user
        print("Select the authentication type:")
        for index, options in enumerate(auth_options, start=1):
            option_names = ", ".join(options)
            print(f"{index}. {option_names}")

        # Prompt the user to choose an authentication type
        selection = int(input("Enter the number of the desired authentication type: ")) - 1
        selected_options = auth_options[selection]

        # Prompt the user to enter values for each required credential
        credentials = {}
        for option in selected_options:
            user_input = input(f"Please enter a value for '{option}': ")
            credentials[option] = user_input

        # Check if all required values have been provided
        missing_options = [option for option in selected_options if not credentials.get(option)]
        if missing_options:
            logging.error(f"Missing values for: {', '.join(missing_options)}")
            exit(1)

        print(f"All required credentials provided for {args.scm}.")
        return credentials

    def set_auth_configuration(self, args) -> None:
        if args.prompt:
            self.auth_configuration = self.prompt_for_credentials(args)
        self.auth_configuration = self.validate_auth_options(args)

