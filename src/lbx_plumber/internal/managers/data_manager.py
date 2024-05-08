"""Manage the data of the aplication."""

from lbx_python import python

from lbx_plumber.api import nodes, parameters, workspaces
from lbx_plumber.api.attributes import input_attributes, output_attributes
from lbx_plumber.internal import common
from lbx_plumber.internal.managers import manager


class DataManager(object):
    """Manage the data of the application."""

    __instance = None
    manager = manager.Manager()

    parameters = dict()  # store all the parameters by data type
    input_attributes = dict()  # store all the input attributes by data type
    output_attributes = dict()  # store all the output attributes by data type
    features = dict()  # store all the features by category and name
    add_ons = dict()  # store the list of add ons features names
    default_workspace = None

    def __new__(cls, *args, **kwargs):
        """Override the __new__ method to always return the same instance."""
        if not cls.__instance:
            cls.__instance = super(DataManager, cls).__new__(cls)

            # register to the manager
            cls.manager.data_manager = cls.__instance

            # make sure the app data path exists
            common.APP_DATA_PATH.create()
            common.USER_ADD_ONS_PATH.create()
            common.USER_ADD_ONS_PATH.get_folder("nodes").create()
            # make sure the default workspace exists
            cls.default_workspace = workspaces.Workspace(common.DEFAULT_WORKSPACE_PATH)
            try:
                cls.default_workspace.create()
            except RuntimeError:  # in case the workspace already exists
                cls.default_workspace.load()

            # load the builtin features
            cls.__instance.load_builtins()

        return cls.__instance

    # methods

    def load_builtins(self):
        """Load all the builtin features."""

        # get builtin parameters and attributes
        for variable, module, skip in (
            ("parameters", parameters, "Parameter"),
            ("input_attributes", input_attributes, "Attribute"),
            ("output_attributes", output_attributes, "Attribute"),
        ):
            items = dict()
            for name, _class in python.get_module_classes(module):
                # skip the abstract classes
                if not name.endswith(skip):
                    items[name] = _class
            setattr(self, variable, items)

        # get builtin features
        self._get_nodes_from_paths([common.PACKAGE_ADD_ONS_PATH], add_ons=False)

    def load_add_ons(self):
        """Load the add-ons features."""

        # get the add-ons paths
        paths = [common.USER_ADD_ONS_PATH, self.manager.workspace.projects_folder]

        # clear the add-ons
        for category in common.Features.CATEGORIES:
            add_ons_list = self.add_ons.get(category, list())
            items = self.features.get(category, dict())
            self.features[category] = {
                k: v for k, v in items.items() if k not in add_ons_list
            }

        # get add-ons features from the given paths
        self._get_nodes_from_paths(paths, add_ons=True)

    def _get_nodes_from_paths(self, paths, add_ons):
        """Get all the nodes stored in the given paths.

        Arguments:
            paths (list): The list of paths to parse.
            add_ons (bool): True if the paths are add-ons paths else False.
        """
        # reset the class variables
        self.features["nodes"] = _nodes = self.features.get("nodes", dict())
        if add_ons:
            self.add_ons["nodes"] = add_ons_list = list()

        # parse every given path
        for path in paths:
            # get the nodes
            for file in path.get_folder("nodes").get_files(recursive=True):
                module = python.import_module_from_path(file.base_name, file)
                for name, _class in python.get_module_classes(module):
                    # make sure the node's name is unique
                    base_name, index = name, 0
                    while name in _nodes:
                        name = "{}{}".format(base_name, index)
                        index += 1

                    # add the node to the list of nodes
                    _nodes[name] = {
                        "class": nodes.Node,
                        "data": {
                            "data_type": name,
                            "inputs": _class.inputs,
                            "outputs": _class.outputs,
                            "compute": _class.compute,
                        },
                    }

                    # update the add_ons list if necesary
                    if add_ons:
                        add_ons_list.append(name)
