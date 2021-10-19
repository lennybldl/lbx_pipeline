"""Create the ui to define the workspace body."""

from python_core.pyside2 import base_ui
from python_core.pyside2.widgets import layout

from pipeline.utils import database


class WorkspacePath(layout.VBoxLayout):
    """Create a layout to manage the workspace path."""

    def __init__(self, *args, **kwargs):
        """Initialize the layout."""

        super(WorkspacePath, self).__init__(*args, **kwargs)

        self.db = database.Database()

    def populate(self):
        """Populate the workspace path with buttons to interact."""

        self.add_label("Workspace Path : ")

        layout = self.add_layout("horizontal")
        self.path = layout.add_line_edit(
            "",
            placeholder=r"C:\path\to\maya\project\...",
            tooltip="The maya project path.",
        )
        self.path.editingFinished.connect(self.save_prefs)

        layout.add_button("Browse...", clicked=self.browse)

        self.set_prefs()

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

        self.save_prefs()

    def save_prefs(self):
        """Save current ui prefs."""

        prefs = self.db.prefs

        prefs.update(
            {
                "workspace": self.path.text(),
            }
        )

        self.db.prefs = prefs

    def set_prefs(self):
        """Edit the ui with the saved prefs."""

        prefs = self.db.prefs

        if prefs.get("workspace", False):
            self.path.setText(prefs["workspace"])
