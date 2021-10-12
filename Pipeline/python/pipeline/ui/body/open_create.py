"""Add a layout that to open an create assets tasks."""

from python_core.pyside2.widgets import layout

from pipeline.utils import conformity, database
from pipeline.ui.widgets import assets_list_widget


class OpenCreate(layout.VBoxLayout):
    """Manage files to open or create."""

    def __init__(self, *args, **kwargs):
        """Initialize the layout."""

        super(OpenCreate, self).__init__(*args, **kwargs)

        self.db = database.Database()

    def populate(self):
        """Populate the ui with buttons to interact."""

        # get the app data
        data = self.db.app_data

        # build tasks
        lay = self.add_layout("horizontal")
        self.asset_type = lay.add_combo_box(data["assets"].keys())
        self.task_type = lay.add_combo_box(data["tasks"])

        # build the create
        lay = self.add_layout("horizontal")
        self.asset_name = lay.add_line_edit("", placeholder="pre_assetName")
        self.asset_name.editingFinished.connect(self.conform_name)
        self.create_button = lay.add_button("Create", clicked=self.create_task)
        self.create_button.setEnabled(False)

        # build the tasks representation
        self.filter_bar = self.add_line_edit()
        self.list_widget = assets_list_widget.AssetsListWidget()
        self.list_widget.populate()
        self.addWidget(self.list_widget)

        # build the open
        lay = self.add_layout("horizontal")
        lay.add_button("Open latest")
        lay.add_button("Open specific")

        self.set_prefs()

        # save the current ui prefs every time something changes
        self.asset_type.currentTextChanged.connect(self.save_prefs)
        self.task_type.currentTextChanged.connect(self.save_prefs)

    def create_task(self):
        """Create a task to work on an asset."""

    def conform_name(self):
        """Conform the asset name set in the line edit."""

        self.asset_name.blockSignals(True)

        # conform the asset name
        name = self.asset_name.text()
        if name:
            self.asset_name.setText(conformity.conform_asset_name(name))
            self.create_button.setEnabled(True)
        else:
            self.create_button.setEnabled(False)

        self.asset_name.blockSignals(False)

    def save_prefs(self):
        """Save current ui prefs."""

        prefs = self.db.prefs

        prefs.update(
            {
                "current_assets": self.asset_type.currentText(),
                "current_tasks": self.task_type.currentText(),
            }
        )

        self.db.prefs = prefs

    def set_prefs(self):
        """Edit the ui with the saved prefs."""

        prefs = self.db.prefs

        if prefs.get("current_assets", False):
            self.asset_type.setCurrentText(prefs["current_assets"])

        if prefs.get("current_tasks", False):
            self.task_type.setCurrentText(prefs["current_tasks"])
