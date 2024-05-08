"""Manage the application's api."""

from lbx_plumber.internal.managers import (
    manager,
    data_manager,
    preferences,
    synchronizer,
)


def run():
    """Run the application.

    It is mandatory to run this command first when using the package on its own to
    initialize the needed variables.
    """
    manager.Manager()
    data_manager.DataManager()
    synchronizer.Synchronizer()
    preferences.Preferences()
