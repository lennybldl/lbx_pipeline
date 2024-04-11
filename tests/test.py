"""Test the package to see if it still works correctly."""

# setup the test environment
import sys

from lbx_python_core import context, logging, system

sys.path.insert(0, system.File(__file__).get_upstream(2) + "/src")


from lbx_pipeline import open_api  # noqa E402

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
            result = func(*args, **kwargs)
            logger.info("{}: success".format(func.__name__))
            return result
        except Exception as err:
            logger.error("{}: failed".format(func.__name__))
            raise err

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

        # run the test method
        self.test()

    # @context.TimeIt()
    @context.TimeIt()
    def test(self):
        """Run the test methods."""
        self.run()
        # create a custom project
        project = self.create()
        self.create_features(project)
        self.create_attributes(project)
        self.save(project)
        # re generate the project from data
        self.load()

    # management tests

    @log
    def run(self):
        """Test if the application can run."""
        open_api.run()

    @log
    def create(self):
        """Test generating the pipeline.

        Returns:
            Project: The created project.
        """
        # create a custom workspace
        workspace = open_api.create_workspace(self.workspace_path, force=True)
        # create the new project
        project = workspace.create_project(self.project_name, force=True)
        return project

    @log
    def save(self, project):
        """Test saving the project.

        Arguments:
            project (Project): The project to work on.
        """
        project.save(indent=4)

    @log
    def load(self):
        """Test loading the project."""

        # load a custom workspace
        workspace = open_api.load_workspace(self.workspace_path)

        # create the new project
        project = workspace.load_project(self.project_name)

        # get the created node
        node = project.get_feature("driver")
        node.query("driver")

        # make sure loading the project doesn't alter the data
        original_data = project.read()
        project.save(path=project.directory.get_file("loaded_project.pipe"), indent=4)
        if project.read() != original_data:
            raise RuntimeError("Loading a project alters it")

    # features tests

    @log
    def create_features(self, project):
        """Test creating features.

        Arguments:
            project (Project): The project to work on.
        """
        # create a driver and driven node
        project.add_node("Null", name="driver")
        project.add_node("Null", name="driven")

    @log
    def create_attributes(self, project):
        """Test creating attributes.

        Arguments:
            project (Project): The project to work on.
        """
        # get project's nodes
        driver = project.get_feature("driver")
        driven = project.get_feature("driven")

        # add and customize an attribute
        driver.add_attribute("Float", name="driver", step=0.025)
        driver.edit("driver", 3)
        driver.edit("driver", -5, param="min")

        # create an attribute of each attribute type
        for attribute_type in open_api.get_object_types("attributes"):
            for node in (driver, driven):
                node.add_attribute(attribute_type)


if __name__ == "__main__":
    Test()
