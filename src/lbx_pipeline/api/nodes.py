"""Manage the nodes."""

from lbx_python_core import strings

from lbx_pipeline.internal import core, logging

logger = logging.SessionLogger()


class Node(object):
    """Manage the base class for nodes."""

    def __init__(self, name, *args, **kwargs):
        """Initialize the node.

        Arguments:
            name (str): The name to give to the node.
        """
        # inheritance
        super(Node, self).__init__(*args, **kwargs)

        # initialize the properties
        self.attributes = list()

        # keep the properties in memory
        self.name = strings.remove_specials(name, keep="_")

    def __str__(self):
        """Override the __repr__ method.

        Returns:
            str: The object as a string.
        """
        return "({}){}".format(self.type, self.name)

    def __repr__(self):
        """Override the __repr__ method.

        Returns:
            str: The new representation of the object.
        """
        return self.__str__()

    # methods

    def get_type(self):
        """Get the type of the current attribute.

        Returns:
            str: The type of attribute in snake case.
        """
        return strings.pascal_case(self.__class__.__name__)

    type = property(get_type)

    def serialize(self):
        """Serialize the node.

        Returns:
            dict: The serialized node.
        """
        data = dict()
        data["attributes"] = [attribute.serialize() for attribute in self.attributes]
        return data

    # attributes methods

    def add_attribute(self, attribute_type, long_name=None, *args, **kwargs):
        """Add an attribute to the current node.

        Arguments:
            attribute_type (str): The type of attribute to create.
            long_name (str): The long name to give to the attribute.

        Keyword Arguments:
            long_name (_type_, optional): The long name to give to the attribute.
                If None, use the attribute type and an index. Default to None.

        Returns:
            Attribute: The created attribute.
        """
        # get the attribute class of the attribute to create
        attribute_class = core.ATTRIBUTE_TYPES.get(attribute_type)
        if not attribute_class:
            return logger.error(
                "Invalid attribute_type '{}'. Attribute types can be : {}".format(
                    attribute_type, core.ATTRIBUTE_TYPES.keys()
                )
            )

        # list the existing attributes
        existing_long_names = [attr.long_name for attr in self.attributes]

        # use a unique long name if None given
        if not long_name:
            index = 0
            while not long_name or long_name in existing_long_names:
                long_name = "Attribute{}".format(index)
                index += 1

        # create the attribute to the node
        attribute = attribute_class(self, long_name, *args, **kwargs)
        long_name = attribute.long_name

        # make sure the attribute name is unique
        if attribute.long_name in existing_long_names:
            return logger.error(
                "An attribute named '{}' already exists on '{}'".format(
                    long_name, self.name
                )
            )

        # add the attribute to the node
        self.attributes.append(attribute)
        return attribute
