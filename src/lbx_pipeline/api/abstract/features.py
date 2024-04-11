"""Manage the common behavior of all the features."""

from lbx_pipeline.api.abstract import data_structures


class Feature(data_structures.DataStructure):
    """Manage the common behavior of all the features."""

    category = "features"
    default_storage_variable = "features"

    # private variables

    def __new__(cls, category=None, data_type=None, **data):
        """Create a new data object.

        Arguments:
            category (str): The category of object to add (nodes, macros, etc.).
            data_type (str): The type of data the object holds.
                This can be attribute types as well as node types.

        Keyword Arguments:
            name (str, optional): The name to give to the object. Default to None.

        Returns:
            instance: The created object.
        """
        # create the instance
        instance = super(Feature, cls).__new__(cls)

        # avoid recursion for subclasses
        if cls != Feature:
            return instance

        # figure out the subclass to create
        # get the type of data object that can be added
        data_manager = cls.manager.data_manager
        data_types = data_manager.features.get(category)
        if not data_types:
            cls.project_logger.error("Invalid category '{}'".format(category))
            cls.project_logger.debug(
                "The valid types are : {}".format(list(data_manager.features.keys()))
            )
            return

        # get the data object class of the object to create
        object_class = data_types.get(data_type)
        if not object_class:
            cls.project_logger.error("Invalid data type '{}'".format(category))
            cls.project_logger.debug(
                "The valid types are : {}".format(list(data_types.keys()))
            )
            return

        # initialize the correct data object
        return object_class.__new__(object_class, **data)

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(Feature, self).serialize()
        data["category"] = self.category
        return data


class GraphicFeature(Feature):
    """Manage the common behavior of all the graphic features."""

    icon = None
    position = (0, 0)
    size = (10, 10)

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(GraphicFeature, self).serialize()
        data["position"] = self.position
        data["size"] = self.size
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            data (dict): The data to deserialize with.
        """
        super(GraphicFeature, self).deserialize(**data)
        self.position = data.get("position", self.position)
        self.size = data.get("size", self.size)


class NodalFeature(GraphicFeature):
    """Manage the common behavior of all the nodal features."""

    # private variables
    _attributes = None

    # methods

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(NodalFeature, self).serialize()
        if self.attributes:
            data["attributes"] = [o.serialize() for o in self.attributes.values()]
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            data (dict): The data to deserialize with.
        """
        super(NodalFeature, self).deserialize(**data)
        [self.add_attribute(**d) for d in data.get("attributes", list())]

    # data objects methods

    def add_attribute(self, data_type, **data):
        """Add an attribute to the current object.

        Arguments:
            data_type (str): The type of attribute to create.
            data (dict): The data to deserialize with.

        Returns:
            Attribute: The created attribute.
        """
        # create the attribute
        attribute_class = self.data_manager.attributes.get(data_type)
        if not attribute_class:
            raise TypeError("No valid data_type given : {}".format(data_type))

        # create the attribute
        data["parent"] = self
        data["storage_variable"] = "attributes"
        attribute = attribute_class(**data)
        return attribute

    def get_attribute(self, name):
        """Get an attribute using its name.

        Arguments:
            name (str): The name of the attribute.

        Raises:
            KeyError: Tried to access non-existing attribute.

        Returns:
            Attribute: The attribute we asked for.
        """
        attribute = self.attributes.get(name)
        if attribute:
            return attribute
        raise KeyError("Tried to access non-existing attribute '{}'".format(name))

    def get_attributes(self):
        """Get the list of attributes on the current object.

        Returns:
            dict: The current attributes.
        """
        if self._attributes is None:
            self._attributes = dict()
        return self._attributes

    attributes = property(get_attributes)

    def query(self, name, param="value", default=False):
        """Query an attribute value.

        Arguments:
            name (str): The name of the attribute to query.

        Keyword Arguments:
            param (str, optional): The name of the parameter to query.
                Default to "value".
            default (bool, optional): True to query the default value, else False.
                Default to False.

        Returns:
            any: The value to the attribute.
        """
        attribute = self.get_attribute(name)
        return attribute.query(param, default=default)

    def edit(self, name, value, param="value", default=False):
        """Edit an attribute value.

        Arguments:
            name (str): The name of the attribute to edit.
            value (any): The value to set for the attribute.

        Keyword Arguments:
            name (str, optional): The name of the parameter to edit.
                Default to "value".
            default (bool, optional): True to edit the default value, else False.
                Default to False.
        """
        attribute = self.get_attribute(name)
        return attribute.edit(param, value, default=default)
