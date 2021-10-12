"""Create the ui to define the workspace body."""

from python_core.pyside2 import base_ui
from python_core.pyside2.widgets import layout


class WorkspacePath(layout.HBoxLayout):
    """Create a layout to manage the workspace path."""

    def __init__(self, *args, **kwargs):
        """Initialize the layout."""

        super(WorkspacePath, self).__init__(*args, **kwargs)

    def populate(self):
        """Populate the workspace path with buttons to interact."""

        self.add_label("Workspace Path : ")

        self.path = self.add_line_edit("", placeholder=r"C:\path\to\maya\project\...")

        self.add_button("Browse...", clicked=self.browse)

    def browse(self):
        """Browse to the workspace path."""

        dialog = base_ui.BrowseDialog()
        dialog.title = "Browse to workspace"

        result = dialog.browse(file=False)

        # get the corresponding line edit
        if result is not None:
            self.path.set_text(result[0])
        else:
            self.path.set_text(reset=True)
