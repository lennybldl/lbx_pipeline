"""Manage the application."""

from lbx_pipeline.internal import logging


class Manager(object):
    """Manage the application."""

    _instance = None  # Manager : The manager's instance.

    data_manager = None
    synchronizer = None
    session_logger = logging.SessionLogger()
    project_logger = logging.ProjectLogger()

    # app variables
    _workspace = None
    project = None

    def __new__(cls):
        """Override the __new__ method to always return the same instance.

        Returns:
            Manager: An instance of the Manager class.
        """
        if not cls._instance:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    # methods

    def get_workspace(self):
        """Get the current workspace.

        Returns:
            Workspace: The current workspace.
        """
        if not self._workspace:
            self.workspace = None
        return self._workspace

    def set_workspace(self, workspace):
        """Set the current workspace.

        Arguments:
            workspace (Workspace): The current workspace.
        """
        # set the current workspace
        self._workspace = workspace or self.data_manager.default_workspace
        # update the add-ons
        self.data_manager.load_add_ons()

    workspace = property(get_workspace, set_workspace)
