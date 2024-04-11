"""Manage the common behavior of all the serializable objects."""

from lbx_pipeline.api.abstract import objects


class SerializableObject(objects.Object):
    """Manage the common behavior of all the serializable objects."""

    def serialize(self):
        """Serialize the object.

        Returns:
            dict: The object's serialization.
        """
        data = dict()
        return data

    def deserialize(self, **data):
        """Deserialize the object.

        Arguments:
            data (dict): The data to deserialize with.
        """
