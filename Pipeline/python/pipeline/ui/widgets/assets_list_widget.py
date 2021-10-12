"""Manage the created assets widgets."""

from python_core.pyside2.widgets import list_widget


class AssetsListWidget(list_widget.ListWidget):
    """Manage every project tasks."""

    def __init__(self, *args, **kwargs):
        """Initialize the line edit."""

        super(AssetsListWidget, self).__init__(*args, **kwargs)

    def populate(self):
        """Populate the list widget with tasks to do."""

        # TODO
        print("populate")
