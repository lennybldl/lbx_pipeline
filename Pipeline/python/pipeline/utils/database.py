"""Manage all the datas and datafiles needed for the application to work properly."""

import os

from pipeline.utils import properties


class Database(properties.DatabaseProperties):
    """Manage data and files and check if app can work correctly."""

    def __init__(self):
        """Make sure the app runs on safe basis"""

        super(Database, self).__init__()

    # Checks

    def start_checks(self):
        """Make sure the app runs on safe basis."""

        # check every needed files exists
        self.check_data_path_exists()
        self.check_app_data_file_exists()
        self.check_prefs_file_exists()

    def check_data_path_exists(self):
        """Check if the data folder exists."""

        # if data folder doesn't exists : create one
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def check_app_data_file_exists(self):
        """Check if the app_data file exists."""

        # if app_data file doesn't exists create one
        if not os.path.exists(self.app_data_file):
            self.set_default_app_data()

    def check_prefs_file_exists(self):
        """Check if the app_data file exists."""

        # if not create one
        if not os.path.exists(self.prefs_file):
            self.set_default_prefs()

    # set to default

    def set_default_app_data(self):
        """Write the basic variables we need in appData.json."""

        app_data = {
            "assets": {
                "props": {
                    "prefix": "pr_",
                    "path": r"assets\props",
                },
                "characters": {
                    "prefix": "ch_",
                    "path": r"assets\characters",
                },
                "shot": {
                    "prefix": "sh_",
                    "path": r"scenes",
                },
            },
            "tasks": [
                "modeling",
                "rig",
                "layout",
                "animation",
            ],
            "maya_folders": [
                "WIP",
                "DEF",
                "Publish",
            ],
            "unreal_folders": [
                "modeling",
                "textures",
                "animation",
            ],
        }

        # save default appData in a json file
        self.app_data = app_data

    def set_default_prefs(self):
        """Write the basic variables we need in prefs."""

        prefs = {}

        # save default prefs in a json file
        self.prefs = prefs
