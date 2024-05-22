"""Manage the outliner."""

from lbx_qt.widgets import Widget

from lbx_plumber.ui import abstract
from lbx_plumber.ui.widgets import tree_views


class OutlinerEditor(abstract.AbstractPanel, Widget):
    """Manage the network edior."""

    def __init__(self, *args, **kwargs):
        """Initialize the outliner."""

        # inheritance
        super(OutlinerEditor, self).__init__(layout="vertical", *args, **kwargs)

    def build_ui(self, *args, **kwargs):
        """Build the panel's ui."""

        # inheritance
        super(OutlinerEditor, self).build_ui(*args, **kwargs)

        # add the network outliner
        self.network_outliner = tree_views.NetworkOutliner(self)
        self.layout.add(self.network_outliner)

        self.network_outliner.add_column(count=4)
        item = self.network_outliner.add_item(
            content=["titi", "tutu", "toto"],
            text_alignments={i: "Center" for i in range(5)},
        )
        widget = item.set_widget(column=3, layout="horizontal")
        widget.layout.add("PushButton")
        widget.layout.add("PushButton")
