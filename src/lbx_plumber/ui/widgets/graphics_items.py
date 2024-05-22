"""Manage the application's graphics items."""

from lbx_qt import utils
from lbx_python import maths
from lbx_resources import resources
from lbx_qt.widgets import GraphicsItem, GraphicsImageItem, GraphicsPathItem
from PySide2.QtCore import QPointF, QRectF
from PySide2.QtGui import QBrush, QPainterPath, QPainterPathStroker

from lbx_plumber.internal import common


class NodeItem(GraphicsItem):
    """Manage the nodes items."""

    icon_size = 15
    title_height = 20
    title_color = "#F2F2F2"
    title_fill_color = "#6D6D6D"
    line_width = 2
    line_color = "#272727"
    selected_line_color = "#BD632F"
    background_fill_color = "#161616"
    corners_radius = 10

    def __init__(self, *args, **kwargs):
        """Initialize the object."""

        # inheritance
        super(NodeItem, self).__init__(*args, **kwargs)

        # set the item's flags
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)

        # add the node's items
        # add the icon
        image_item = GraphicsImageItem(resources.get_icon("ui/image.svg"), self)
        image_item.set_size(self.icon_size, self.icon_size)
        image_item.setPos(2 * self.line_width, 2 * self.line_width)
        # add the label
        self.name_label = self.add_simple_text("Untitled")
        self.name_label.setBrush(QBrush(utils.create_gui("Color", self.title_color)))
        self.name_label.setPos(2 * self.line_width + 17, 2 * self.line_width)
        # add the attributes
        self.attributes = list()
        for i, name in enumerate(common.SOCKET_TYPE_COLORS.keys()):
            item = AttributeItem(self, name, name)
            item.setPos(
                0, self.title_height + self.line_width + AttributeItem.height * i
            )
            self.attributes.append(item)

        # adapt the node size to its content
        self.set_size(
            80,
            self.title_height
            + 2 * self.line_width
            + (i + 1) * AttributeItem.height
            + self.corners_radius / 3,
        )

    # methods

    def set_width(self, width):
        """Set the width of the graphics item.

        Arguments:
            width (int, float): The width of the graphics item.
        """
        # inheritance
        super(NodeItem, self).set_width(width)

        # adapt the attributes width to
        for attribute in self.attributes:
            attribute.set_width(width)

    # drawing methods

    def shape(self):
        """Set the shape of the item.

        Returns:
            PainterPath: The item's shape path.
        """
        path = QPainterPath()
        path.addRoundedRect(
            self.boundingRect(), self.corners_radius, self.corners_radius
        )
        return path

    def paint(self, painter, option, widget=None):
        """Override the paint method to add custom behaviours.

        Arguments:
            painter (QPainter): The painter to use to draw the item.
            option (QStyleOptionGraphicsItem): To add style options for the item.

        Keyword Arguments:
            widget (QWidget, optional): The widget to paint on. Default to None.
        """
        # inheritance
        super(NodeItem, self).paint(painter, option, widget)

        # get the rect of the item
        bounding_rect = self.boundingRect()
        x, y, width, height = bounding_rect.getCoords()

        # get the color to draw the outline with
        outline_color = (
            self.selected_line_color if self.isSelected() else self.line_color
        )

        # draw the main shape
        utils.draw_rounded_rect(
            painter,
            rect=bounding_rect,
            radius_x=self.corners_radius,
            radius_y=self.corners_radius,
            line_color=None,
            fill_color=self.background_fill_color,
        )

        # mask the drawing within the shape
        painter.setClipPath(self.shape())
        # draw the title shape
        utils.draw_rect(
            painter,
            rect=QRectF(x, y, width, self.title_height),
            radius_x=self.corners_radius,
            radius_y=self.corners_radius,
            line_color=self.line_color,
            fill_color=self.title_fill_color,
        )
        # remove the clipping region
        painter.setClipping(False)

        # draw the selection outline
        utils.draw_rounded_rect(
            painter,
            rect=bounding_rect,
            radius_x=self.corners_radius,
            radius_y=self.corners_radius,
            line_color=outline_color,
            line_width=self.line_width,
            fill_color=None,
        )


class AttributeItem(GraphicsItem):
    """Manage the sockets items."""

    height = 20
    text_color = "#C2C2C2"

    def __init__(self, parent, name, data_type, *args, **kwargs):
        """Initialize the object."""

        # keep the parent in memory
        self.data_type = data_type
        self.parent = parent

        # inheritance
        super(AttributeItem, self).__init__(parent=parent, *args, **kwargs)

        # populate the item with its content
        self.name_label = self.add_simple_text(name)
        self.name_label.setBrush(QBrush(utils.create_gui("Color", self.text_color)))
        self.name_label.setPos(
            SocketItem.radius + NodeItem.line_width, NodeItem.line_width + 1
        )
        self.input_socket = SocketItem(self, data_type)
        self.input_socket.setPos(
            -SocketItem.radius, self.height / 2 - SocketItem.radius
        )
        self.output_socket = SocketItem(self, data_type)

        # set the item's height
        self.set_height(self.height)

    # methods

    def set_width(self, width):
        """Set the width of the graphics item.

        Arguments:
            width (int, float): The width of the graphics item.
        """
        # inheritance
        super(AttributeItem, self).set_width(width)

        # adapt the output socket
        self.output_socket.setPos(
            width - SocketItem.radius, self.height / 2 - SocketItem.radius
        )


class SocketItem(GraphicsItem):
    """Manage the sockets items."""

    radius = 4
    hover_color = "#C4C4C4"
    is_hovered = False

    def __init__(self, parent, data_type, *args, **kwargs):
        """Initialize the object."""

        # keep the parent in memory
        self.color = common.SOCKET_TYPE_COLORS[data_type]
        self.parent = parent

        # inheritance
        super(SocketItem, self).__init__(parent=parent, *args, **kwargs)

        # setup the socket
        self.setAcceptHoverEvents(True)

        # set the socket's size
        self.set_size(2 * self.radius, 2 * self.radius)

    # paint methods

    def shape(self):
        """Set the shape of the item.

        Returns:
            PainterPath: The item's shape path.
        """
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget=None):
        """Override the paint method to add custom behaviours.

        Arguments:
            painter (QPainter): The painter to use to draw the item.
            option (QStyleOptionGraphicsItem): To add style options for the item.

        Keyword Arguments:
            widget (QWidget, optional): The widget to paint on. Default to None.
        """
        # inheritance
        super(SocketItem, self).paint(painter, option, widget)

        # get the color to draw the outline with
        if self.parent.parent.isSelected():
            outline_color = self.parent.parent.selected_line_color
        else:
            outline_color = self.parent.parent.line_color

        # draw the socket
        utils.draw_circle(
            painter,
            self.boundingRect(),
            line_width=self.parent.parent.line_width,
            line_color=outline_color,
            fill_color=self.hover_color if self.is_hovered else self.color,
        )

    # events

    def hoverEnterEvent(self, event):
        """Override the hoverEnterEvent.

        Arguments:
            event (QEvent): The event to process.
        """
        self.is_hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        """Override the hoverEnterEvent.

        Arguments:
            event (QEvent): The event to process.
        """
        self.is_hovered = False
        self.update()


class ConnectionItem(GraphicsPathItem):
    """Manage the connection items."""

    shape_type = "bezier"

    line_width = 2
    line_color = "#161616"
    selected_line_color = "#BD632F"
    hover_color = "#C4C4C4"
    is_hovered = False

    def __init__(self, source, destination, shape_type=None, *args, **kwargs):
        """Initialize the object."""

        # keep the connected items in memory
        self.__source = source
        self.__destination = destination
        self.shape_type = shape_type or self.shape_type

        # inheritance
        super(ConnectionItem, self).__init__(*args, **kwargs)

        # setup the item
        self.setFlags(self.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

    # methods

    def boundingRect(self):
        """Get the bounding rect of the current item.

        The first thing the item need is a bounding rect.
        This methods gives it a default one setup with the item's width and height.

        Returns:
            QRectF: The bounding rect of the item.
        """
        # get the source and destination
        a = self.__source
        b = self.__destination
        # process the bounding rect
        return QRectF(
            a.scenePos() + QPointF(a.get_width() / 2, a.get_height() / 2),
            b.scenePos() + QPointF(b.get_width() / 2, b.get_height() / 2),
        )

    def get_width(self):
        """Get the width of the graphics item.

        Returns:
            int, float: The width of the graphics item.
        """
        return self.boundingRect().width()

    def get_height(self):
        """Get the height of the graphics item.

        Returns:
            int, float: The height of the graphics item.
        """
        return self.boundingRect().height()

    # paint methods

    def shape(self):
        """Set the shape of the item.

        Returns:
            PainterPath: The item's shape path.
        """
        # use a QPainterPathStroker to have a thicker hover area
        stroke = QPainterPathStroker()
        stroke.setWidth(self.line_width)
        return stroke.createStroke(self.path())

    def paint(self, painter, option, widget=None):
        """Override the paint method to add custom behaviours.

        Arguments:
            painter (QPainter): The painter to use to draw the item.
            option (QStyleOptionGraphicsItem): To add style options for the item.

        Keyword Arguments:
            widget (QWidget, optional): The widget to paint on. Default to None.
        """
        # inheritance
        super(ConnectionItem, self).paint(painter, option, widget)

        # get the color to draw with
        if self.is_hovered:
            color = self.hover_color
        elif self.isSelected():
            color = self.selected_line_color
        else:
            color = self.line_color

        # draw the line
        rect = self.boundingRect()
        start = rect.topLeft()
        end = rect.bottomRight()

        # create the path
        path = QPainterPath()
        path.moveTo(start)
        # process the path
        if self.shape_type == "bezier":
            # process the offset of the cubic points
            mid = (end - start) / 2
            offset = max(mid.x(), 16 * SocketItem.radius)
            factor = 1 / (1 + pow(10, -0.25 * maths.clamp(abs(mid.y()), 0, 20) + 2))
            # create the cubic path
            start.setX(start.x() + offset * factor)
            end.setX(end.x() - offset * factor)
            path.cubicTo(start, end, rect.bottomRight())
        elif self.shape_type == "line":
            path.lineTo(end)
        elif self.shape_type == "square":
            mid = (start + end) / 2
            path.lineTo(mid.x(), start.y())
            path.lineTo(mid.x(), end.y())
            path.lineTo(end)
        elif self.shape_type == "rounded":
            # get the available space
            width = rect.width()
            height = rect.height()
            x_direction = 1 if width >= 0 else -1
            y_direction = 1 if height >= 0 else -1

            # process the offsets
            socket_spacing = 8 * SocketItem.radius
            base_width = min(abs(width) / 2, abs(height) / 2, socket_spacing)

            # process source rect
            rect1 = QRectF(
                start,
                QPointF(start.x() + base_width, start.y() + y_direction * base_width),
            )
            # process destination rect
            x = min(rect1.bottomRight().x(), end.x() - base_width)
            y = rect1.bottomRight().y()
            size = min(abs(x - end.x()), abs(y - end.y()))
            rect4 = QRectF(
                QPointF(x, end.y() - y_direction * size),
                QPointF(x + size, end.y()),
            )
            # process the mid rects for when source is on the other side of destination
            mid = (rect1.bottomRight() + rect4.topLeft()) / 2
            size = max(
                min(
                    abs(rect1.right() - rect4.left()),
                    abs(rect1.bottom() - rect4.top()) + 2,
                ),
                0,
            )
            rect2 = QRectF(
                QPointF(rect1.right(), mid.y() - y_direction * size),
                QPointF(rect1.right() + x_direction * size, mid.y()),
            )
            rect3 = QRectF(
                QPointF(rect4.left() - x_direction * size, mid.y()),
                QPointF(rect4.left(), mid.y() + y_direction * size),
            )

            # drax the arcs within the rects
            path.arcTo(rect1, 90, -90)
            path.arcTo(rect2, 180, 90)
            path.arcTo(rect3, 90, -90)
            path.arcTo(rect4, 180, 90)
            path.lineTo(end)

        else:
            raise ValueError("Invalid shape type")

        # set the created path as the item's path
        self.setPath(path)
        # draw the path
        utils.draw_path(
            painter,
            path,
            line_width=self.line_width,
            line_color=color,
            fill_color=None,
        )

    # events

    def hoverEnterEvent(self, event):
        """Override the hoverEnterEvent.

        Arguments:
            event (QEvent): The event to process.
        """
        self.is_hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        """Override the hoverEnterEvent.

        Arguments:
            event (QEvent): The event to process.
        """
        self.is_hovered = False
        self.update()
