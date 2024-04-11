"""Manage the project."""

from lbx_python import dictionaries, system

from lbx_pipeline.api import networks
from lbx_pipeline.api.abstract import serializable_objects
from lbx_pipeline.internal import core


class Project(system.File, serializable_objects.SerializableObject):
    """Manage the project."""

    # management

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        # create storage variables
        self.networks_by_name = dict()

        # inheritance
        super(Project, self).__init__(*args, **kwargs)

    def create(self):
        """Create the project."""
        # make sure the project path is valid
        if self.exists():
            raise RuntimeError(
                "The given project path conflicts with another : '{}'".format(self)
            )
        if not self.extension == core.PROJECT_EXTENSION:
            raise ValueError("The given project path isn't valid : '{}'".format(self))

        # inheritance
        super(Project, self).create("{}")
        # load the project
        self.load()

    def load(self, path=None):
        """Load the project.

        Keyword Arguments:
            path (str, optional): The path to the project to load.
                Default to None.
        """
        # make sure the project path is valid
        path = system.File(path or self)
        if not path.is_file or not path.extension == core.PROJECT_EXTENSION:
            raise ValueError("The given project path isn't valid : '{}'".format(path))

        # load the project's data
        self.path = path
        data = dictionaries.Dictionary(self)
        self.deserialize(**data)

    def save(self, path=None, *args, **kwargs):
        """Save the current project.

        Keyword Arguments:
            path (str, optional): The path where to save the project as.
                Default to None.
        """
        # make sure the project path is valid
        path = system.File(path or self)
        if path.extension != core.PROJECT_EXTENSION:
            raise ValueError("The given project path isn't valid : '{}'".format(path))

        # save the data
        data = dictionaries.Dictionary(self.serialize())
        data.dump(path, *args, **kwargs)
        # update the variables
        self.path = path
        self.project_logger.name = self.name

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(Project, self).serialize()
        data["networks"] = [o.serialize() for o in self.networks]
        return data

    def deserialize(self, **data):
        """Deserialize the object's features.

        Arguments:
            data (dict): The data to deserialize with.
        """
        super(Project, self).deserialize(**data)

        # add the networks
        for d in data.get("networks", list()):
            self.add_network(**d)

    # methods

    def set_name(self, name):
        """Set the name of the project.

        Arguments:
            name (str): The project's name.
        """
        super(Project, self).set_name(name)
        self.project_logger.set_name(name)

    name = property(system.File.get_name, set_name)

    # data management

    def add_network(self, **data):
        """Add a network to the current project.

        Returns:
            Network: The created network.
        """
        data["parent"] = self
        return networks.Network(**data)

    def get_network(self, name):
        """Get a network using its name.

        Arguments:
            name (str): The name of the network.

        Raises:
            KeyError: Tried to access non-existing network.

        Returns:
            Network: The network we asked for.
        """
        network = self.networks_by_name.get(name)
        if network:
            return network
        raise KeyError(
            "Tried to access non-existing network '{}' in '{}'".format(name, self)
        )

    def get_networks(self):
        """Get the list of networks on the current object.

        Returns:
            list: The current networks.
        """
        return self.networks_by_name.values()

    networks = property(get_networks)
