"""Manage the common behavior of all the data objects."""

from lbx_pipeline.api.abstract import serializable_objects


class DataObject(serializable_objects.SerializableObject):
    """Manage the common behavior of all the data objects."""

    path_separator = "."

    # private variables
    name = None
    _parent = None

    def __init__(self, parent, **data):
        """Initialize the object.

        Arguments:
            parent (Object): The parent of the current object.
        """
        # inheritance
        super(DataObject, self).__init__()

        # intialize the variables
        self.parent = parent
        self.data_type = self.__class__.__name__

        # intialize the object
        self.initialize(**data)

        # deserialize the object
        self.deserialize(**data)

    def __str__(self):
        """Override the __repr__ method.

        Returns:
            str: The object as a string.
        """
        return self.path

    def __repr__(self):
        """Override the __repr__ method.

        Returns:
            str: The new representation of the object.
        """
        return "({}){}".format(self.data_type, self.path)

    def __eq__(self, other):
        """Override the __eq__ method.

        Returns:
            bool: True if equal else False.
        """
        return self.path == other

    def __ne__(self, other):
        """Override the __ne__ method.

        Returns:
            bool: True if different else False.
        """
        return self.path != other

    def __gt__(self, other):
        """Override the __gt__ method.

        Returns:
            bool: True if greater, else False.
        """
        return self.path < other

    def __lt__(self, other):
        """Override the __lt__ method.

        Returns:
            bool: True if lower, else False.
        """
        return self.path > other

    def __ge__(self, other):
        """Override the __ge__ method.

        Returns:
            bool: True if greater or equal, else False.
        """
        return self.path <= other

    def __le__(self, other):
        """Override the __le__ method.

        Returns:
            bool: True if lower or equal, else False.
        """
        return self.path >= other

    # methods

    def initialize(self, **data):
        """Initialize the object before deserializing it.

        Arguments:
            data (dict): The data to deserialize with.
        """

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(DataObject, self).serialize()
        data["data_type"] = self.data_type
        data["name"] = self.name
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            data (dict): The data to deserialize with.
        """
        super(DataObject, self).deserialize(**data)
        self.name = data.get("name")

    # custom methods

    def get_path(self, relative_to=None):
        """Get the path of the current object in its parent hierarchy.

        Keyword Arguments:
            relative_to (str, optional): The path to get the relative path from.
                Default to None.

        Returns:
            str: The path of the current object.
        """
        if isinstance(self.parent, DataObject):
            path = self.parent.get_path(relative_to)
            if path != relative_to:
                return path + self.path_separator + self.name
        return self.name

    path = property(get_path)
