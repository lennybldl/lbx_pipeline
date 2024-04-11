"""Manage the application's api."""

from lbx_pipeline.internal.managers import manager, data_manager, synchronizer


def run():
    """Run the application.

    It is mandatory to run this command first when using the package on its own to
    initialize the needed variables.
    """
    manager.Manager()
    data_manager.DataManager()
    synchronizer.Synchronizer()
