"""Manage the application's graphics scenes."""

from lbx_qt import utils
from lbx_qt.widgets import GraphicsScene

from lbx_plumber.ui.widgets import graphics_items


class NetworkScene(GraphicsScene):
    """Manage the network scene."""

    def __init__(self, parent=None, *args, **kwargs):
        """Initialize the object."""

        # inheritance
        super(NetworkScene, self).__init__(parent=parent, *args, **kwargs)

        # set the scene size
        self.setSceneRect(-500, -500, 1000, 1000)
        # create background
        self.setBackgroundBrush(utils.create_gui("Color", "#393939"))

        # TODO remove
        # add nodes
        node1 = self.add_node(self)
        node2 = self.add_node(self, 100, 0)
        # add connection
        self.add_connection(
            node1.attributes[0].output_socket,
            node2.attributes[2].input_socket,
        )
        self.add_connection(
            node1.attributes[1].output_socket,
            node2.attributes[1].input_socket,
        )
        self.add_connection(
            node1.attributes[7].output_socket,
            node2.attributes[7].input_socket,
        )

    # methods

    def add_node(self, node, *args, **kwargs):
        """Add a node item to the scene.

        Arguments:
            node (Node): The node to add.

        Returns:
            NodeItem: The created node item.
        """
        item = graphics_items.NodeItem()
        self.add_item(item, *args, **kwargs)
        return item

    def add_connection(self, source, destination, *args, **kwargs):
        """Add a connection to the scene.

        Arguments:
            source (str): The connection's source.
            destination (str): The connection's destination.

        Returns:
            ConnectionItem: The created connection item.
        """
        item = graphics_items.ConnectionItem(source, destination)
        self.add_item(item, *args, **kwargs)
        return item

    # paint methods

    def drawBackground(self, painter, rect):
        """Draw the scene's background.

        Arguments:
            painter (QPainter): The painter in charge of painting the background.
            rect (QRect): The zone to paint in.
        """
        # inheritance
        super(NetworkScene, self).drawBackground(painter, rect)

        # draw light grid
        utils.draw_grid(painter, rect, size=20, line_color="#2F2F2F", line_width=1)
        # draw dark grid
        utils.draw_grid(painter, rect, size=100, line_color="#292929", line_width=2)

        # draw the scene space
        self.draw_scene_rect(painter, fill_color=None)

    # events

    def mousePressEvent(self, event):
        """Override the mousePressEvent method.

        Arguments:
            event (QEvent): The event that has been triggered.
        """
        # clear the selection if no item selected
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if item is None:
            self.clearSelection()

        # perform the normal event
        super(NetworkScene, self).mousePressEvent(event)
