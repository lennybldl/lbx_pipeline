"""Manage the constant variables of the application."""

from lbx_python import system

import lbx_plumber

# config
PROJECT_EXTENSION = "pipe"
PROJECT_FOLDER_NAME = ".pipeline"
ADD_ONS_FOLDER_NAME = "add_ons"

# folders
ROOT = system.Folder(lbx_plumber.ROOT)
RESOURCES_PATH = ROOT.get_folder("resources")
IMAGES_PATH = RESOURCES_PATH.get_folder("images")
# package folders
PACKAGE_ADD_ONS_PATH = RESOURCES_PATH.get_folder(ADD_ONS_FOLDER_NAME)
# app data folders
APP_DATA_PATH = system.Folder([system.get_user_path(), ".lbx", "plumber"])
USER_ADD_ONS_PATH = APP_DATA_PATH.get_folder(ADD_ONS_FOLDER_NAME)
DEFAULT_WORKSPACE_PATH = APP_DATA_PATH.get_folder("default")


class Features(object):
    """List the possible features types."""

    NODE = "nodes"
    CATEGORIES = [NODE]


# plugs color codes from Autodesk Maya
SOCKET_TYPE_COLORS = {
    "Bool": "#E69963",
    "Int": "#62CFD9",
    "Float": "#82D99F",
    "Str": "#D9BE6C",
    "Vector": "#A8D977",  # TODO just idea
    "Matrix": "#E67373",  # TODO just idea
    "List": "#CCB699",  # TODO just idea
    "Dict": "#546E7A",  # TODO just idea
    "Path": "#90A3F4",  # TODO just idea
}


def get_image(name, slashed=True):
    """Get an icon by its file name.

    Arguments:
        name (str): The name of the image file. (e.g. "image.svg")

    Keyword Arguments:
        slashed (bool, optional): True to get the image path with slashes.
            Else, convert the slashes to backslashes. Defaults to True.

    Returns:
        str: The path to the icon.
    """
    file = IMAGES_PATH.get_file(name)
    if file.exists():
        return file.slashed() if slashed else file.back_slashed()
    raise KeyError("Unabled to find: {}".format(name))
