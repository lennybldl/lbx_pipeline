"""Manage a menu bar to add menus to the app."""

from python_core.pyside2.widgets import menu_bar


class AppMenuBar(menu_bar.MenuBar):

    _name = "AppMenuBar"

    def __init__(self, *args, **kwargs):
        """Initialize the app menu bar."""

        super(AppMenuBar, self).__init__(*args, **kwargs)

    def populate(self):
        """Poulate the app menu bar with menus."""

        # add file management menus
        recent_menu = self.add_menu("Recent")

        # TODO
        for i in range(10):
            recent_menu.add_action("test" + str(i))
