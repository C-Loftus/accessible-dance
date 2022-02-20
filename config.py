from csv import excel_tab
import yaml
import os

APP_PATH = "Gamepad/config.yaml"
HARDWARE_PATH = "Gamepad/hardware_mappings.yaml"

class application_config:

    def __init__(self):
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.app_path = os.path.join(ROOT_DIR, APP_PATH)
        self.hardware_path = os.path.join(ROOT_DIR, HARDWARE_PATH)
        
        self._load_config()

    def _load_config(self):
        with open(self.app_path) as file:
            try:
                self.config = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise Exception("Error loading config file at {}".format(self.app_path))
        with open(self.hardware_path) as file:
            try:
                self.hardware = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise Exception("Error loading hardware config file at {}".format(self.hardware_path))

    def get_config(self):
        return self.config
    def get_hardware_config(self):
        return self.hardware

    def get_hardware_list(self, gamepad):
        return {k:v for x in self.hardware[gamepad] for k,v in x.items()}

    def print_config(self):
        for key in self.config:
            print(key, self.config[key])
    def print_hardware(self):
        for device in self.hardware:
            print(device)

    def pad_listed(self, pad_name) -> bool:
        if pad_name in self.hardware:
            return True
        raise Exception("Pad \"{}\" not found in hardware config file".format(pad_name))

    def key_listed(self, key, gamepad) -> bool:
        key_list = self.get_hardware_list(gamepad)

        if key in key_list:
            return True
        raise Exception("Key {} not found in hardware config file".format(key))

    def button_mapped(self, button):
        for b in self.config:
            if button == str(b):
                return True
        raise Exception("Button {} not mapped in config file".format(button))

    def action_from_key(self, key):
        try:
            return self.config[key]
        except KeyError:
            raise Exception("Key {} not found in config file".format(key))

    def decode_press(self, gamepad, key):
        if self.pad_listed(gamepad):
            if self.key_listed(key, gamepad):
                dancepad_button = self.get_hardware_list(gamepad)[key]

                if self.button_mapped(dancepad_button):
                    return self.action_from_key(dancepad_button)

    