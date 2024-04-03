"""Manage the attributes."""

from lbx_python_core import strings

from lbx_pipeline.internal import core, logging

logger = logging.SessionLogger()


class Attribute(object):
    """Manage the base class for the attribute."""

    # private variables
    _default = None

    def __init__(self, node, long_name, **kwargs):
        """Initialize the attribute.

        Arguments:
            node (Node): The node the attribute is linked to.
            long_name (str): The long name to give to the attribute.
        """
        # initialize the attribute
        super(Attribute, self).__init__()

        # initialize the variables
        self.node = node
        self.type = strings.snake_case(self.__class__.__name__.split("Attribute")[0])
        self.long_name = strings.remove_specials(long_name, keep="_")
        self.nice_name = kwargs.get("nice_name", strings.title_case(long_name))
        self.in_plugs = list()
        self.out_plugs = list()

        # add the parameters in memory
        self.parameters = list()
        default = kwargs.get("default", self._default)
        self.add_parameter(
            self.type, "value", value=kwargs.get("value", default), default=default
        )

    def __str__(self):
        """Override the __repr__ method.

        Returns:
            str: The object as a string.
        """
        return "({}){}".format(self.type, self.long_name)

    def __repr__(self):
        """Override the __repr__ method.

        Returns:
            str: The new representation of the object.
        """
        return self.__str__()

    def __eq__(self, other):
        """Override the __eq__ method.

        Returns:
            bool: True if equal else False.
        """
        return self.long_name == other

    def __ne__(self, other):
        """Override the __ne__ method.

        Returns:
            bool: True if different else False.
        """
        return self.long_name != other

    # methods

    def serialize(self):
        """Serialize the attribute.

        Returns:
            dict: The serialized attribute.
        """
        data = dict()

        # serialize the variables
        for name in ["type", "long_name", "nice_name"]:
            data[name] = getattr(self, name)

        # serialize the parameters
        for parameter in self.parameters:
            data[parameter.name] = parameter.serialize()

        return data

    # parameters methods

    def add_parameter(self, parameter_type, name, *args, **kwargs):
        """Add a parameter to the current attribute.

        Arguments:
            parameter_type (str): The type of attribute to create.
            name (str): The long name to give to the attribute.

        Returns:
            Parameter: The created parameter.
        """
        # get the parameter class of the parameter to create
        parameter_class = core.PARAMETERS_TYPES.get(parameter_type)
        if not parameter_class:
            return logger.error(
                "Invalid attribute_type '{}'. Attribute types can be : {}".format(
                    parameter_type, list(core.ATTRIBUTE_TYPES.keys())
                )
            )

        # create the parameter and link it to the current attribute
        parameter = parameter_class(self, name, *args, **kwargs)
        setattr(self.__class__, name, parameter)
        self.parameters.append(parameter)
        return parameter

    def get_parameter(self, name):
        """Get a parameter of the current attribute.

        Arguments:
            name (str): The name of the parameter to get.

        Returns:
            Parameter: The parameter if found.
        """
        for param in self.parameters:
            if param.name == name:
                return param


# classic attributes


class BoolAttribute(Attribute):
    """Manage the int attributes."""

    _default = False


class NumericAttribute(Attribute):
    """Manage the abstract numeric attributes common behavior."""

    _attribute_type = None

    def __init__(self, *args, **kwargs):
        """Initialize the attribute."""

        # initialize the attribute
        super(NumericAttribute, self).__init__(*args, **kwargs)

        # add the parameters in memory
        self.add_parameter(
            self._attribute_type, "min", value=kwargs.get("min"), default=None
        )
        self.add_parameter(
            self._attribute_type, "max", value=kwargs.get("max"), default=None
        )
        self.add_parameter(
            self._attribute_type, "step", value=kwargs.get("step"), default=1
        )


class IntAttribute(NumericAttribute):
    """Manage the int attributes."""

    _attribute_type = "int"
    _default = 0


class FloatAttribute(NumericAttribute):
    """Manage the float attributes."""

    _attribute_type = "float"
    _default = 0.0

    def __init__(self, *args, **kwargs):
        """Initialize the attribute."""

        # initialize the attribute
        super(FloatAttribute, self).__init__(*args, **kwargs)

        # add the parameters in memory
        self.add_parameter(
            self._attribute_type, "precision", value=kwargs.get("precision"), default=3
        )


class StrAttribute(Attribute):
    """Manage the string attributes."""

    _default = ""
