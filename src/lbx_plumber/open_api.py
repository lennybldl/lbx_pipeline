"""Manage the package's api commands the users have access to."""

from lbx_plumber import api
from lbx_plumber.api import attributes, workspaces
from lbx_plumber.internal import proxies
from lbx_plumber.internal.managers import manager, data_manager

# management


def run():
    """Run the application.

    It is mandatory to run this command first when using the package on its own to
    initialize the needed variables.
    """
    api.run()


def setEvaluationSuspended(value):
    """Set the node evaltuation suspended or not.

    Arguments:
        value (bool): True to suspend the evaluation else False.
    """
    _manager = manager.Manager()
    _manager.set_evaluation_suspended(value)


def listObjectTypes(category):
    """Get the list of types for a specific category objects.

    Arguments:
        category (str): The type of category to get the types from.
            (e.g. "nodes", "attributes", etc.).

    Returns:
        list: The list of object types.
    """
    manager = data_manager.DataManager()
    if category == "attributes":
        return list(manager.input_attributes.keys())
    return list(manager.features.get(category, dict()).keys())


# commands access


def createWorkspace(path, force=False):
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
    return Workspace(workspace)


def loadWorkspace(path):
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
    return Workspace(workspace)


# classes access


class Workspace(proxies.Proxy):
    """Manage the proxy nodes."""

    def getPath(self):
        """Get the project's path.

        Returns:
            str: The project's path.
        """
        return self._Proxy__api_instance.path

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
        self._Proxy__api_instance.create(path, force)

    def load(self, path=None):
        """Load an existing workspace.

        Keyword Arguments:
            path (str, optional): The path to the workspace to create.
                Default to None.
        """
        self._Proxy__api_instance.load(path)

    def createProject(self, name, force=False):
        """Create a project within the current workspace.

        Arguments:
            name (str): The name of the project to create.

        Keyword Arguments:
            force (bool, optional): Replace the existing project if True.
                Default to False.

        Raises:
            RuntimeError: If the project already exists.

        Returns:
            Project: The created project.
        """
        return Project(self._Proxy__api_instance.create_project(name, force))

    def loadProject(self, name):
        """Load a project within the current workspace.

        Arguments:
            name (str): The name of the project to load.

        Raises:
            RuntimeError: If the project doesn't exists.

        Returns:
            Project: The created project.
        """
        return Project(self._Proxy__api_instance.load_project(name))


class SerializableObject(proxies.Proxy):
    """Manage the proxy serializable objects."""

    def getName(self):
        """Get the name of the current object.

        Returns:
            str: The current object's name.
        """
        return self._Proxy__api_instance.name

    def setName(self, name):
        """Set the name of the current object.

        Arguments:
            name (str): The current object's name.
        """
        self._Proxy__api_instance.name = name

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        return self._Proxy__api_instance.serialize()


class Project(SerializableObject):
    """Manage the proxy nodes."""

    def getPath(self):
        """Get the project's path.

        Returns:
            str: The project's path.
        """
        return self._Proxy__api_instance.path

    def create(self):
        """Create the project."""
        self._Proxy__api_instance.create()

    def load(self, path=None):
        """Load the project.

        Keyword Arguments:
            path (str, optional): The path to the project to load.
                Default to None.
        """
        self._Proxy__api_instance.load(path)

    def save(self, path=None, *args, **kwargs):
        """Save the current project.

        Keyword Arguments:
            path (str, optional): The path where to save the project as.
                Default to None.
        """
        self._Proxy__api_instance.save(path, *args, **kwargs)

    def eval(self):
        """Evaluate every nodes from the project."""
        self._Proxy__api_instance.eval()

    def addNetwork(self, **data):
        """Add a network to the current project.

        Returns:
            Network: The created network.
        """
        return Network(self._Proxy__api_instance.add_network(**data))

    def getNetwork(self, name):
        """Get a network using its name.

        Arguments:
            name (str): The name of the network.

        Raises:
            KeyError: Tried to access non-existing network.

        Returns:
            Network: The network we asked for.
        """
        return Network(self._Proxy__api_instance.get_network(name))

    def getNetworks(self):
        """Get the list of networks on the current object.

        Returns:
            dict: The current networks.
        """
        return [Network(o) for o in self._Proxy__api_instance.get_networks()]


class DataObject(SerializableObject):
    """Manage the common methods to all the data objects."""

    def getDataType(self):
        """Get the data type of the current object.

        Returns:
            str: The data type of the current object.
        """
        self._Proxy__api_instance.data_type

    def getPath(self, relative_to=None):
        """Get the path of the current object in its parent hierarchy.

        Keyword Arguments:
            relative_to (str, optional): The path to get the relative path from.
                Default to None.

        Returns:
            str: The path of the current object.
        """
        self._Proxy__api_instance.get_path(relative_to=relative_to)

    def delete(self):
        """Delete the current object"""
        self._Proxy__api_instance.delete()


class Network(DataObject):
    """Manage the prox networks"""

    # features methods

    def addNode(self, data_type, **data):
        """Add a node to the current object.

        Arguments:
            data_type (str): The type of node to create.
            data (dict): The data to deserialize with.

        Returns:
            Node: The created node.
        """
        return Node(self._Proxy__api_instance.add_node(data_type, **data))

    def getNode(self, name):
        """Get a node using its name.

        Arguments:
            name (str): The name of the node.

        Returns:
            Node: The desired node.
        """
        return Node(self._Proxy__api_instance.get_node(name))

    # data management

    def connect(self, source, *destinations, force=True):
        """Connect an attribute to another.

        Arguments:
            source (str, Attribute): The source attribute to connect.
            destinations (str, Attribute, list): The destination attributes
                to connect to.

        Keyword Arguments:
            force (bool, optional): To force the connection if already connected.
                Default to True.

        Raises:
            RuntimeError:
                | - No destinations given.
                | - One of the attributes isn't valid.
        """
        # make sure we do not work with open_api objects
        source = self.__get_api_instance(source)
        destinations = (self.__get_api_instance(d) for d in destinations)
        # connect the attributes
        self._Proxy__api_instance.connect(source, *destinations, force=force)

    def disconnect(self, attribute):
        """Disconnect the attributes from its input and outputs.

        Arguments:
            attribute (str, Attribute): The attribute to disconnect.
        """
        # make sure we do not work with open_api objects
        self._Proxy__api_instance.disconnect(self.__get_api_instance(attribute))

    def disconnectInput(self, attribute):
        """Disconnect the attribute's input.

        Arguments:
            attribute (str, Attribute): The attribute to disconnect.
        """
        # make sure we do not work with open_api objects
        self._Proxy__api_instance.disconnect_input(self.__get_api_instance(attribute))

    def disconnectOutput(self, source, destinations=None):
        """Disconnect the attribute from its output(s).

        Keyword Arguments:
            source (str, Attribute): The source attribute to connect.
            destinations (str, Attribute, list, optional): The destination attributes
                to disconnect. If None, disconnect them all. Default to None.
        """
        # make sure we do not work with open_api objects
        source = self.__get_api_instance(source)
        destinations = (self.__get_api_instance(d) for d in destinations)
        # disconnect the attributes
        self._Proxy__api_instance.disconnect_output(source, destinations)


class Node(DataObject):
    """Manage the proxy nodes."""

    # attributes methods

    def addAttr(self, data_type, **data):
        """Add an attribute to the current object.

        Arguments:
            mode (int): 0 for the attribute to be an input, 1 for output.
            data_type (str): The type of attribute to create.
            data (dict): The data to deserialize with.

        Raises:
            TypeError: The given data_type isn't valid.

        Returns:
            InputAttribute: The created attribute.
        """
        return InputAttribute(
            self._Proxy__api_instance.add_attribute(0, False, data_type, **data)
        )

    def getAttr(self, name):
        """Get an attribute using its name.

        Arguments:
            name (str): The name of the attribute.

        Raises:
            KeyError: Tried to access non-existing attribute.

        Returns:
            InputAttribute, OutputAttribute: The desired attribute.
        """
        attribute = self._Proxy__api_instance.get_attribute(name)
        if attribute:
            if attribute.is_input:
                return InputAttribute(attribute)
            return OutputAttribute(attribute)

    def getAttrs(self):
        """Get all the attributes on the current Node.

        Returns:
            list: The list of all the attributes on the current Node.
        """
        attrs = list()
        for attribute in self._Proxy__api_instance.attributes:
            if attribute.is_input:
                attrs.append(InputAttribute(attribute))
            else:
                attrs.append(OutputAttribute(attribute))
        return attrs

    def removeAttr(self, name):
        """Delete each and every attribute on this node.

        Arguments:
            name (str): The name of the attribute.
        """
        self._Proxy__api_instance.remove_attribute(name)

    def removeAllAttr(self):
        """Remove all the attributes from the current node."""
        self._Proxy__api_instance.remove_attributes()

    def listAttr(self):
        """List all the attributes on the current Node.

        Returns:
            list: The list of all the attributes names on the current Node.
        """
        return [attr.name for attr in self._Proxy__api_instance.attributes]

    # data management

    def get(self, name):
        """Query an attribute's value.

        Arguments:
            name (str): The name of the attribute to query.

        Returns:
            any: The value to the attribute.
        """
        return self._Proxy__api_instance.get(name)

    def set(self, name, value):
        """Edit an attribute's value.

        Arguments:
            name (str): The name of the attribute to edit.
            value (any): The value to set for the attribute.
        """
        self._Proxy__api_instance.set(name, value)

    def query(self, name, parameter, default=False):
        """Query an attribute's value.

        Arguments:
            name (str): The name of the attribute to query.
            parameter (str): The name of the parameter to query.

        Keyword Arguments:
            default (bool, optional): True to query the default value, else False.
                Default to False.

        Returns:
            any: The value to the attribute.
        """
        return self._Proxy__api_instance.query(name, parameter, default)

    def edit(self, name, parameter, value, default=False):
        """Edit an attribute's value.

        Arguments:
            name (str): The name of the attribute to edit.
            parameter (str): The name of the parameter to edit.
            value (any): The value to set for the attribute.

        Keyword Arguments:
            default (bool, optional): True to edit the default value, else False.
                Default to False.
        """
        self._Proxy__api_instance.edit(name, parameter, value, default=default)

    def connect(self, source, *destinations, force=True):
        """Connect an attribute of this node to another.

        Arguments:
            source (str, Attribute): The source attribute to connect.
            destinations (str, Attribute, list): The destination attributes
                to connect to.

        Keyword Arguments:
            force (bool, optional): To force the connection if already connected.
                Default to True.
        """
        # make sure we do not work with open_api objects
        source = self._Proxy__get_api_instance(source)
        destinations = (self._Proxy__get_api_instance(d) for d in destinations)
        # connect the attributes
        self._Proxy__api_instance.connect(source, destinations, force=force)

    def disconnect(self, attribute):
        """Disconnect an attribute of this node from its input and outputs.

        Arguments:
            attribute (str): The name of the attribute to disconnect.
        """
        # make sure we do not work with open_api objects
        self._Proxy__api_instance.disconnect(self._Proxy__get_api_instance(attribute))

    def disconnectInput(self, attribute):
        """Disconnect an attribute of this node's input.

        Arguments:
            attribute (str): The name of the attribute to disconnect.
        """
        # make sure we do not work with open_api objects
        self._Proxy__api_instance.disconnect_input(
            self._Proxy__get_api_instance(attribute)
        )

    def disconnectOutput(self, source, destinations=None):
        """Disconnect an attribute of this node from its output(s).

        Arguments:
            source (str): The name of the attribute to disconnect.

        Keyword Arguments:
            destinations (str, list, optional): The destination attributes
                to disconnect. If None, disconnect them all. Default to None.
        """
        # make sure we do not work with open_api objects
        source = self._Proxy__get_api_instance(source)
        destinations = (self._Proxy__get_api_instance(d) for d in destinations)
        # disconnect the attributes
        self._Proxy__api_instance.disconnect_output(source, destinations)


class Attribute(DataObject):
    """Manage the proxy attributes."""

    def get(self):
        """Get the value of the current attribute.

        Returns:
            -: The value of the current attribute.
        """
        return self._Proxy__api_instance.get()

    def connect(self, destinations, force=True):
        """Connect this attribute to another.

        Arguments:
            destinations (str, Attribute, list): The destination attributes
                to connect to.

        Keyword Arguments:
            force (bool, optional): To force the connection if already connected.
                Default to True.

        Raises:
            RuntimeError:
                | - One of the attributes isn't valid.
                | - Can't connect because some attributes
                do not live in the same network.
        """
        # make sure we do not work with open_api objects
        destinations = (self._Proxy__get_api_instance(d) for d in destinations)
        # connect the attributes
        self._Proxy__api_instance.connect(destinations, force)

    def disconnect(self):
        """Disconnect the attributes."""
        self._Proxy__api_instance.disconnect()

    def disconnectOutput(self, destinations=None):
        """Disconnect the attribute from its output(s).

        Keyword Arguments:
            destinations (str, Attribute, list, optional): The destination attributes
                to disconnect. If None, disconnect them all. Default to None.
        """
        # make sure we do not work with open_api objects
        destinations = (self._Proxy__get_api_instance(d) for d in destinations)
        # disconnect the attributes
        self._Proxy__api_instance.disconnect_output(destinations)


class InputAttribute(Attribute):
    """Manage the proxy input attributes."""

    def set(self, value):
        """Set the value of the current attribute.

        Arguments:
            value (-): The value of the current attribute.
        """
        self._Proxy__api_instance.set(value)

    def query(self, name, default=False):
        """Query a parameter value.

        Arguments:
            name (str): The name of the parameter to query.

        Keyword Arguments:
            default (bool, optional): True to query the default value, else False.
                Default to False.

        Returns:
            any: The value to the parameter.
        """
        return self._Proxy__api_instance.query(name, default)

    def edit(self, name, value, default=False):
        """Edit a parameter value.

        Arguments:
            name (str): The name of the parameter to edit.
            value (any): The value to set for the parameter.

        Keyword Arguments:
            default (bool, optional): True to edit the default value, else False.
                Default to False.
        """
        self._Proxy__api_instance.query(name, value, default)

    def reset(self):
        """Reset the attribute's value to its default."""
        self._Proxy__api_instance.reset()

    def resetToFactory(self):
        """Reset all the parameters of the attribute."""
        self._Proxy__api_instance.reset_to_factory()

    def disconnectInput(self):
        """Disconnect the attributes from its input and outputs."""
        self._Proxy__api_instance.disconnect_input()


class OutputAttribute(Attribute):
    """Manage the proxy output attributes."""


# customization


class BaseNode(object):
    """Create a class designed to be inherited and to create custom nodes."""

    inputs = None  # list : A list of dictonaries to create input attributes
    outputs = None  # list : A list of dictonaries to create output attributes

    def compute(self, inputs):
        """Perform some action when the node gets evaluated.

        Arguments:
            inputs (dict): A dictionary of input attributes names and their value.

        Returns:
            dict: A dictionary containing the value for each output attribute.
        """
        outputs = dict()
        return outputs


def node_input(data_type, **data):
    """Generate the a node's input attribute.

    Arguments:
        data_type (str): The data type of the attribute to create.
        name (str): The name to give to the attribute.

    Returns:
        str: The necessary data to generate the attribute.
    """
    # create the attribute
    data["parent"] = None
    data["is_builtin"] = False
    attribute = attributes.AttributeBuilder(0, data_type, **data)

    # make sure all the parameters are set
    for param, value in data.items():
        if param in attribute.parameters:
            attribute.edit(param, value, default=param.endswith("_default"))
        elif param == "default":
            if "value" not in data:
                attribute.edit("value", value)
            attribute.edit("value", value, default=True)

    # return the serialized attribute
    return attribute.serialize()


def node_output(data_type, **data):
    """Generate the a node's output attribute.

    Arguments:
        data_type (str): The data type of the attribute to create.

    Returns:
        str: The necessary data to generate the attribute.
    """
    data["parent"] = None
    data["is_builtin"] = False
    attribute = attributes.AttributeBuilder(1, data_type, **data)
    return attribute.serialize()
