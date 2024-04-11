"""Manage the params."""

from lbx_pipeline.api.abstract import objects


class Param(objects.Object):
    """Manage a descriptor that gives access to bound data units."""

    def __init__(self, data_type, **data):
        """Initialize the param."""
        # keep the data in memory to create a data unt
        self.data_type = data_type
        self.data = data
        # a dictionary that keeps in memory the instances that hold the param
        self.instances = dict()

    def __get__(self, instance, owner):
        """Override the __get__method to redirect to a data unit.

        Returns:
            DataUnit: The bound data unit.
        """
        if instance is None:
            return self

        # return the existing data unit if it already exists
        if instance in self.instances:
            return self.instances[instance]

        # create a data unit
        # get the data unit class
        data_unit_class = self.data_manager.data_units.get(self.data_type)
        if not data_unit_class:
            raise TypeError("No valid data unt type given : {}".format(self.data_type))

        # create the param
        self.data["parent"] = instance
        self.data["storage_variable"] = "params"
        data_unit = data_unit_class(**self.data)
        # keep the instance in memory
        self.instances[instance] = data_unit
        return data_unit
