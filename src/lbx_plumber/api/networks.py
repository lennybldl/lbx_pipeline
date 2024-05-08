"""Manage the common behavior of all the data items."""

import six

from lbx_plumber.api import attributes, dependency_graphs
from lbx_plumber.api.abstract import data_structures, features
from lbx_plumber.internal import common


class Network(data_structures.DataStructure):
    """Manage the common behavior of all the data items."""

    storage_variable = "networks"

    # methods

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        # create storage variables
        self.features_by_uuid = dict()
        self.features_by_name = dict()

        # add a dependency graph to the network
        self._dependency_graph = dependency_graphs.DependencyGraph()
        self._evaluation_queue = set()

        # inheritance
        super(Network, self).__init__(*args, **kwargs)

    def serialize(self):
        """Serialize the object's features.

        Returns:
            dict: The object's features serialization.
        """
        data = super(Network, self).serialize()
        data["features"] = [o.serialize() for o in self.features]

        # serialize the connections
        data["connections"] = connections = dict()
        network_path = self.path
        for feature in self.features:
            for attribute in feature.attributes:
                out_attributes = attribute.out_attributes
                if out_attributes:
                    connections[attribute.get_path(relative_to=network_path)] = [
                        o.get_path(relative_to=network_path) for o in out_attributes
                    ]
        return data

    def deserialize(self, **data):
        """Deserialize the object's features.

        Arguments:
            data (dict): The data to deserialize with.
        """
        super(Network, self).deserialize(**data)

        # suspend the evaluation
        self.manager.set_evaluation_suspended(True)

        # add the features
        for d in data.get("features", list()):
            self.add_feature(**d)

        # connect the created features
        for s, d in data.get("connections", dict()).items():
            self.connect(s, d)

        # suspend the evaluation
        self.manager.set_evaluation_suspended(False)

    def eval(self, *nodes, force=False):
        """Evaluate every nodes within the network.

        If the evaluation is suspended, add the node to the list of nodes to evaluate
        when the evaluation is restored.

        Keyword Arguments:
            nodes (Node, list, optional): The nodes to evaluate.
                If none, evaluate them all. Default to None.
            force (bool, optional): Force the node's evaluation even if not needed.
                Default to False.
        """
        # add the node to the list of nodes to evaluate
        for node in nodes or self.list_nodes():
            self._evaluation_queue.add(node.uuid)

        # skip if the evaluation is suspended
        if self.manager.is_evaluation_suspended:
            return

        # get the evaluation order and reset the evaluation queue
        order = self._dependency_graph.get_evaluation_order(self._evaluation_queue)
        self._evaluation_queue.clear()

        # evaluate the nodes in the optimal order
        for uuid in order:
            self.get_feature_by_uuid(uuid).eval(force=force)

    # data objects methods

    def add_feature(self, category, data_type, **data):
        """Add a feature to the current object.

        Arguments:
            category (str): The category of object to add (nodes, etc.).
            data_type (str): The type of feature to create.
            data (dict): The data to deserialize with.

        Returns:
            Feature: The created feature.
        """
        # create the feature and add it to the current object
        data["parent"] = self
        feature = features.FeatureBuilder(category, data_type, **data)
        return feature

    def get_feature(self, name):
        """Get a feature using its name.

        Arguments:
            name (str): The name of the feature.

        Raises:
            KeyError: Tried to access non-existing feature.

        Returns:
            Feature: The feature we asked for.
        """
        feature = self.features_by_name.get(name)
        if feature:
            return feature
        raise KeyError(
            "Tried to access non-existing feature '{}' in '{}'".format(name, self)
        )

    def get_feature_by_uuid(self, uuid):
        """Get a feature using its uuid.

        Arguments:
            uuid (str): The uuid of the feature.

        Raises:
            KeyError: Tried to access non-existing feature.

        Returns:
            Feature: The feature we asked for.
        """
        feature = self.features_by_uuid.get(uuid)
        if feature:
            return feature
        raise KeyError(
            "Tried to access non-existing feature '{}' in '{}'".format(uuid, self)
        )

    def get_features(self):
        """Get the list of features on the current object.

        Returns:
            list: The current features.
        """
        return self.features_by_uuid.values()

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

    def get_node(self, name):
        """Get a node using its name.

        Arguments:
            name (str): The name of the node.

        Returns:
            Node: The desired node.
        """
        node = self.get_feature(name)
        if node.category is common.Features.NODE:
            return node

    def list_nodes(self):
        """List the nodes of the current network.

        Returns:
            list: The list of nodes the network is hosting.
        """
        nodes = list()
        for feature in self.features:
            if feature.category is common.Features.NODE:
                nodes.append(feature)
        return nodes

    # connection methods

    def _get_attribute(self, attribute):
        """Get an attribute on a node of the current network.

        Arguments:
            attribute (str, Attribute): The attribute to get.

        Raises:
            ValueError: The given attribyte doesn't live in the current network.

        Returns:
            Attribute: The attribute we are looking for if it exists.
        """
        if isinstance(attribute, attributes.Attribute):
            # make sure the given attribute belongs to this network
            if attribute.parent.parent is self:
                return attribute
            raise ValueError(
                "The attribute ({}) doesn't live in the current network ({})".format(
                    attribute, self
                )
            )

        # get the attribute from a string
        elif isinstance(attribute, six.string_types):
            node, attribute = attribute.split(".", 1)
            return self.get_node(node).get_attribute(attribute)

    def connect(self, source, destinations, force=True):
        """Connect an attribute to another.

        Arguments:
            source (str, Attribute): The source attribute to connect.
            destinations (list): The destination attributes to connect to.

        Keyword Arguments:
            force (bool, optional): To force the connection if already connected.
                Default to True.

        Raises:
            RuntimeError:
                | - No destinations given.
                | - The destination is already connected.
            RecursionError: The connection would create a dependency cycle.
        """
        # skip if no destinations
        if not destinations:
            raise RuntimeError(
                "The source must be given at least one destination to connect to"
            )

        # get the sources and destinations as attributes
        source = self._get_attribute(source)
        destinations = (self._get_attribute(d) for d in destinations)

        # parse every destinations
        for destination in destinations:
            # make sure the source and destination aren't already connected together
            in_attribute = destination.in_attribute
            if in_attribute is self:
                self.project_logger.warning(
                    "'{}' and '{}' are already connected".format(self, destination)
                )
                continue

            # make sure the destination isn't already connected
            if in_attribute:
                if not force:
                    raise RuntimeError(
                        "'{}' already has an input connection".format(destination)
                    )
                destination.disconnect_input(in_attribute)

            # make sure that connecting the attribute won't create a cyle
            dp = self._dependency_graph
            dp.add_dependency(source, destination)
            if dp.has_cycle(source):
                dp.remove_dependency(source)
                raise RecursionError(
                    "Connecting '{}' and '{}' would create a dependency cyle".format(
                        source, destination
                    )
                )
            # connect the attributes together
            destination.in_attribute = source
            source.out_attributes.append(destination)

    def disconnect(self, attribute):
        """Disconnect the attributes from its input and outputs.

        Arguments:
            attribute (str, Attribute): The attribute to disconnect.
        """
        self.disconnect_input(attribute)
        self.disconnect_output(attribute)

    def disconnect_input(self, attribute):
        """Disconnect the attribute's input.

        Arguments:
            attribute (str, Attribute): The attribute to disconnect.
        """
        attribute = self._get_attribute(attribute)
        if not attribute.is_input:
            return

        # get the input attribute
        in_attribute = attribute.in_attribute
        if not in_attribute:
            self.project_logger.warning("'{}' is not connected".format(self))
            return

        # remove the dependency
        self._dependency_graph.remove_dependency(attribute)

        # disconnect the attribute
        in_attribute.out_attributes.pop(attribute, None)
        attribute.in_attribute = None

    def disconnect_output(self, source, destinations=None):
        """Disconnect the attribute from its output(s).

        Keyword Arguments:
            source (str, Attribute): The source attribute to connect.
            destinations (str, Attribute, list, optional): The destination attributes
                to disconnect. If None, disconnect them all. Default to None.
        """
        # get the sources and destinations as attributes
        source = self._get_attribute(source)
        destinations = (self._get_attribute(d) for d in destinations)

        # get the destination attributes to disconnect
        to_disconnect = source.out_attributes
        if destinations:
            to_disconnect = [o for o in to_disconnect if o in destinations]

        if to_disconnect:
            # remove the attribute from its out_attributes
            for attribute in to_disconnect:
                # remove the dependency
                self._dependency_graph.remove_dependency(attribute)
                # remove the input connection
                attribute.in_attribute = None

            # reset the out_attributes variable
            source.out_attributes = list()
