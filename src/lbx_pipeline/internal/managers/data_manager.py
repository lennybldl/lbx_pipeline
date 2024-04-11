"""Manage the data of the aplication."""

from lbx_python_core import python

from lbx_pipeline.internal import core
from lbx_pipeline.internal.managers import manager
from lbx_pipeline.api import attributes, parameters, workspaces


class DataManager(object):
    """Manage the data of the application."""

    _instance = None
    manager = manager.Manager()

    parameters = dict()  # store all the parameters by data type
    attributes = dict()  # store all the parameters by data type
    features = dict()  # store all the features by category and name
    add_ons = dict()  # store the list of add ons features names
    default_workspace = None

    def __new__(cls, *args, **kwargs):
        """Override the __new__ method to always return the same instance."""
        if not cls._instance:
            cls._instance = super(DataManager, cls).__new__(cls)

            # register to the manager
            cls.manager.data_manager = cls._instance

            # make sure the app data path exists
            core.APP_DATA_PATH.create()
            core.USER_ADD_ONS_PATH.create()
            core.USER_ADD_ONS_PATH.get_folder("nodes").create()
            core.USER_ADD_ONS_PATH.get_folder("macros").create()
            # make sure the default workspace exists
            cls.default_workspace = workspaces.Workspace(core.DEFAULT_WORKSPACE_PATH)
            try:
                cls.default_workspace.create()
            except RuntimeError:  # in case the workspace already exists
                cls.default_workspace.load()

            # load the builtin features
            cls._instance.load_builtins()

        return cls._instance

    # methods

    def load_builtins(self):
        """Load all the builtin features."""

        # get builtin parameters and attributes
        for variable, module, skip in (
            ("parameters", parameters, "Parameter"),
            ("attributes", attributes, "Attribute"),
        ):
            items = dict()
            for name, _class in python.get_module_classes(module):
                # skip the abstract classes
                if not name.endswith(skip):
                    items[name] = _class
            setattr(self, variable, items)

        # get builtin nodes and macros
        self._get_resources_from_paths([core.PACKAGE_ADD_ONS_PATH], add_ons=False)

    def load_add_ons(self):
        """Load the add-ons features."""

        # get the add-ons paths
        paths = [core.USER_ADD_ONS_PATH, self.manager.workspace.projects_folder]

        # load the resources from the add-ons paths
        self._get_resources_from_paths(paths, add_ons=True)

    def _get_resources_from_paths(self, paths, add_ons):
        """Get the resources stored in the given paths.

        Arguments:
            paths (list): The list of paths to parse.
            add_ons (bool): True if the paths are add-ons paths else False.
        """
        # clear the add-ons
        for category in core.FEATURES_TYPES:
            add_ons_list = self.add_ons.get(category, list())
            items = self.features.get(category, dict())
            self.features[category] = {
                k: v for k, v in items.items() if k not in add_ons_list
            }

        # reset the class variables
        self.features["nodes"] = nodes = self.features.get("nodes", dict())
        self.features["macros"] = macros = self.features.get("macros", dict())
        if add_ons:
            self.add_ons["nodes"] = add_ons_nodes_list = list()
            self.add_ons["macros"] = add_ons_macros_list = list()

        # parse every given path
        for path in paths:
            # get the nodes
            for file in path.get_folder("nodes").get_files(recursive=True):
                module = python.import_module_from_path(file.base_name, file)
                for name, _class in python.get_module_classes(module):
                    # make sure the node's name is unique
                    base_name, index = name, 0
                    while name in nodes:
                        name = "{}{}".format(base_name, index)
                        index += 1
                    # add the node to the list of nodes
                    nodes[name] = _class
                    if add_ons:
                        add_ons_nodes_list.append(name)

            # get the macros
            for file in path.get_folder("macros").get_files(recursive=True):
                # make sure the node's name is unique
                name = file.base_name
                base_name, index = name, 0
                while name in macros:
                    name = "{}{}".format(base_name, index)
                    index += 1
                # add the node to the list of macros
                macros[name] = file
                if add_ons:
                    add_ons_macros_list.append(name)
