"""Manage the synchronizer class.

This class is in charge of the communication between every member of the UI.
"""

from lbx_pipeline.internal.managers import manager


class Synchronizer(object):
    """Manage the communications between the UI members."""

    __instance = None
    manager = manager.Manager()

    def __new__(cls, *args, **kwargs):
        """Override the __new__ method to always return the same instance."""
        if not cls.__instance:
            cls.__instance = super(Synchronizer, cls).__new__(cls)
            # register to the manager
            cls.manager.synchronizer = cls.__instance

        return cls.__instance
