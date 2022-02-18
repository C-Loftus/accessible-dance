import yaml
import os

PATH = "Gamepad/config.yaml"

class application_config:

    def __init__(self):
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(ROOT_DIR, PATH)
        
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        with open(self.config_path) as file:
            try:
                self.config = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise Exception("Error loading config file at {}".format(self.config_path))

    def get_config(self):
        return self.config