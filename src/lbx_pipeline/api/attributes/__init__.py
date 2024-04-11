"""Manage the attributes."""

from lbx_pipeline.api.abstract import objects, data_structures


class AttributeBuilder(objects.Object):
    """Manage the attributes building."""

    def __new__(cls, mode, data_type, **data):
        """Create attributes from data.

        Arguments:
            mode (int): 0 for an input attribute, 1 for an output.
            data_type (str): The data type of the attribute to create.

        Raises:
            TypeError: Invalid data type.

        Returns:
            Attribute: The created attribute.
        """
        # get the data manage that holds all the available attributes data
        data_manager = cls.manager.data_manager

        # get the available data types
        if mode:
            data_types = data_manager.output_attributes
        else:
            data_types = data_manager.input_attributes

        # get the type of data object that can be added
        object_class = data_types.get(data_type)
        if not object_class:
            cls.project_logger.debug(
                "The valid types are : {}".format(list(data_types.keys()))
            )
            raise TypeError("Invalid data type '{}'".format(data_type))

        # initialize the correct data object
        return object_class(**data)


class Attribute(data_structures.DataStructure):
    """Manage the base class for the attribute."""

    storage_variable = "attributes"

    # methods

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        if self.is_builtin:
            return {"name": self.name, "value": self.get()}
        return super(Attribute, self).serialize()

    def deserialize(self, is_builtin, **data):
        """Deserialize the object.

        Arguments:
            is_builtin (bool): True if the attribute comes with feature, else False.
            data (dict): The data to deserialize with.
        """
        # initialize the variables before deserializing
        self.is_builtin = is_builtin
        self.out_attributes = list()

        # inheritance
        super(Attribute, self).deserialize(**data)

    def delete(self, force=False):
        """Delete the current attribute.

        Keyword Arguments:
            force (bool, optional): To delete the attribute even if it is not allowed.
                Default to False.

        Raises:
            RuntimeError: The attribute cannot be deleted.
        """
        if self.is_builtin and not force:
            raise RuntimeError(
                "A builtin attribute cannot be deleted ('{}')".format(self)
            )

        # make sure the attribute is disconnected
        self.disconnect()

        # inheritance
        super(Attribute, self).delete()

    # data management

    def connect(self, destinations, force=True):
        """Connect an attribute to another.

        Arguments:
            source (str, Attribute): The source attribute to connect.
            destinations (list): The destination attributes to connect to.

        Keyword Arguments:
            force (bool, optional): To force the connection if already connected.
                Default to True.
        """
        # call the connect methods from the attribute's network
        self.parent.parent.connect(self, destinations, force=force)

    def disconnect(self):
        """Disconnect the attributes."""
        self.parent.parent.disconnect(self)

    def disconnect_output(self, destinations=None):
        """Disconnect the attribute from its output(s).

        Keyword Arguments:
            destinations (str, Attribute, list, optional): The destination attributes
                to disconnect. If None, disconnect them all. Default to None.
        """
        self.parent.parent.disconnect_output(self, destinations)
