"""Test the package to see if it still works correctly."""

# setup the test environment
import sys

from lbx_python import context, logging, system
from PySide2.QtWidgets import QApplication

sys.path.insert(0, system.File(__file__).get_upstream(2) + "/src")

from lbx_plumber import open_api, open_ui  # noqa E402

logger = logging.Logger("Test")
logger.stream_level = "info"


def log(func):
    """Check if the test worked.

    This method is meant to be used as a decorator.

    Arguments:
        func (callable): The function to call.
    """

    def wrapper(*args, **kwargs):
        """Wrap the function."""
        try:
            with context.TimeIt(message=func.__name__):
                return func(*args, **kwargs)
        except Exception as error:
            logger.error("{} : FAILED".format(func.__name__))
            raise error

    return wrapper


class Test(object):
    """Test the package."""

    # get the workspace_path path and remove it
    workspace_path = system.File(__file__).get_upstream(1).get_folder("test_workspace")
    project_name = "test_project"

    def __init__(self, *args, **kwargs):
        """Test the package."""

        # inheritance
        super(Test, self).__init__(*args, **kwargs)

        app = QApplication()

        # test the global working of the application
        with context.TimeIt(message="TEST DONE : Global Workings", log_level="info"):
            self.run()
            self.test_global_workings()

        app.exec_()

    # @context.ProfileIt(path=workspace_path.get_file("profile.profile"), execute=True)
    def test_global_workings(self):
        """Run the test methods."""

        self.run_ui()

    # management

    @log
    def run(self):
        """Test if the application can run."""
        open_api.run()

    @log
    def run_ui(self):
        """Test if the ui can run.

        Returns:
            MainWindow: Return the created MainWindow.
        """
        return open_ui.run()


if __name__ == "__main__":
    Test()
