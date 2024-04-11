"""Test the package to see if it still works correctly."""

# setup the test environment
import random
import sys

from lbx_python import context, logging, system

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

        # test the global working of the application
        with context.TimeIt(message="TEST DONE : Global Workings", log_level="info"):
            self.run()
            self.test_global_workings()

        with context.TimeIt(message="TEST DONE : Heavy Project", log_level="info"):
            self.test_heavy_project(10**4)

    # @context.ProfileIt(path=workspace_path.get_file("profile.profile"), execute=True)
    def test_global_workings(self):
        """Run the test methods."""
        # create a custom project
        project = self.create()
        network = self.create_networks(project)[0]
        self.create_features(network)
        self.create_attributes(network)
        self.edit_attributes(network)
        self.connect_attributes(network)
        self.evaluation(network)
        self.save(project)
        # re generate the project from data
        self.load()

    # @context.ProfileIt(path=workspace_path.get_file("profile.profile"), execute=True)
    def test_heavy_project(self, size):
        """Test generating and loading a heavy project.

        Arguments:
            size (int): The amount of nodes to create.
        """
        # load a custom workspace
        workspace = open_api.loadWorkspace(self.workspace_path)
        # create the new project
        project = workspace.createProject(
            "heavy_{}".format(self.project_name), force=True
        )
        network = project.addNetwork()

        # test the heavy generation
        nodes = self.heavy_generation(network, size)
        self.heavy_connect(nodes)
        self.heavy_save(project)
        self.heavy_load(project)

    # management

    @log
    def run(self):
        """Test if the application can run."""
        open_api.run()

    # global test methods

    @log
    def create(self):
        """Test generating the pipeline.

        Returns:
            Project: The created project.
        """
        # create a custom workspace
        workspace = open_api.createWorkspace(self.workspace_path, force=True)
        # create the new project
        project = workspace.createProject(self.project_name, force=True)
        return project

    @log
    def create_networks(self, project):
        """Test creating networks.

        Arguments:
            project (Project): The project to work on.

        Returns:
            list: The created networks.
        """
        return [project.addNetwork(), project.addNetwork(name="test_network")]

    @log
    def create_features(self, network):
        """Test creating features.

        Arguments:
            network (Network): The network to work on.

        Returns:
            list: The created features.
        """
        return [
            network.addNode("Null", name="driver"),
            network.addNode("Null", name="driven"),
        ]

    @log
    def create_attributes(self, network):
        """Test creating attributes.

        Arguments:
            network (Network): The network to work on.
        """
        # get network's nodes
        nodes = (network.getNode("driver"), network.getNode("driven"))

        # create an attribute of each attribute type
        for attribute_type in open_api.listObjectTypes("attributes"):
            for node in nodes:
                node.addAttr(attribute_type)

    @log
    def edit_attributes(self, network):
        """Test editing attributes.

        Arguments:
            network (Network): The network to work on.
        """
        # get network's nodes
        driver = network.getNode("driver")

        # add and customize an attribute
        driver.addAttr("Float", name="test_attr", step=0.025)
        value, min_value = 3, -5
        driver.set("test_attr", value)
        driver.edit("test_attr", "min", min_value)

        # make sure the value were updated
        if driver.get("test_attr") != value:
            raise ValueError("The attribute value assignation don't work")
        if driver.query("test_attr", "min") != min_value:
            raise ValueError("The attribute edition don't work")

    @log
    def connect_attributes(self, network):
        """Test connecting the attributes.

        Arguments:
            network (Network): The network to work on.
        """
        # get network's nodes
        driver = network.getNode("driver")
        driven = network.getNode("driven")

        # create an attribute of each attribute type
        for attribute_type in open_api.listObjectTypes("attributes"):
            attribute_name = "{}1".format(attribute_type)
            driver.connect(attribute_name, driven.getAttr(attribute_name))

        # make sure the attributes udpate themselves
        driver.set("Float1", 15.26)
        if driver.get("Float1") != driven.get("Float1"):
            raise ValueError("The attribute's value change don't propagate")

    @log
    def evaluation(self, network):
        """Test the nodes evaluations.

        Arguments:
            network (Network): The network to work on.
        """
        # create a color maker node
        in_color = network.addNode("RGBAToHex", name="in_color")
        out_color = network.addNode("HexToRGBA", name="out_color")

        # connect the nodes together
        in_color.connect("output", out_color.getAttr("input"))

        # edit the in_color
        in_color.set("G", 0)
        if in_color.get("output") != "#FF00FF":
            raise RuntimeError("The nodes aren't evaluated after setting an attribute")

        # make sure the out_color has been reevaluated
        chanels = [out_color.get(c) for c in "RGBA"]
        if chanels != [255, 0, 255, 255]:
            raise RuntimeError("The evaluation doesn't propagate")

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
        workspace = open_api.loadWorkspace(self.workspace_path)

        # load the project
        project = workspace.loadProject(self.project_name)
        network = project.getNetwork("Network1")

        # get the created node
        node = network.getNode("driver")
        node.get("test_attr")

        # get the projects paths
        original_path = system.File(project.getPath())
        copy_path = original_path.directory.get_file("loaded_project.pipe")

        # make sure loading the project doesn't alter the data
        original_data = original_path.read()
        project.save(path=copy_path, indent=4)
        if copy_path.read() != original_data:
            raise RuntimeError("Loading a project alters it")

    # heavy test methods

    @log
    def heavy_generation(self, network, size):
        """Generate multiple nodes and attributes.

        Arguments:
            network (Network): The network to work on.
            size (int): The amount of nodes to create.

        Returns:
            list: The generated nodes.
        """
        # get the attributes and nodes types
        nodes_types = open_api.listObjectTypes("nodes")
        attribute_types = open_api.listObjectTypes("attributes")

        # create random nodes
        nodes = list()
        for _ in range(size):
            # create a node
            node = network.addNode(random.choice(nodes_types))
            nodes.append(node)
            # generate one of each basic attributes on the node
            for attribute_type in attribute_types:
                node.addAttr(attribute_type)

        return nodes

    @log
    def heavy_connect(self, nodes):
        """Connect multiple nodes together.

        Arguments:
            nodes (list): The lis of nodes to connect randomly.
        """
        # get the attributes types
        attribute_types = open_api.listObjectTypes("attributes")

        half_size = int(len(nodes) / 2)
        random.shuffle(nodes)
        for driver, driven in zip(nodes[:half_size], nodes[half_size:]):
            attribute_name = random.choice(attribute_types) + "1"
            driver.connect(attribute_name, driven.getAttr(attribute_name))

    @log
    def heavy_save(self, project):
        """Save the given project.

        Arguments:
            project (Project): The project to work on.
        """
        project.save()

    @log
    def heavy_load(self, project):
        """Load the given project.

        Arguments:
            project (Project): The project to work on.
        """
        # load a custom workspace
        workspace = open_api.loadWorkspace(self.workspace_path)
        # load the project
        workspace.loadProject(project.getName())


if __name__ == "__main__":
    Test()
