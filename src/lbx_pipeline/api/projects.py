"""Manage the project."""

from lbx_python_core import dictionaries, system

from lbx_pipeline.api.abstract import networks
from lbx_pipeline.internal import core, exceptions


class Project(system.File, networks.Network):
    """Manage the project."""

    # management

    def create(self):
        """Create the project."""
        # make sure the project path is valid
        if self.exists():
            raise exceptions.ConfictingProjectPathError(self)
        if not self.extension == core.PROJECT_EXTENSION:
            raise exceptions.InvalidProjectPathError(self)

        # inheritance
        super(Project, self).create("{}")
        # load the project
        self.load()

    def load(self, path=None):
        """Load the project.

        Keyword Arguments:
            path (str, optional): The path to the project to load.
                Default to None.
        """
        # make sure the project path is valid
        path = system.File(path or self)
        if not path.is_file or not path.extension == core.PROJECT_EXTENSION:
            raise exceptions.InvalidProjectPathError(path)

        # load the project's data
        self.path = path
        data = dictionaries.Dictionary(self)
        self.deserialize(**data)

    def save(self, path=None, *args, **kwargs):
        """Save the current project.

        Keyword Arguments:
            path (str, optional): The path where to save the project as.
                Default to None.
        """
        # make sure the project path is valid
        path = system.File(path or self)
        if path.extension != core.PROJECT_EXTENSION:
            raise exceptions.InvalidProjectPathError(path)

        # save the data
        data = dictionaries.Dictionary(self.serialize())
        data.dump(path, *args, **kwargs)
        # update the variables
        self.path = path
        self.project_logger.name = self.name

    # methods

    def set_name(self, name):
        """Set the name of the project.

        Arguments:
            name (str): The project's name.
        """
        super(Project, self).set_name(name)
        self.project_logger.set_name(name)

    name = property(system.File.get_name, set_name)
