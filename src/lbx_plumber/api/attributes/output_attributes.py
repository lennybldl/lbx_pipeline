"""Manage the output attributes."""

from lbx_plumber.api import attributes


class OutputAttribute(attributes.Attribute):
    """Manage the output attributes."""

    def __init__(self, *args, **kwargs):
        """Initialize the object."""

        # inheritance
        super(OutputAttribute, self).__init__(*args, **kwargs)

        # create the value parameter
        parameter_class = self.data_manager.parameters.get(self.data_type)
        self.parameter = parameter_class(parent=self)

    # methods

    @property
    def is_input(self):
        """Get if the attribute is an input attribute.

        Returns:
            bool: True if it is else False.
        """
        return False

    def get(self):
        """Get the value of the current attribute.

        Returns:
            -: The value of the current attribute.
        """
        return self.parameter.value

    def set(self, value):
        """Set the value of the current attribute.

        Arguments:
            value (-): The value of the current attribute.
        """
        # set the value if the value changed
        if value != self.get():
            self.parameter.value = value
            # propagate the value change
            for attribute in self.out_attributes:
                attribute.set(value)


# custom attributes


class Bool(OutputAttribute):
    """Manage the boolean attributes."""


class Int(OutputAttribute):
    """Manage the int attributes."""


class Float(OutputAttribute):
    """Manage the float attributes."""


class Str(OutputAttribute):
    """Manage the string attributes."""
