"""Create a custom node."""

from lbx_plumber import open_api


class Null(open_api.BaseNode):
    """Manage the null node that does nothing on its own."""
