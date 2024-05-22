"""Manage the main windows of the application."""

from lbx_qt.widgets import FramelessMainWindow
from lbx_resources import resources
from PySide2.QtGui import QFontDatabase

import lbx_plumber
from lbx_plumber.internal import common
from lbx_plumber.ui import abstract, editors

TITLE = "Plumber - {}".format(lbx_plumber.VERSION)
ICON = common.get_image("pipe.png")
MINIMIZE_ICON = resources.get_icon("ui/minus.svg")
NORMAL_ICON = resources.get_icon("ui/minimize_2.svg")
MAXIMIZE_ICON = resources.get_icon("ui/square.svg")
CLOSE_ICON = resources.get_icon("ui/x.svg")


class MainWindow(abstract.AbstractPanel, FramelessMainWindow):
    """Manage the application's main widnow."""

    def __init__(self, *args, **kwargs):
        """Initialize the window."""

        # inheritance
        super(MainWindow, self).__init__(
            title=TITLE,
            icon=ICON,
            minimize_icon=MINIMIZE_ICON,
            normal_icon=NORMAL_ICON,
            maximize_icon=MAXIMIZE_ICON,
            close_icon=CLOSE_ICON,
            *args,
            **kwargs
        )

        # load the fonts from the resources
        for font in resources.get_fonts().values():
            QFontDatabase.addApplicationFont(font)

    def build_ui(self):
        """Build the ui of the widget."""

        # setup the menu bar
        menu_bar = self.title_bar.menu_bar

        # create the edit menu
        edit_menu = menu_bar.add_menu("Edit")
        # add the themes to the menu bar
        edit_menu.add_separator()
        themes_menu = edit_menu.add_menu("Themes")
        for theme, path in sorted(
            resources.get_qt_themes().items(), key=lambda x: x[0].lower()
        ):
            themes_menu.add_action(
                theme,
                triggered=lambda x=None, path=path: self.set_theme(path),
            )

        # add a layout to host the main editors
        splitter = self.layout.add("Splitter")

        # add the outliner
        outliner_editor = editors.OutlinerEditor(self)
        splitter.add(outliner_editor)
        # add the network editor
        network_editor = editors.NetworkEditor(self)
        splitter.add(network_editor)
        # add the attribute editor
        attribute_editor = editors.AttributeEditor(self)
        splitter.add(attribute_editor)

        self.sub_widgets.extend([outliner_editor, network_editor, attribute_editor])

    # preferences

    def save_preferences(self, recursive=True):
        """Save the preferences of the widget.

        Keyword Arguments:
            recursive (bool, optional): To recursively save the children preferences.
                Defaults to True.
        """
        prefs = self.manager.preferences

        # save the window preferences
        prefs.set("ui.maximized", self.title_bar.maximize_button.isChecked())
        prefs.set("ui.theme", self.theme.name)

        # inheritance
        super(MainWindow, self).save_preferences(recursive)

    def initialize_preferences(self, recursive=False):
        """Initialize the widget with the saved preferences.

        Keyword Arguments:
            recursive (bool, optional): To recursively initialize the children
                preferences. Defaults to False.
        """
        prefs = self.manager.preferences

        # set the window preferences
        self.set_theme(resources.get_qt_theme(prefs.get("ui.theme", "default")))
        self.title_bar.maximize_button.setChecked(prefs.get("ui.maximized", True))

        # inheritance
        super(MainWindow, self).initialize_preferences(recursive)
