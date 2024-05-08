"""Manage the application."""

from lbx_plumber.internal import logging


class Manager(object):
    """Manage the application."""

    __instance = None  # Manager : The manager's instance.

    # managers
    data_manager = None
    synchronizer = None
    preferences = None

    # loggers
    session_logger = logging.SessionLogger()
    project_logger = logging.ProjectLogger()

    # main ui variables
    main_window = None

    # app variables
    _workspace = None
    is_evaluation_suspended = False

    def __new__(cls):
        """Override the __new__ method to always return the same instance.

        Returns:
            Manager: An instance of the Manager class.
        """
        if not cls.__instance:
            cls.__instance = super(Manager, cls).__new__(cls)
        return cls.__instance

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

    def set_evaluation_suspended(self, value):
        """Set the node evaluation supended or not.

        Arguments:
            value (bool): True to suspend the evaluation, else False.
        """
        self.is_evaluation_suspended = value
