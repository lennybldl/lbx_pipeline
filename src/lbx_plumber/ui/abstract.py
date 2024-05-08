"""Create an abstract class to manage the tools."""

from lbx_python import strings

from lbx_plumber.internal.managers import manager, synchronizer


class AbstractWidget(object):
    """Manage the common behavior for all the widgets."""

    manager = manager.Manager()  # the app manager
    synchronizer = synchronizer.Synchronizer()  # the app synchronizer

    def __init__(self, *args, **kwargs):
        """Initialize the widget."""

        # inheritance
        super(AbstractWidget, self).__init__(*args, **kwargs)

        # initialize the widget
        self.sub_widgets = list()
        self.initialize()

    def initialize(self):
        """Initialize the current widget."""
        self.initialize_preferences()

    # methods

    def sync(self, *args, **kwargs):
        """Synchronize the widget with the rest of the ui."""

    # preferences

    def save_preferences(self, recursive=True):
        """Save the preferences of the widget.

        Keyword Arguments:
            recursive (bool, optional): To recursively save the children preferences.
                Defaults to True.
        """
        # propagate the save preferences to the sub widgets
        if recursive and hasattr(self, "sub_widgets"):
            for widget in self.sub_widgets:
                if hasattr(widget, "save_preferences"):
                    widget.save_preferences(recursive=True)

        # write the preferences
        self.manager.preferences.dump()

    def initialize_preferences(self, recursive=False):
        """Initialize the widget with the saved preferences.

        Keyword Arguments:
            recursive (bool, optional): To recursively initialize the children
                preferences. Defaults to False.
        """
        # propagate the initialize preferences to the sub widgets
        if recursive:
            for widget in self.sub_widgets:
                if hasattr(widget, "initialize_preferences"):
                    widget.initialize_preferences(recursive=True)

    # open/close events

    def interface_closing(self, recursive=True):
        """Override the things to do when the application's ui get's closed.

        Keyword Arguments:
            recursive (bool, optional): To recursively call the close methods on the
                children. Defaults to False.
        """
        # propagate the initialize preferences to the sub widgets
        if recursive:
            for widget in self.sub_widgets:
                if hasattr(widget, "interface_closing"):
                    widget.interface_closing(recursive=True)


class AbstractPanel(AbstractWidget):
    """Manage the common behavior for all the panels."""

    def initialize(self):
        """Initialize the current widget."""
        self.register()
        self.build_ui()
        super(AbstractPanel, self).initialize()

    def register(self):
        """Register the current widget to the synchronizer."""
        setattr(self.synchronizer, strings.snake_case(self.__class__.__name__), self)

    def build_ui(self, *args, **kwargs):
        """Build the widget's ui."""

    # open/close events

    def closeEvent(self, event):  # noqa N802 - Pyside2 method
        """Override the things to do when the application's ui get's closed."""
        self.save_preferences()
        self.interface_closing()
        event.accept()
