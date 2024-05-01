"""Manage the application's dependency graphs."""


class DependencyGraph(object):
    """Manage the dependency graph."""

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        # inheritance
        super(DependencyGraph, self).__init__(*args, **kwargs)

        # create a variable that will list all the dependencies
        self.attributes_dependencies = dict()
        self.nodes_dependencies = dict()

    # methods

    def add_dependency(self, driven, driver):
        """Add a dependency.

        Arguments:
            driven (str): The item being driven by the driver.
            driver (str): The item that drives the driven.
        """
        # add the attribute dependency
        self.attributes_dependencies[driven.uuid] = driver

        # add the node dependency
        if driven.is_input and driven.is_builtin:
            node = self.parent
            if node in self.nodes_dependencies:
                self.nodes_dependencies[node.uuid].add(driver.parent)
            else:
                self.attributes_dependencies[node.uuid] = {driver.parent}

    def remove_dependency(self, driven):
        """Remove a dependency.

        Arguments:
            driven (str): The item being driven by the driver.
        """
        if driven.uuid in self.attributes_dependencies:
            # get the node the driven depends on
            driver_node = self.attributes_dependencies[driven.uuid].parent

            # remove the driven dependency
            del self.attributes_dependencies[driven.uuid]

            # check the node dependency
            if driven.is_input and driven.is_builtin:
                # check if another attribue of the driven node
                # depends on the driver node
                dependencies_count = 0
                for attribute in driven.parent.inputs:
                    driver = self.attributes_dependencies.get(attribute.uuid)
                    if driver and driver.parent is driver_node:
                        dependencies_count += 1
                        if dependencies_count > 1:
                            return

                # if the current dependency was the only one to the driver node
                # remove the node dependency
                self.nodes_dependencies[driver_node.uuid].remove(driver_node)
                if not self.nodes_dependencies[driver_node.uuid]:
                    del self.nodes_dependencies[driver_node.uuid]

    def get_evaluation_order(self, uuids):
        """Get the optimal evaluation order for the given list of nodes.

        Arguments:
            uuids (list): The uuids of the nodes to sort by evaluation order.

        Returns:
            list: The list of nodes uuids to evaluate sorted by evaluation order.
        """

        def dfs(uuid):
            """Perform a Depth-first Search to recursively get the evaluation order.

            Arguments:
                uuid (UUID): The node to start searching from.
            """
            # do not iterate multiple times on the same node
            if uuid in visited:
                return
            visited.add(uuid)

            # get the evaluation order
            if uuid in self.nodes_dependencies:
                for driver_node in self.nodes_dependencies[uuid]:
                    dfs(driver_node.uuid)
            order.append(uuid)

        # iterate through all the given nodes
        visited, order = set(), list()
        for uuid in uuids:
            dfs(uuid)
        return reversed(order)

    # cycles process

    def has_attributes_cycle(self, *keys):
        """Look for cycles in the attributes dependencies.

        Arguments:
            keys (list): The keys to check.
                If none given, parse all the dependencies.

        Returns:
            bool: True if there is a cycle in the dependencies, else False.
        """

        def dfs(key):
            """Perform a Depth-first Search to look for a cycle in the dependencies.

            Arguments:
                key (str): The key in the dependencies to start from.

            Returns:
                bool: True if a cycle has been detected, else False.
            """
            # if the key is already being checked, it means we're on a cycle
            if key in stack:
                return True

            # set the current key as beend checked to avoid checking it recursively
            if key in visited:
                return False
            visited.add(key)

            if key in self.attributes_dependencies:
                # set the current key as being checked and check its driver
                stack.add(key)
                if dfs(self.attributes_dependencies[key].uuid):
                    return True
                # remove the current key from the keys being checked
                stack.remove(key)
            return False

        # declare variables to keep track of the analysis
        stack = set()
        visited = set()
        # parse the given keys or all of them
        for key in keys or self.attributes_dependencies:
            if dfs(key):
                return True
        return False

    def has_nodes_cycle(self, *keys):
        """Look for cycles in the nodes dependencies.

        Arguments:
            keys (list): The keys to check.
                If none given, parse all the dependencies.

        Returns:
            bool: True if there is a cycle in the dependencies, else False.
        """

        def dfs(key):
            """Perform a Depth-first Search to look for a cycle in the dependencies.

            Arguments:
                key (str): The key in the dependencies to start from.

            Returns:
                bool: True if a cycle has been detected, else False.
            """
            # if the key is already being checked, it means we're on a cycle
            if key in stack:
                return True

            # set the current key as beend checked to avoid checking it recursively
            if key in visited:
                return False
            visited.add(key)

            if key in self.nodes_dependencies:
                # set the current key as being checked and check its driver
                stack.add(key)
                for item in self.nodes_dependencies[key]:
                    if dfs(item.uuid):
                        return True
                # remove the current key from the keys being checked
                stack.remove(key)
            return False

        # declare variables to keep track of the analysis
        stack = set()
        visited = set()
        # parse the given keys or all of them
        for key in keys or self.nodes_dependencies:
            if dfs(key):
                return True
        return False

    def has_cycle(self, driven):
        """Get if the dependencies hold a cycle of not.

        Arguments:
            driven (Attribute): The driven attribute to get the cycle of.

        Returns:
            bool: True if there is a cycle in the dependencies, else False.
        """
        return self.has_attributes_cycle(driven.uuid) or self.has_nodes_cycle(
            driven.parent.uuid
        )
