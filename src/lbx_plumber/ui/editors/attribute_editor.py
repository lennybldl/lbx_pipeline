"""Manage the attribute editor."""

from lbx_qt.widgets import Widget

from lbx_plumber.ui import abstract


class AttributeEditor(abstract.AbstractPanel, Widget):
    """Manage the attribute edior."""

    def __init__(self, *args, **kwargs):
        """Initialize the object."""

        # inheritance
        super(AttributeEditor, self).__init__(layout="vertical", *args, **kwargs)

    def build_ui(self, *args, **kwargs):
        """Build the panel's ui."""

        # inheritance
        super(AttributeEditor, self).build_ui(*args, **kwargs)

        for _ in range(4):
            self.layout.add("PushButton")
