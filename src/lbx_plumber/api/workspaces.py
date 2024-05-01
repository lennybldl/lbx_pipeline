"""Manage the workspaces."""

from lbx_python import system

from lbx_plumber.api import projects
from lbx_plumber.api.abstract import objects
from lbx_plumber.internal import core


class Workspace(system.Folder, objects.Object):
    """Manage the workspaces."""

    def __repr__(self):
        """Override the __repr__ method.

        Returns:
            str: The new representation of the object.
        """
        return "(Workspace){}".format(self.path)

    # management

    def create(self, path=None, force=False):
        """Create the workspace.

        Keyword Arguments:
            path (str, optional): The path to the workspace to create.
                Default to None.
            force (bool, optional): Replace the existing workspace if True.
                Default to False.

        Raises:
            RuntimeError: If the project already exists.
        """
        # get the workspace path
        self.path = path or self.path

        # overwrite the workspace or not
        if self.exists() and not self.is_empty:
            if not force:
                raise RuntimeError(
                    "A workspace already exists at the given path '{}'".format(
                        self.path
                    )
                )
            # force the creation of the project
            # by removing the previous project and recreating it
            self.remove()

        # inheritance
        super(Workspace, self).create()

        # load the created workspace
        self.load()

    def load(self, path=None):
        """Load an existing workspace.

        Keyword Arguments:
            path (str, optional): The path to the workspace to create.
                Default to None.
        """
        # get the workspace path
        self.path = path or self.path

        # make sure the project folder exists
        self.projects_folder = self.get_folder(core.PROJECT_FOLDER_NAME)
        self.projects_folder.create()

        # make sure the add_ons folder exists
        add_ons_folder = self.projects_folder.get_folder(core.ADD_ONS_FOLDER_NAME)
        add_ons_folder.create()
        for category in core.Features.CATEGORIES:
            add_ons_folder.get_folder(category).create()

        # register to the manager
        self.manager.workspace = self

    # methods

    def create_project(self, name, force=False):
        """Create a project within the current workspace.

        Arguments:
            name (str): The name of the project to create.

        Keyword Arguments:
            force (bool, optional): Replace the existing project if True.
                Default to False.

        Raises:
            ValueError: The project name can't be valid.
            RuntimeError: If the project already exists.

        Returns:
            Project: The created project.
        """
        # make sure the project name isn't invalid
        if name.count(".") > 1:
            raise ValueError("Invalid project name '{}'".format(name))

        # figure out the project and its folder's name
        extension = ".{}".format(core.PROJECT_EXTENSION)
        if name.endswith(extension):
            base_name = name.replace(extension, "")
        else:
            base_name = name
            name = name + extension

        # get the project items
        project_folder = self.get_folder(base_name)
        project_file = project_folder.get_file(name)

        # make sure the project is creatable
        if project_folder.exists() and not project_folder.is_empty:
            if not force:
                raise RuntimeError("A project named '{}' already exists".format(name))
            # force the creation of the project
            # by removing the previous project and recreating it
            project_folder.remove()

        # create the project folder
        project_folder.create()

        # create the project
        project = projects.Project(project_file)
        project.create()
        return project

    def load_project(self, name):
        """Load a project within the current workspace.

        Arguments:
            name (str): The name of the project to load.

        Raises:
            ValueError: The project name can't be valid.
            RuntimeError: If the project doesn't exists.

        Returns:
            Project: The created project.
        """
        # make sure the project name isn't invalid
        if name.count(".") > 1:
            raise ValueError("Invalid project name '{}'".format(name))

        # figure out the project and its folder's name
        extension = ".{}".format(core.PROJECT_EXTENSION)
        if name.endswith(extension):
            base_name = name.replace(extension, "")
        else:
            base_name = name
            name = name + extension

        # get the project items
        project_folder = self.get_folder(base_name)
        project_file = project_folder.get_file(name)

        # make sure the project exists
        if not project_file.exists():
            raise RuntimeError("No project named '{}'".format(name))

        # create the project
        project = projects.Project(project_file)
        project.load()
        return project
