"""Manage the application's logs."""

from lbx_python import logging

import lbx_pipeline


class Logger(logging.Logger):
    """Manage the application logs."""

    # levels
    _stream_level = "INFO"
    _file_level = "DEBUG"


class SessionLogger(Logger):
    """Manage the current session pipeline logs."""

    def __init__(self, *args, **kwargs):
        """Initialize the logger."""

        super(SessionLogger, self).__init__(
            "({}) SESSION".format(lbx_pipeline.NAME), *args, **kwargs
        )


class ProjectLogger(Logger):
    """Manage the current project's logs."""

    def __init__(self, *args, **kwargs):
        """Initialize the logger."""

        super(ProjectLogger, self).__init__(
            "({}) WORKSPACE".format(lbx_pipeline.NAME), *args, **kwargs
        )

    # methods

    def set_name(self, name):
        """Set the name of the current logger.

        Arguments:
            name (str): The name of the logger.
        """
        self.name = "({}) {}".format(lbx_pipeline.NAME, name)
