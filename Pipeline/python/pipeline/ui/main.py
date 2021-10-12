"""Manage the pipeline main window."""

from python_core.pyside2 import base_ui

from pipeline.ui.body import app_menu_bar, open_create, workspace_path
from pipeline.utils import database


class Main(base_ui.MainWindow):
    """Manage the main window."""

    _title = "Pipeline 0.1.0"
    _name = "MainWindow"

    def __init__(self, *args, **kwargs):
        """initialise the main window."""

        super(Main, self).__init__(*args, **kwargs)

        # make sure the app runs on safe basis
        db = database.Database()
        db.start_checks()

    def populate(self):
        """Populate themain window UI."""

        main_layout = self.main_widget.layout
        main_layout.set_alignment("top")

        # create a menu bar
        menu = app_menu_bar.AppMenuBar()
        menu.populate()
        main_layout.addWidget(menu)

        # populate the app ui in an other layout that has padding
        layout = main_layout.add_layout("vertical")

        # add the workspace path
        lay = workspace_path.WorkspacePath()
        lay.populate()
        layout.addLayout(lay)

        # add the open create
        lay = open_create.OpenCreate()
        lay.populate()
        layout.addLayout(lay)
