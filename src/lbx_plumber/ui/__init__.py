"""Manage the ui of the application."""

from lbx_plumber import open_api
from lbx_plumber.ui import main_window
from PySide2.QtWidgets import QApplication


def run():
    """Launch the UI.

    Returns:
        MainWindow: The created main window.
    """
    open_api.run()

    app = QApplication()
    window = main_window.MainWindow()
    window.show()
    app.exec_()

    return window
