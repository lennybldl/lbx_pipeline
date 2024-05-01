"""Manage the nodes."""

from lbx_plumber.api import attributes
from lbx_plumber.api.abstract import features
from lbx_plumber.internal import core


class Node(features.GraphicFeature):
    """Manage the base class for nodes."""

    category = core.Features.NODE

    # private variables
    _is_dirty = False

    # methods

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        # create storage variables
        self.attributes_by_name = dict()

        # inheritance
        super(Node, self).__init__(*args, **kwargs)

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(Node, self).serialize()
        if self.attributes:
            data["attributes"] = [o.serialize() for o in self.attributes]
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            compute (callable): The compute function to call to compute the node.
            data (dict): The data to deserialize with.
        """
        # inheritance
        super(Node, self).deserialize(**data)

        # update the data type of the node
        self.data_type = data.get("data_type", self.data_type)

        # keep in memory the methods to call
        self.compute = data.get("compute")
        if self.compute is None:
            raise ValueError("A node needs at least a 'compute' method")

        # initialize the input and output attributes
        self.inputs = [
            self.add_attribute(0, True, **d) for d in data.get("inputs") or list()
        ]
        self.outputs = [
            self.add_attribute(1, True, **d) for d in data.get("outputs") or list()
        ]

        # initialize the attributes
        for attribute_data in data.get("attributes", list()):
            attribute = self.attributes_by_name.get(attribute_data["name"])
            if attribute:
                self.set(**attribute_data)
            else:
                self.add_attribute(0, False, **attribute_data)

    def delete(self):
        """Delete the current data structure."""
        # make sure every attributes are deleted
        for attribute in self.attributes:
            attribute.delete(force=True)

        # inheritance
        super(Node, self).delete()

    # evaluation methods

    def get_is_dirty(self):
        """Get if the object is dirty.

        Returns:
            bool: True if the attribute is dirty else, False.
        """
        return self._is_dirty

    def set_is_dirty(self, value):
        """Set the current object dirty or not.

        Arguments:
            value (bool): True to set the object dirty else False.
        """
        self._is_dirty = value
        if value:
            self.parent.eval(self)

    is_dirty = property(get_is_dirty, set_is_dirty)

    def eval(self, force=False):
        """Evaluate the current node.

        Keyword Arguments:
            force (bool, optional): Force the node's evaluation even if not needed.
                Default to False.
        """
        # skip if the evaluation isn't necessary
        if not force and not self.is_dirty:
            return

        # get the inputs
        inputs = {o.name: o.get() for o in self.inputs}
        # compute the outputs
        outputs = self.compute(self, inputs)

        # set the node to be clean
        self.is_dirty = False

        # update the output attributes
        for name, value in outputs.items():
            self.set(name, value)

    # attributes methods

    def add_attribute(self, mode, is_builtin, data_type, **data):
        """Add an attribute to the current object.

        Arguments:
            mode (int): 0 for the attribute to be an input, 1 for output.
            is_builtin (bool): True if the attribute comes with feature, else False.
            data_type (str): The type of attribute to create.
            data (dict): The data to deserialize with.

        Raises:
            TypeError: The given data_type isn't valid.

        Returns:
            Attribute: The created attribute.
        """
        # create the attribute
        data["parent"] = self
        data["is_builtin"] = is_builtin
        attribute = attributes.AttributeBuilder(mode, data_type, **data)
        return attribute

    def remove_attribute(self, name):
        """Delete each and every attribute on this node.

        Arguments:
            name (str): The name of the attribute.
        """
        attribute = self.get_attribute(name)
        attribute.delete()

    def remove_attributes(self):
        """Delete each and every attribute on this node."""
        for attribute in self.attributes:
            if not attribute.is_builtin:
                attribute.delete()

    def get_attribute(self, name):
        """Get an attribute using its name.

        Arguments:
            name (str): The name of the attribute.

        Raises:
            KeyError: Tried to access non-existing attribute.

        Returns:
            Attribute: The attribute we asked for.
        """
        attribute = self.attributes_by_name.get(name)
        if attribute:
            return attribute
        raise KeyError(
            "Tried to access non-existing attribute '{}' on '{}'".format(name, self)
        )

    def get_attributes(self):
        """Get the list of attributes on the current object.

        Returns:
            list: The current attributes.
        """
        return self.attributes_by_name.values()

    attributes = property(get_attributes)

    # data management

    def get(self, name):
        """Query an attribute's value.

        Arguments:
            name (str): The name of the attribute to query.

        Returns:
            any: The value to the attribute.
        """
        return self.get_attribute(name).get()

    def set(self, name, value):
        """Edit an attribute's value.

        Arguments:
            name (str): The name of the attribute to edit.
            value (any): The value to set for the attribute.
        """
        self.get_attribute(name).set(value)

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
        return self.get_attribute(name).query(parameter, default=default)

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
        self.get_attribute(name).edit(parameter, value, default=default)

    def connect(self, source, destinations, force=True):
        """Connect an attribute to another.

        Arguments:
            source (str, Attribute): The source attribute to connect.
            destinations (str, Attribute, list): The destination attributes
                to connect to.

        Keyword Arguments:
            force (bool, optional): To force the connection if already connected.
                Default to True.
        """
        self.get_attribute(source).connect(destinations, force=force)

    def disconnect(self, attribute):
        """Disconnect an attribute of this node from its input and outputs.

        Arguments:
            attribute (str, Attribute): The attribute to disconnect.
        """
        self.get_attribute(attribute).disconnect()

    def disconnect_input(self, attribute):
        """Disconnect an attribute of this node's input.

        Arguments:
            attribute (str, Attribute): The attribute to disconnect.
        """
        self.get_attribute(attribute).disconnect_input()

    def disconnect_output(self, attribute, destinations=None):
        """Disconnect an attribute of this node from its output(s).

        Arguments:
            attribute (str, Attribute): The attribute to disconnect.

        Keyword Arguments:
            destinations (str, Attribute, list, optional): The destination attributes
                to disconnect. If None, disconnect them all. Default to None.
        """
        self.get_attribute(attribute).disconnect_output(destinations)
