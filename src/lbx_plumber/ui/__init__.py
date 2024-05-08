"""Manage the ui of the application."""

from lbx_plumber.ui import main_windows


def run():
    """Launch the UI.

    Returns:
        MainWindow: The created main window.
    """
    window = main_windows.MainWindow()
    window.show()
    return window
