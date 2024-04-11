"""Manage the common behavior of all the data items."""

from lbx_pipeline.api.abstract import features, serializable_objects


class Network(serializable_objects.SerializableObject):
    """Manage the common behavior of all the data items."""

    # private variables
    _features = None

    # methods

    def serialize(self):
        """Serialize the object's features.

        Returns:
            dict: The object's features serialization.
        """
        data = super(Network, self).serialize()
        data["features"] = [o.serialize() for o in self.features.values()]
        return data

    def deserialize(self, **data):
        """Deserialize the object's features.

        Arguments:
            data (dict): The data to deserialize with.
        """
        super(Network, self).deserialize(**data)
        [self.add_feature(**d) for d in data.get("features", list())]

    # data objects methods

    def add_feature(self, category, data_type, **data):
        """Add a feature to the current object.

        Arguments:
            category (str): The category of object to add (nodes, macros, etc.).
            data_type (str): The type of feature to create.
            data (dict): The data to deserialize with.

        Returns:
            Feature: The created feature.
        """
        # create the feature and add it to the current object
        data["parent"] = self
        data["storage_variable"] = "features"
        feature = features.Feature(category, data_type, **data)
        return feature

    def get_feature(self, name):
        """Get a featrue using its name.

        Arguments:
            name (str): The name of the feature.

        Raises:
            KeyError: Tried to access non-existing feature.

        Returns:
            Feature: The feature we asked for.
        """
        feature = self.features.get(name)
        if feature:
            return feature
        raise KeyError("Tried to access non-existing feature '{}'".format(name))

    def get_features(self):
        """Get the list of features on the current object.

        Returns:
            dict: The current features.
        """
        if self._features is None:
            self._features = dict()
        return self._features

    features = property(get_features)

    def add_node(self, data_type, **data):
        """Add a node to the current object.

        Arguments:
            data_type (str): The type of node to create.
            data (dict): The data to deserialize with.

        Returns:
            Feature: The created node.
        """
        return self.add_feature("nodes", data_type, **data)

    def add_macro(self, data_type, **data):
        """Add a macro to the current object.

        Arguments:
            data_type (str): The type of macro to create.
            data (dict): The data to deserialize with.

        Returns:
            Feature: The created macro.
        """
        return self.add_feature("macros", data_type, **data)
