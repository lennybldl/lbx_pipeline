"""Manage the common behavior of all the data structures."""

import uuid

from lbx_python import strings

from lbx_pipeline.api.abstract import data_objects


class DataStructure(data_objects.DataObject):
    """Manage the common behavior of all the data structures."""

    storage_variable = None

    # private variables
    _name = None

    # methods

    def __init__(self, *args, **data):
        """Initialize the object."""
        # create a unique identifier for the data structure to keep track of the object
        self.uuid = uuid.uuid4()
        # inheritance
        super(DataStructure, self).__init__(*args, **data)

    def get_name(self):
        """Get the name of the current data structure.

        Returns:
            str: The current data structure's name.
        """
        return self._name

    def set_name(self, name=None):
        """Set the name of the current data structure.

        Keyword Arguments:
            name (str, optional): The name we want to set for the current
                data strucuture. If None, generate a new one. Default to None.
        """
        # make sure the name is in snake case
        if name:
            name = strings.replace_specials(name, "_")

        # do not go further if no parent
        if not self.parent:
            self._name = name or (self.data_type + "1")
            return

        # list the existing content
        assigned_names = getattr(self.parent, self.storage_variable + "_by_name")
        # remove the current name from the assigned names
        assigned_names.pop(self._name, None)

        # use a unique name if None given
        if not name or name in assigned_names:
            base_name = name or self.data_type
            if assigned_names:
                for index in map(str, range(1, len(assigned_names) + 2)):
                    name = base_name + index
                    if name not in assigned_names:
                        break
            else:
                name = base_name + "1"

        # set the name of the data structure
        self._name = name
        # register the object under its new name to the project and holder
        assigned_names[name] = self

    name = property(get_name, set_name)

    def delete(self):
        """Delete the current data structure."""
        # remove the data structure from the variables it is stored in
        if self.parent:
            getattr(self.parent, self.storage_variable + "_by_name").pop(self.name)

        del self
