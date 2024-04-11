"""Manage the common behavior of all the objects."""

from lbx_pipeline.internal.managers import manager


class Object(object):
    """Manage the common behavior of all the objects."""

    manager = manager.Manager()
    session_logger = manager.session_logger
    project_logger = manager.project_logger

    @property
    def data_manager(self):
        """Get the application's data manager.

        Returns:
            DataManager: The application's data manager.
        """
        return self.manager.data_manager
