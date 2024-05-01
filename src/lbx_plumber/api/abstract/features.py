"""Manage the common behavior of all the features."""

from lbx_plumber.api.abstract import objects, data_structures


class FeatureBuilder(objects.Object):
    """Manage the features building."""

    def __new__(cls, category, data_type, **data):
        """Builder a feature.

        Keyword Arguments:
            category (str): The category of object to add (nodes, etc.).
            data_type (str): The type of data the object holds.
                This can be attribute types as well as node types.
            data (dict): The data to deserialize with.

        Raises:
            TypeError: Invalid category.
            TypeError: Invalid data type.

        Returns:
            Feature: The created feature.
        """
        # get the data manage that holds all the availables features data
        data_manager = cls.manager.data_manager

        # get the type of data object that can be added
        data_types = data_manager.features.get(category)
        if not data_types:
            cls.project_logger.debug(
                "The valid types are : {}".format(list(data_manager.features.keys()))
            )
            raise TypeError("Invalid category '{}'".format(category))

        # get the data object class of the object to create
        feature_data = data_types.get(data_type)
        if not feature_data:
            cls.project_logger.debug(
                "The valid types are : {}".format(list(data_types.keys()))
            )
            raise TypeError("Invalid data type '{}'".format(data_type))

        # initialize the correct data object
        object_class = feature_data.get("class")
        return object_class(
            **{
                k: v
                for k, v in list(data.items()) + list(feature_data.get("data").items())
            }
        )


class Feature(data_structures.DataStructure):
    """Manage the common behavior of all the features."""

    category = None
    storage_variable = "features"
    path_separator = "|"

    def __init__(self, *args, **data):
        """Initialize the object."""
        # inheritance
        super(Feature, self).__init__(*args, **data)

        # register the object to its parent by its uuid
        if self.parent:
            variable = getattr(self.parent, self.storage_variable + "_by_uuid")
            variable[self.uuid] = self

    # methods

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
