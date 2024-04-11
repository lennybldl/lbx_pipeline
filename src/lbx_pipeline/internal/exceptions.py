"""Manage the exeptions of the package."""


class ConfictingProjectPathError(Exception):
    """Manage the error when a project conflicts with another."""

    def __init__(self, path):
        """Initialize the error.

        Arguments:
            path (str): The project's path.
        """
        super(ConfictingProjectPathError, self).__init__(
            "The given project path conflicts with another : '{}'".format(path)
        )


class InvalidProjectPathError(Exception):
    """Manage the error when a project is invalid."""

    def __init__(self, path):
        """Initialize the error.

        Arguments:
            path (str): The project's path.
        """
        super(InvalidProjectPathError, self).__init__(
            "The given project path isn't valid : '{}'".format(path)
        )
