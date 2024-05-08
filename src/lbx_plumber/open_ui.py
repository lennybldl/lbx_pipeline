"""Manage the package's api commands the users have access to."""

from lbx_plumber import ui
from lbx_plumber.internal import proxies

# management


def run():
    """Run the application's ui.

    Returns:
        MainWindow: The created main window.
    """
    return MainWindow(ui.run())


# classes access


class MainWindow(proxies.Proxy):
    """Manage the proxy nodes."""
