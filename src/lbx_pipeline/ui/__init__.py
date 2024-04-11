"""Manage the ui of the pipeline."""

from lbx_pipeline import open_api
from lbx_pipeline.ui import main_window
from PySide2.QtWidgets import QApplication


def launch_windows_ui():
    """Launch the UI on a windows device.

    Returns:
        MainWindow: The created main window.
    """
    open_api.run()

    app = QApplication()
    window = main_window.MainWindow()
    window.show()
    app.exec_()

    return window
