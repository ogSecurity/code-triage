import logging
import toml

logging.basicConfig(level=logging.INFO)


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
