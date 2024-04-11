"""Manage the common behavior of all the data objects."""

from lbx_python_core import strings

from lbx_pipeline.api.abstract import serializable_objects


class DataObject(serializable_objects.SerializableObject):
    """Manage the common behavior of all the data objects."""

    category = None
    default_storage_variable = None

    # private variables
    _name = None

    def __init__(self, *args, **data):
        """Initialize the object."""
        # inheritance
        super(DataObject, self).__init__()
        # intialize the object
        self.initialize(**data)
        # deserialize the object
        self.deserialize(**data)

    def __str__(self):
        """Override the __repr__ method.

        Returns:
            str: The object as a string.
        """
        return self.data_path

    def __repr__(self):
        """Override the __repr__ method.

        Returns:
            str: The new representation of the object.
        """
        return "({}){}".format(self.data_type, self.data_path)

    # methods

    def initialize(self, **data):
        """Initialize the object before deserializing it."""

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(DataObject, self).serialize()
        data["data_type"] = self.data_type
        data["name"] = self.name
        return data

    def deserialize(self, parent, **data):
        """Deserialize the object.

        Arguments:
            parent (Object): The parent of the current object.
            data (dict): The data to deserialize with.
        """
        # make sure the parent is set first
        self.parent = parent
        self.storage_variable = data.get(
            "storage_variable", self.default_storage_variable
        )

        # inheritance
        super(DataObject, self).deserialize(**data)
        # deserialize the rest of the properties
        self.name = data.get("name")

    def get_name(self):
        """Get the name of the current data structure.

        Returns:
            str: The current data structure's name.
        """
        return self._name

    def set_name(self, name=None):
        """Set the name of the current data structure.

        Keyword Arguments:
            name (str, optional): The name we want to set for the current
                data strucuture. If None, generate a new one. Default to None.
        """
        # make sure the name is in snake case
        if name:
            name = strings.replace_specials(name, "_")

        # list the existing content
        assigned_names = dict()
        if self.storage_variable and hasattr(self.parent, self.storage_variable):
            assigned_names = getattr(self.parent, self.storage_variable)

        # remove the current name of the node from the assigned names
        assigned_names.pop(self._name, None)

        # use a unique name if None given
        if not name or name in assigned_names:
            base_name = name if name else self.data_type
            index = 1
            while not name or name in assigned_names:
                name = "{}{}".format(base_name, index)
                index += 1

        # set the name of the data structure
        self._name = name
        assigned_names[name] = self

    name = property(get_name, set_name)

    def get_data_type(self):
        """Get the type of the current data object.

        Returns:
            str: The type of the current data object.
        """
        return self.__class__.__name__

    data_type = property(get_data_type)

    # methods

    def get_data_path(self):
        """Get the full path of the current data structure.

        Returns:
            str: The full path of the current data structure.
        """
        if not hasattr(self.parent, "data_path"):
            return ".".join(["", self.name])
        return ".".join([self.parent.data_path, self.name])

    data_path = property(get_data_path)
