"""Manage the parameters."""

from lbx_python_core import strings

from lbx_pipeline.internal import logging

logger = logging.SessionLogger()


class Parameter(object):
    """Manage the base class for the parameter."""

    # private variables
    _value = None
    _default = None

    def __init__(self, attribute, name, value, lock=False, visible=True, **kwargs):
        """Initialize the parameter.

        Arguments:
            attribute (Attribute): The attribute the parameter is linked to.
            name (str): The name of the parameter.
            value (-, optional): The value of the parameter.

        Keyword Arguments:
            lock (bool, optional): True to lock the parameter, else False.
                Default to False.
            visible (bool, optional): True to set the parameter visible, else False.
                Default to True.
            default (-, optional): The default value of the parameter. Default to value.
        """
        # initialize the attribute
        super(Parameter, self).__init__()

        # initialize the variables
        self.type = strings.snake_case(self.__class__.__name__.split("Parameter")[0])

        # initialize the parameters properties
        self.attribute = attribute
        self.name = name
        self.default = kwargs.get("default", value)
        self.value = value
        self.lock = lock
        self.visible = visible

    def __str__(self):
        """Override the __repr__ method.

        Returns:
            str: The object as a string.
        """
        return str(self.value)

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
        return self.value == other

    def __ne__(self, other):
        """Override the __ne__ method.

        Returns:
            bool: True if different else False.
        """
        return self.value != other

    def __get__(self, *args, **kwargs):
        """Get the value of the current parameter.

        Returns:
            -: The parameters value.
        """
        return self.get_value()

    def __set__(self, *args, **kwargs):
        """Set the parameter's value."""
        self.set_value(args[1])

    # methods

    def get_path(self):
        """Get the path of the current parameter.

        Returns:
            str: The dot separated path of the current parameter.
        """
        return ".".join([self.attribute.node.name, self.attribute.long_name, self.name])

    path = property(get_path)

    def get_value(self):
        """Get the value of the current attribute.

        Returns:
            -: The attribute's value.
        """
        return self._value

    def set_value(self, value):
        """Set the value of the current attribute.

        Arguments:
            value (-): The value to set to the current attribute.
        """
        self._value = self.validate_value(value)

    value = property(get_value, set_value)

    def get_default(self):
        """Get the default value of the current attribute.

        Returns:
            -: The attribute's default.
        """
        return self._default

    def set_default(self, value):
        """Set the default of the current attribute.

        Arguments:
            value (-): The default value to set to the current attribute.
        """
        self._default = self.validate_value(value)

    default = property(get_default, set_default)

    def validate_value(self, value, none_as_default=True):
        """Make sure the value is valid.

        Arguments:
            value (-): The value to validate.

        Keyword Arguments:
            none_as_default (bool, optional): To set the value to default if the given
                value is None. Default to True.

        Returns:
            -: The validated value.
        """
        if none_as_default and value is None:
            return self.default
        return value

    def reset(self):
        """Reset the parameter."""
        self.value = self.default

    def serialize(self):
        """Serialize the parameter.

        Returns:
            dict: The serialized parameter.
        """
        data = dict()
        data["type"] = self.type
        for key in ["default", "value", "lock", "visible"]:
            data[key] = getattr(self, key)
        return data


# classic parameters


class ClassicParameters(Parameter):
    """Manage the abstract class for common behaviors to classic parameters classes."""

    _parameter_type = None

    def validate_value(self, value, none_as_default=True):
        """Make sure the value is valid.

        Arguments:
            value (-): The value to validate.

        Keyword Arguments:
            none_as_default (bool, optional): To set the value to default if the given
                value is None. Default to True.

        Returns:
            -: The validated value.
        """
        # inheritance
        value = super(ClassicParameters, self).validate_value(value, none_as_default)

        # try to convert the value if possible
        if not isinstance(value, self._parameter_type):
            try:
                value = self._parameter_type(value)
            except (TypeError, ValueError):
                logger.error(
                    "Invalid value '{}' for '{}' parameter".format(value, self.path)
                )
                return self.value

        return value


class BoolParameter(ClassicParameters):
    """Manage the bool parameters."""

    _parameter_type = bool
    _default = False


class IntParameter(ClassicParameters):
    """Manage the int parameters."""

    _parameter_type = int
    _default = 0


class FloatParameter(ClassicParameters):
    """Manage the float parameters."""

    _parameter_type = float
    _default = 0.0


class StrParameter(ClassicParameters):
    """Manage the str parameters."""

    _parameter_type = str
    _default = ""
