"""Manage the parameters."""

from lbx_pipeline.api.abstract import data_objects


class Parameter(data_objects.DataObject):
    """Manage the base class for parameters."""

    # private variables
    _value = None
    _default = None

    def __str__(self):
        """Override the __repr__ method.

        Returns:
            str: The object as a string.
        """
        return "({}){}: {}".format(self.data_type, self.name, self.value)

    def __repr__(self):
        """Override the __repr__ method.

        Returns:
            str: The new representation of the object.
        """
        return self.__str__()

    def __eq__(self, other):
        """Override the __eq__ method.

        Returns:
            bool: True if equal else, False.
        """
        return self.value == other

    def __ne__(self, other):
        """Override the __ne__ method.

        Returns:
            bool: True if different, else False.
        """
        return self.value != other

    def __gt__(self, other):
        """Override the __gt__ method.

        Returns:
            bool: True if greater, else False.
        """
        return self.value < other

    def __lt__(self, other):
        """Override the __lt__ method.

        Returns:
            bool: True if lower, else False.
        """
        return self.value > other

    def __ge__(self, other):
        """Override the __ge__ method.

        Returns:
            bool: True if greater or equal, else False.
        """
        return self.value <= other

    def __le__(self, other):
        """Override the __le__ method.

        Returns:
            bool: True if lower or equal, else False.
        """
        return self.value >= other

    # methods

    def serialize(self):
        """Serialize the parameter.

        Returns:
            dict: The serialized parameter.
        """
        data = super(Parameter, self).serialize()
        for key in ["default", "value", "accept_none"]:
            data[key] = getattr(self, key)
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            data (dict): The data to deserialize with.
        """
        # inheritance
        super(Parameter, self).deserialize(**data)
        self.accept_none = data.get("accept_none", False)
        self.default = data.get("default", data.get("value", self.default))
        self.value = data.get("value", self.default)

    # value methods

    def get_value(self):
        """Get the value of the current parameter.

        Returns:
            -: The parameter's value.
        """
        return self._value

    def set_value(self, value):
        """Set the value of the current parameter.

        Arguments:
            value (-): The value to set to the current parameter.
        """
        self._value = self.validate(value)

    value = property(get_value, set_value)

    def get_default(self):
        """Get the default value of the current parameter.

        Returns:
            -: The parameter's default.
        """
        return self._default

    def set_default(self, value):
        """Set the default of the current parameter.

        Arguments:
            value (-): The default value to set to the current parameter.
        """
        self._default = self.validate(value)

    default = property(get_default, set_default)

    def validate(self, value):
        """Make sure the value is valid.

        Arguments:
            value (-): The value to validate.

        Returns:
            -: The validated value.
        """
        if not self.accept_none and value is None:
            return self.default
        return value

    # manipulation methods

    def reset(self):
        """Reset the parameter."""
        self.value = self.default


# custom paramters


class ClassicParameter(Parameter):
    """Manage the abstract class for common behaviors to classic parameters classes."""

    _parameter_type = None

    def validate(self, value):
        """Make sure the value is valid.

        Arguments:
            value (-): The value to validate.

        Returns:
            -: The validated value.
        """
        # inheritance
        value = super(ClassicParameter, self).validate(value)

        # return the value if it is acceptable
        if self.accept_none and value is None:
            return value

        # try to convert the value if possible
        if not isinstance(value, self._parameter_type):
            try:
                value = self._parameter_type(value)
            except (TypeError, ValueError):
                self.project_logger.error(
                    "Invalid value '{}' for '{}' parameter".format(value, self.name)
                )
                return self.value

        return value


class Bool(ClassicParameter):
    """Manage the bool parameters."""

    _parameter_type = bool
    _default = False


class Int(ClassicParameter):
    """Manage the int parameters."""

    _parameter_type = int
    _default = 0


class Float(ClassicParameter):
    """Manage the float parameters."""

    _parameter_type = float
    _default = 0.0


class Str(ClassicParameter):
    """Manage the str parameters."""

    _parameter_type = str
    _default = ""
