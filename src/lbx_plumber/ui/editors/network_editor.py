"""Manage the network editor."""

from lbx_qt.widgets import Widget

from lbx_plumber.ui import abstract
from lbx_plumber.ui.widgets import graphics_views


class NetworkEditor(abstract.AbstractPanel, Widget):
    """Manage the network edior."""

    def __init__(self, *args, **kwargs):
        """Initialize the object."""

        # inheritance
        super(NetworkEditor, self).__init__(layout="vertical", *args, **kwargs)

    def build_ui(self, *args, **kwargs):
        """Build the panel's ui."""

        # inheritance
        super(NetworkEditor, self).build_ui(*args, **kwargs)

        # add the network view
        self.network_view = graphics_views.NetworkView(self)
        self.layout.add(self.network_view)
        self.sub_widgets.append(self.network_view)
