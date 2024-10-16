import os
import csv
import logging
import sys

logging.basicConfig(level=logging.INFO)


class RowHeader:
    """
    A class that represents the structure of a row, including its label, default value, and visibility.
    """

    def __init__(self, label: str, type: any = str, default_value: any = '', hidden: bool = False, enabled: bool = True):
        self.label = label
        self.type = type
        self.default_value = default_value
        self.hidden = hidden
        self.enabled = enabled


class RowConfiguration:
    """
    This class defines the structure for the output, including row labels, default values, and whether
    the row should be hidden.
    Note: This should match the Row class structure.
    """

    # Row configurations (structure only, no actual data)
    name = RowHeader(label='Name', type=str)
    owner = RowHeader(label='Owner', type=str)
    pull = RowHeader(label='Pull (Y/N)', type=str)
    pull_branch_tag = RowHeader(label='Pull Branch/Tag', type=str)
    notes = RowHeader(label='Notes', type=str)
    empty = RowHeader(label='Empty', type=bool, default_value=False)
    archived = RowHeader(label='Archived', type=bool, default_value=False)
    fork = RowHeader(label='Fork', type=bool, default_value=False)
    description = RowHeader(label='Description', type=str)
    forks = RowHeader(label='Forks', type=int, default_value=0)
    open_issues = RowHeader(label='Open Issues', type=int, default_value=0)
    last_updated = RowHeader(label='Last Updated')
    url = RowHeader(label='URL')
    clone_url = RowHeader(label='Clone URL')
    default_branch = RowHeader(label='Default Branch')
    branch_list = RowHeader(label='Branch List')
    tags = RowHeader(label='Release Tags', type=int, default_value=0)
    latest_tag = RowHeader(label='Latest Tag', type=str)


class Row:
    """
    This class represents a single row of data, using the RowConfiguration to provide property-based
    access to the row values.
    Note: This should match the RowConfiguration structure.
    """

    def __init__(self, row_config: RowConfiguration):
        # Initialize a dictionary to store actual row values, starting with the defaults from RowConfiguration
        self._data = {key: getattr(row_config, key).default_value for key in dir(row_config)
                      if isinstance(getattr(row_config, key), RowHeader)}
        self._config = row_config  # Store the row configuration to access types

    def _check_type(self, key: str, value: any):
        """
        Validate that the value being set matches the expected type defined in the RowConfiguration.
        """
        expected_type = getattr(self._config, key).type
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected {expected_type} for '{key}', but got {type(value)}")

    @property
    def name(self):
        return self._data['name']

    @name.setter
    def name(self, value):
        self._check_type('name', value)
        self._data['name'] = value

    @property
    def owner(self):
        return self._data['owner']

    @owner.setter
    def owner(self, value):
        self._check_type('owner', value)
        self._data['owner'] = value

    @property
    def pull(self):
        return self._data['pull']

    @pull.setter
    def pull(self, value):
        self._check_type('pull', value)
        self._data['pull'] = value

    @property
    def pull_branch_tag(self):
        return self._data['pull_branch_tag']

    @pull_branch_tag.setter
    def pull_branch_tag(self, value):
        self._check_type('pull_branch_tag', value)
        self._data['pull_branch_tag'] = value

    @property
    def notes(self):
        return self._data['notes']

    @notes.setter
    def notes(self, value):
        self._check_type('notes', value)
        self._data['notes'] = value

    @property
    def empty(self):
        return self._data['empty']

    @empty.setter
    def empty(self, value):
        self._check_type('empty', value)
        self._data['empty'] = value

    @property
    def archived(self):
        return self._data['archived']

    @archived.setter
    def archived(self, value):
        self._check_type('archived', value)
        self._data['archived'] = value

    @property
    def fork(self):
        return self._data['fork']

    @fork.setter
    def fork(self, value):
        self._check_type('fork', value)
        self._data['fork'] = value

    @property
    def description(self):
        return self._data['description']

    @description.setter
    def description(self, value):
        self._check_type('description', value)
        self._data['description'] = value

    @property
    def forks(self):
        return self._data['forks']

    @forks.setter
    def forks(self, value):
        self._check_type('forks', value)
        self._data['forks'] = value

    @property
    def open_issues(self):
        return self._data['open_issues']

    @open_issues.setter
    def open_issues(self, value):
        self._check_type('open_issues', value)
        self._data['open_issues'] = value

    @property
    def last_updated(self):
        return self._data['last_updated']

    @last_updated.setter
    def last_updated(self, value):
        self._check_type('last_updated', value)
        self._data['last_updated'] = value

    @property
    def url(self):
        return self._data['url']

    @url.setter
    def url(self, value):
        self._check_type('url', value)
        self._data['url'] = value

    @property
    def clone_url(self):
        return self._data['clone_url']

    @clone_url.setter
    def clone_url(self, value):
        self._check_type('clone_url', value)
        self._data['clone_url'] = value

    @property
    def default_branch(self):
        return self._data['default_branch']

    @default_branch.setter
    def default_branch(self, value):
        self._check_type('default_branch', value)
        self._data['default_branch'] = value

    @property
    def branch_list(self):
        return self._data['branch_list']

    @branch_list.setter
    def branch_list(self, value):
        self._check_type('branch_list', value)
        self._data['branch_list'] = value

    @property
    def tags(self):
        return self._data['tags']

    @tags.setter
    def tags(self, value):
        self._check_type('tags', value)
        self._data['tags'] = value

    @property
    def latest_tag(self):
        return self._data['latest_tag']

    @latest_tag.setter
    def latest_tag(self, value):
        self._check_type('latest_tag', value)
        self._data['latest_tag'] = value


class Output:
    """
    The Output class contains a list of rows (data) and holds a reference to the RowConfiguration to
    know how to deal with each column. It includes methods for writing out to CSV.
    """

    def __init__(self, row_config: RowConfiguration, output_file: str, format: str = 'csv'):
        self.row_config = row_config  # Store the row configuration
        self.output_file = output_file
        self.output_file_handle = None
        self.format = format
        self.rows = []  # List to store rows of data

        # Pre-checks on the output file, does it already exist or is it open?
        if os.path.exists(output_file):
            overwrite = input(f"File {output_file} already exists. Overwrite? (Y/N): ")
            if overwrite.casefold() not in {'y', 'yes'}:
                logging.info("Exiting...")
                sys.exit(1)

        try:
            self.output_file_handle = open(output_file, mode='w', newline='')
        except PermissionError:
            logging.error(f"Permission denied to write to file: {output_file} - is it open?")
            sys.exit(1)

    def add_row(self, row: Row):
        """
        Add a new Row to the list of rows.
        """
        self.rows.append(row)

    def write(self):
        """
        Write the current rows to the output file, based on the format.
        """
        if self.format == 'csv':
            self.write_csv()
        else:
            logging.error(f"Unsupported output format: {self.format}")

    def write_csv(self):
        """
        Write the current rows to a CSV file, including only visible (non-hidden) columns.
        """
        # Get visible headers and their corresponding keys from the row configuration
        # Note: hidden not supported in csv files
        headers = [key for key, value in vars(self.row_config.__class__).items() if isinstance(value, RowHeader)]
        header_labels = [getattr(self.row_config, key).label for key in headers]

        writer = csv.writer(self.output_file_handle, dialect='excel')
        writer.writerow(header_labels)

        # Write each row of data
        for row in self.rows:
            row_data = [getattr(row, key) for key in headers]
            writer.writerow(row_data)

        self.output_file_handle.flush()
        self.output_file_handle.close()


class TriageFile:
    """
    This class is responsible for loading and parsing the triage file, which contains a list of repositories
    """

    def __init__(self, file_path: str, row_config: RowConfiguration, format: str = 'csv'):
        self.file_path = file_path
        self.format = format
        self.row_config = row_config
        self.rows = []

        # Pre-checks on the triage file, does it exist?
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} does not exist.")
            sys.exit(1)

        # Load the data from the file
        if format == 'csv':
            self.load_csv()
        else:
            logging.error(f"Unsupported file format: {format}")
            sys.exit(1)

    def load_csv(self):
        """
        Load data from a CSV file, using the row configuration to map columns to properties.
        """
        with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read the CSV header row

            # Create a mapping from the header label (in CSV) to the row configuration keys
            header_map = {getattr(self.row_config, key).label: key for key in vars(self.row_config.__class__) if
                          isinstance(getattr(self.row_config, key), RowHeader)}

            # Read each row and create a new Row object
            for row in reader:
                new_row = Row(self.row_config)
                for header, value in zip(headers, row):
                    if header in header_map:
                        key = header_map[header]

                        # Retrieve the expected type from the row configuration
                        expected_type = getattr(self.row_config, key).type

                        # Define a mapping for type conversions
                        type_conversions = {
                            bool: lambda v: v.upper() == 'TRUE' if v else False,
                            str: lambda v: v if v else "",
                            int: lambda v: int(v) if v else 0,
                        }

                        try:
                            # Perform the conversion using the type_conversions dictionary
                            new_value = type_conversions.get(expected_type, expected_type)(value)
                        except ValueError as e:
                            logging.error(f"Error converting value '{value}' to type {expected_type}: {e} for '{key}'")

                        try:
                            setattr(new_row, key, new_value)
                        except TypeError as e:
                            logging.error(f"Error setting value '{value}' for '{key}': {e}")

                self.rows.append(new_row)

    def get_data(self):
        """
        Return the loaded data.
        """
        return self.rows



