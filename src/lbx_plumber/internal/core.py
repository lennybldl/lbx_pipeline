"""Manage the constant variables of the application."""

from lbx_python import system

import lbx_plumber

# config
PROJECT_EXTENSION = "pipe"
PROJECT_FOLDER_NAME = ".pipeline"
ADD_ONS_FOLDER_NAME = "add_ons"

# folders
PATH = system.Folder(lbx_plumber.ROOT)
RESOURCES = PATH.get_folder("resources")
# package folders
PACKAGE_ADD_ONS_PATH = RESOURCES.get_folder(ADD_ONS_FOLDER_NAME)
# app data folders
APP_DATA_PATH = system.Folder([system.get_user_path(), ".lbx", "pipeline"])
USER_ADD_ONS_PATH = APP_DATA_PATH.get_folder(ADD_ONS_FOLDER_NAME)
DEFAULT_WORKSPACE_PATH = APP_DATA_PATH.get_folder("default")


class Features(object):
    """List the possible features types."""

    NODE = "nodes"
    CATEGORIES = [NODE]
