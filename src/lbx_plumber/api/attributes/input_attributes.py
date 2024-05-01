"""Manage the input attributes."""

from lbx_python import strings

from lbx_plumber.api import attributes


class InputAttribute(attributes.Attribute):
    """Manage the input attributes."""

    # private variables
    _parameters = None
    _in_attribute = None

    # methods

    def initialize(self, **data):
        """Initialize the object before deserializing it.

        Arguments:
            data (dict): The data to deserialize with.
        """
        # inheritance
        super(InputAttribute, self).initialize(**data)

        # add the parameters in memory
        self.add_parameter(self.data_type, name="value", value=data.get("value"))

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        # inheritance
        data = super(InputAttribute, self).serialize()
        if self.is_builtin:
            return data

        # customize the serialization
        data["nice_name"] = self.nice_name
        data["parameters"] = [o.serialize() for o in self.parameters.values()]
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            data (dict): The data to deserialize with.
        """
        # inheritance
        super(InputAttribute, self).deserialize(**data)

        # initialize the variables
        self.nice_name = data.get("nice_name", strings.title_case(self.name))

        # initialize the parameters
        for param_data in data.get("parameters", list()):
            parameter = self.get_parameter(param_data["name"])
            parameter.deserialize(parent=self, **param_data)

    @property
    def is_input(self):
        """Get if the attribute is an input attribute.

        Returns:
            bool: True if it is else False.
        """
        return True

    def get_in_attribute(self):
        """Get the in attribute of the current attribute.

        Returns:
            Attribute: The input attribute.
        """
        return self._in_attribute

    def set_in_attribute(self, attribute):
        """Set the in attribute of the current attribute.

        Arguments:
            attribute (Attribute): The attribute to set as input.
        """
        self._in_attribute = attribute
        if attribute:
            self.set(attribute.get())

    in_attribute = property(get_in_attribute, set_in_attribute)

    # parameters methods

    def add_parameter(self, data_type, name, **data):
        """Add a parameter to the current object.

        Arguments:
            name (str): The name to give to the parameter.
            data_type (str): The type of parameter to create.
            data (dict): The data to deserialize with.

        Returns:
            Parameter: The created parameter.
        """
        # create the parameter
        parameter_class = self.data_manager.parameters.get(data_type)
        if not parameter_class:
            raise TypeError("No valid data_type given : {}".format(data_type))

        # create the parameter and add it to the attribute
        data["parent"] = self
        parameter = parameter_class(name=name, **data)
        self.parameters[name] = parameter
        return parameter

    def get_parameter(self, name):
        """Get a parameter using its name.

        Arguments:
            name (str): The name of the parameter.

        Raises:
            KeyError: Tried to access non-existing parameter.

        Returns:
            Parameter: The parameter we asked for.
        """
        parameter = self.parameters.get(name)
        if parameter:
            return parameter
        raise KeyError(
            "Tried to access non-existing parameter '{}' on '{}'".format(name, self)
        )

    def get_parameters(self):
        """Get the list of parameters on the current object.

        Returns:
            dict: The current parameters.
        """
        if self._parameters is None:
            self._parameters = dict()
        return self._parameters

    parameters = property(get_parameters)

    # data management

    def get(self):
        """Get the value of the current attribute.

        Returns:
            -: The value of the current attribute.
        """
        return self.query("value")

    def set(self, value):
        """Set the value of the current attribute.

        Arguments:
            value (-): The value of the current attribute.
        """
        self.edit("value", value)

    def query(self, name, default=False):
        """Query a parameter value.

        Arguments:
            name (str): The name of the parameter to query.

        Keyword Arguments:
            default (bool, optional): True to query the default value, else False.
                Default to False.

        Returns:
            any: The value to the parameter.
        """
        parameter = self.get_parameter(name)
        return parameter.default if default else parameter.value

    def edit(self, name, value, default=False):
        """Edit a parameter value.

        Arguments:
            name (str): The name of the parameter to edit.
            value (any): The value to set for the parameter.

        Keyword Arguments:
            default (bool, optional): True to edit the default value, else False.
                Default to False.
        """
        # skip if the attribute is a builtin attribute
        if self.is_builtin and (name != "value" or default):
            return

        # get the desired parameter
        parameter = self.get_parameter(name)
        if default:
            parameter.default = value
            return

        # skip if the value didn't change
        if value == parameter.value:
            return

        parameter.value = value
        if name == "value":
            # validate the attribute value
            if not self.in_attribute:
                parameter.value = self.validate(parameter.value)
                value = parameter.value

            # set the host to be dirty if the input attribute changed
            if self.is_builtin:
                self.parent.is_dirty = True

            # propagate the value change
            for attribute in self.out_attributes:
                attribute.set(value)

    def validate(self, value):
        """Make sure the given value meets the attribute requirements.

        Arguments:
            value (-): The value to validate.

        Returns:
            -: The validated value.
        """
        return value

    def reset(self):
        """Reset the attribute's value to its default."""
        parameter = self.get_parameter("value")
        parameter.reset()

    def reset_to_factory(self):
        """Reset all the parameters of the attribute."""
        for parameter in self.parameters:
            parameter.reset()

    def disconnect_input(self):
        """Disconnect the attribute's input."""
        self.parent.parent.disconnect_input(self)


# abstract attributes


class NumericAttribute(InputAttribute):
    """Manage the abstract numeric attributes common behavior."""

    _attribute_type = None

    def initialize(self, **data):
        """Initialize the object before deserializing it.

        Arguments:
            data (dict): The data to deserialize with.
        """

        # inheritance
        super(NumericAttribute, self).initialize(**data)

        # add the parameters in memory
        self.add_parameter(
            self._attribute_type,
            name="min",
            value=data.get("min"),
            default=None,
            accept_none=True,
        )
        self.add_parameter(
            self._attribute_type,
            name="max",
            value=data.get("max"),
            default=None,
            accept_none=True,
        )
        self.add_parameter(
            self._attribute_type,
            name="step",
            value=data.get("step"),
            default=1,
        )

    def validate(self, value):
        """Make sure the given value meets the attribute requirements.

        Arguments:
            value (-): The value to validate.

        Returns:
            -: The validated value.
        """
        value = super(NumericAttribute, self).validate(value)

        # make sure the value stands withing the range
        _min, _max = self.query("min"), self.query("max")
        if _min is None and _max is None:
            return value
        if _min is not None and _max is not None:
            return max(_min, min(value, _max))
        if _min is None:
            return min(value, _max)
        return max(_min, value)


# custom attributes


class Bool(InputAttribute):
    """Manage the boolean attributes."""


class Int(NumericAttribute):
    """Manage the int attributes."""

    _attribute_type = "Int"


class Float(NumericAttribute):
    """Manage the float attributes."""

    _attribute_type = "Float"

    def initialize(self, **data):
        """Initialize the attribute.

        Arguments:
            data (dict): The data to deserialize with.
        """
        # initialize the attribute
        super(Float, self).initialize(**data)

        # add the parameters in memory
        self.add_parameter(
            "Int",
            name="precision",
            value=data.get("precision"),
            default=3,
        )

    def validate(self, value):
        """Make sure the given value meets the attribute requirements.

        Arguments:
            value (-): The value to validate.

        Returns:
            -: The validated value.
        """
        value = super(Float, self).validate(value)
        return round(value, self.query("precision"))


class Str(InputAttribute):
    """Manage the string attributes."""
