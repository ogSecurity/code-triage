import logging
import toml

logging.basicConfig(level=logging.INFO)

# Enum for the column names in the output CSV file
ROW_NAME_LABEL = 'Name'
ROW_OWNER_LABEL = 'Owner'
ROW_PULL_LABEL = 'Pull (Y/N)'
ROW_PULL_BRANCH_TAG_LABEL = 'Pull Branch/Tag'
ROW_NOTES_LABEL = 'Notes'
ROW_EMPTY_LABEL = 'Empty'
ROW_ARCHIVED_LABEL = 'Archived'
ROW_FORK_LABEL = 'Fork'
ROW_DESCRIPTION_LABEL = 'Description'
ROW_FORKS_LABEL = 'Forks'
ROW_OPEN_ISSUES_LABEL = 'Open Issues'
ROW_LAST_UPDATED_LABEL = 'Last Updated'
ROW_URL_LABEL = 'URL'
ROW_CLONE_URL_LABEL = 'Clone URL'
ROW_DEFAULT_BRANCH_LABEL = 'Default Branch'
ROW_BRANCH_LIST_LABEL = 'Branch List'
ROW_RELEASE_TAGS_LABEL = 'Release Tags'
ROW_LATEST_TAG_LABEL = 'Latest Tag'


class CodeTriageConfiguration:
    output_file: str = None

    def __init__(self, config_file: str = None, cli_options: dict = None):
        self.config_file = config_file
        if self.config_file:
            self.config = self.read_config()

    def read_config(self):
        with open(self.config_file, 'r') as file:
            config_file = toml.load(file)

        # Attempt to set default values
        try:
            self.output_file = config_file['output_file']
        except KeyError:
            self.output_file = None
