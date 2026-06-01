import os
import sys
import json

class Config:
    """ Class to hold configuration settings for the application """
    def __init__(self):
        self.saved_names: list[str] = []
        self.pos: dict[str, int] = {'x': 100, 'y': 100}

        self.config_file = "tracker_config.json"
        self.config_path = os.path.join(self.get_exe_path(), self.config_file)
        
        self.load_config()

    def get_exe_path(self):
        """Gets the absolute path of the running script. This is used for saving/loading the config."""
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    
    def load_config(self):
        """Load settings from a .json file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                try:
                    config = json.load(f)
                    self.pos = config.get('pos', {'x': 100, 'y': 100})
                    self.saved_names = config.get('names', [""])

                except json.JSONDecodeError:
                    pass # If the config file is corrupted, just use default settings

    def save_config(self):
        """Save settings into a .json file"""
        config = {
            'pos': self.pos,
            'names': self.saved_names
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)