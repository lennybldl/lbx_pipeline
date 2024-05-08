"""Manage the application preferences."""

from lbx_python import dictionaries

from lbx_plumber.internal import common
from lbx_plumber.internal.managers import manager


class Preferences(dictionaries.Dictionary):
    """Manage the application preferences."""

    manager = manager.Manager()

    def __init__(self, *args, **kwargs):
        """Initialize the preferences."""

        # create preferences
        self.path = common.APP_DATA_PATH.get_file("prefs.json")
        self.path.create(content="{}")

        # inheritance - load the dictionary
        super(Preferences, self).__init__(self.path, *args, **kwargs)

        # register the instance to the manager
        self.manager.preferences = self
