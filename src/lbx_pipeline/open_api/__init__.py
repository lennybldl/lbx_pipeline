"""Manage the package's api commands the users have access to."""

from lbx_pipeline import api
from lbx_pipeline.api import workspaces


# management


def run():
    """Run the application.

    It is mandatory to run this command first when using the package on its own to
    initialize the needed variables.
    """
    api.run()


def get_object_types(category):
    """Get the list of types for a specific category objects.

    Arguments:
        category (str): The type of category to get the types from.
            (e.g. "nodes", "attributes", etc.).

    Returns:
        list: The list of object types.
    """
    from lbx_pipeline.internal.managers import data_manager

    manager = data_manager.DataManager()
    if category == "attributes":
        return list(manager.attributes.keys())
    else:
        return list(manager.features.get(category, dict()).keys())


# workspace commands


def create_workspace(path, force=False):
    """Create a workspace and initialize it.

    Arguments:
        path (str): The path of the workspace.
        force (bool, optional): Replace the existing workspace if True.
            Default to False.

    Returns:
        Workspace: The created workspace.
    """
    workspace = workspaces.Workspace(path)
    workspace.create(force=force)
    return workspace


def load_workspace(path):
    """Load a workspace and initialize it.

    Arguments:
        path (str): The path of the workspace.
        force (bool, optional): Replace the existing workspace if True.
            Default to False.

    Returns:
        Workspace: The load workspace.
    """
    workspace = workspaces.Workspace(path)
    workspace.load()
    return workspace
