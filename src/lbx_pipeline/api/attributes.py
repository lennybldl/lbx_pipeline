"""Manage the attributes."""

from lbx_python_core import strings

from lbx_pipeline.api.abstract import data_structures


class Attribute(data_structures.DataStructure):
    """Manage the base class for the attribute."""

    default_storage_variable = "attributes"

    # private variables
    _parameters = None

    def __str__(self):
        """Override the __repr__ method.

        Returns:
            str: The object as a string.
        """
        return self.data_path

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
        return self.get_parameter("value") == other

    def __ne__(self, other):
        """Override the __ne__ method.

        Returns:
            bool: True if different else False.
        """
        return self.get_parameter("value") != other

    def __gt__(self, other):
        """Override the __gt__ method.

        Returns:
            bool: True if greater, else False.
        """
        return self.get_parameter("value") < other

    def __lt__(self, other):
        """Override the __lt__ method.

        Returns:
            bool: True if lower, else False.
        """
        return self.get_parameter("value") > other

    def __ge__(self, other):
        """Override the __ge__ method.

        Returns:
            bool: True if greater or equal, else False.
        """
        return self.get_parameter("value") <= other

    def __le__(self, other):
        """Override the __le__ method.

        Returns:
            bool: True if lower or equal, else False.
        """
        return self.get_parameter("value") >= other

    # methods

    def initialize(self, **data):
        """Initialize the object before deserializing it."""
        # inheritance
        super(Attribute, self).initialize(**data)

        # add the parameters in memory
        self.add_parameter(
            self.data_type,
            name="value",
            value=data.get("value"),
            default=data.get("default"),
        )

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = super(Attribute, self).serialize()
        data["nice_name"] = self.nice_name
        data["parameters"] = [o.serialize() for o in self.parameters.values()]
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            data (dict): The data to deserialize with.
        """
        # inheritance
        super(Attribute, self).deserialize(**data)

        # initialize the variables
        self.nice_name = data.get("nice_name", strings.title_case(self.name))

        # initialize the parameters
        for param_data in data.get("parameters", list()):
            param = self.parameters.get(param_data["name"])
            if param:
                param.deserialize(parent=self, **param_data)
            else:
                self.add_parameter(**param_data)

    # data objects methods

    def add_parameter(self, data_type, **data):
        """Add a parameter to the current object.

        Arguments:
            data_type (str): The type of parameter to create.
            data (dict): The data to deserialize with.

        Returns:
            Parameter: The created parameter.
        """
        # create the parameter
        parameter_class = self.data_manager.parameters.get(data_type)
        if not parameter_class:
            raise TypeError("No valid data_type given : {}".format(data_type))

        # create the parameter
        data["parent"] = self
        data["storage_variable"] = "parameters"
        parameter = parameter_class(**data)
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
        param = self.parameters.get(name)
        if param:
            return param
        raise KeyError("Tried to access non-existing parameter '{}'".format(name))

    def get_parameters(self):
        """Get the list of parameters on the current object.

        Returns:
            dict: The current parameters.
        """
        if self._parameters is None:
            self._parameters = dict()
        return self._parameters

    parameters = property(get_parameters)

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
        param = self.get_parameter(name)
        if default:
            return param.default
        return param.value

    def edit(self, name, value, default=False):
        """Edit a parameter value.

        Arguments:
            name (str): The name of the parameter to edit.
            value (any): The value to set for the parameter.

        Keyword Arguments:
            default (bool, optional): True to edit the default value, else False.
                Default to False.
        """
        param = self.get_parameter(name)
        if default:
            param.default = value
        else:
            param.value = value

    # maniplation methods

    def reset(self):
        """Reset the attribute's value to its default."""
        parameter = self.get_parameter("value")
        parameter.reset()

    def reset_to_factory(self):
        """Reset all the parameters of the attribute."""
        for parameter in self.parameters:
            parameter.reset()


# custom attributes


class ClassicAttribute(Attribute):
    """Manage the abstract numeric attributes common behavior."""


class Bool(Attribute):
    """Manage the int attributes."""


class NumericAttribute(Attribute):
    """Manage the abstract numeric attributes common behavior."""

    _attribute_type = None

    def initialize(self, **data):
        """Initialize the object before deserializing it."""

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


class Int(NumericAttribute):
    """Manage the int attributes."""

    _attribute_type = "Int"


class Float(NumericAttribute):
    """Manage the float attributes."""

    _attribute_type = "Float"

    def initialize(self, **data):
        """Initialize the attribute."""

        # initialize the attribute
        super(Float, self).initialize(**data)

        # add the parameters in memory
        self.add_parameter(
            "Int",
            name="precision",
            value=data.get("precision"),
            default=3,
        )


class Str(Attribute):
    """Manage the string attributes."""
