"""Manage the application."""

from lbx_pipeline.internal import session


class Manager(object):
    """Manage the application."""

    software = None  # str : The software we're executing the pipeline from.

    def __init__(self, software):
        """Initialize the manager.

        Arguments:
            software (str): The software we're executing the pipeline on.
        """
        # inheritance
        super(Manager, self).__init__()

        # update the variables
        self.software = software
        session.MANAGER = self

    # methods

    def load(self, path):
        """Load a pipeline from a specific path.

        Arguments:
            path (str): The path to the project.
        """

    def create(self, path):
        """Create the pipeline folder and initialize.

        Arguments:
            path (str): The path to create the pipeline to.
        """
