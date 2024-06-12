import sys
from PySide2.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
)
from PySide2.QtGui import QCursor, QPainter, QPixmap, QTransform
from PySide2.QtCore import Qt, QRectF

from lbx_python import maths
from lbx_qt import utils, widgets
from lbx_resources import resources


class TransformableItemAnchorPoint(widgets.GraphicsItem):
    """Manage an anchor point item."""

    def __init__(
        self,
        parent,
        line_width=3,
        line_color="#000000",
        line_color_hovered="#ABB2BF",
        line_color_selected="#BD632F",
        radius=4,
        *args,
        **kwargs
    ):
        """Initialize the object."""

        # keep the parent item in memory and the paint variables too
        self.parent = parent
        self.line_width = line_width
        self.line_color = line_color
        self.line_color_hovered = line_color_hovered
        self.line_color_selected = line_color_selected

        # inheritance
        super(TransformableItemAnchorPoint, self).__init__(
            parent=parent, *args, **kwargs
        )

        # setup the item
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # set the size of the anchor
        self.setBoundingRect(QRectF(-radius, -radius, 2 * radius, 2 * radius))

    # methods

    def paint(self, painter, *args, **kwargs):
        """Override the paint method to add custom behaviours.

        Arguments:
            painter (QPainter): The painter to use to draw the item.
            option (QStyleOptionGraphicsItem): To add style options for the item.

        Keyword Arguments:
            widget (QWidget, optional): The widget to paint on. Default to None.
        """
        # inheritance
        super(TransformableItemAnchorPoint, self).paint(painter, *args, **kwargs)

        # get the color to draw the anchor with
        if self.isSelected():
            color = self.line_color_selected
        elif self.is_hovered:
            color = self.line_color_hovered
        else:
            color = self.line_color

        # draw a point for the anchor
        utils.draw_plus(
            painter, self.boundingRect(), line_width=self.line_width, line_color=color
        )

    def setPos(self, *args, **kwargs):
        """Override the setPos method to edit the position of the anchor point."""
        self.parent.setTransformOriginPoint(*args, **kwargs)

    # events

    def hoverEnterEvent(self, event):
        """Override the hoverEnterEvent.

        Arguments:
            event (QEvent): The event to process.
        """
        # inheritance
        super(TransformableItemAnchorPoint, self).hoverEnterEvent(event)

        # update the item
        self.update()

    def hoverLeaveEvent(self, event):
        """Override the hoverEnterEvent.

        Arguments:
            event (QEvent): The event to process.
        """
        # inheritance
        super(TransformableItemAnchorPoint, self).hoverLeaveEvent(event)

        # update the item
        self.update()

    def mouseMoveEvent(self, event):
        """Override the mouseMoveEvent method.

        Arguments:
            event (QEvent): The event that has been triggered.
        """
        # inheritance
        super(TransformableItemAnchorPoint, self).mouseMoveEvent(event)
        # update the anchor point of the parent item when the anchor is moved
        self.parent.setTransformOriginPoint(self.pos())

    def mouseReleaseEvent(self, event):
        """Override the mouseReleaseEvent.

        Arguments:
            event (QEvent): The event to process.
        """
        # inheritance
        super(TransformableItemAnchorPoint, self).mouseReleaseEvent(event)

        # deselect the anchor
        self.setSelected(False)


class TransformableItem(widgets.GraphicsRectItem):
    """Manage the transformable items."""

    # define hover areas
    LEFT_AREA = 0
    TOP_AREA = 1
    RIGHT_AREA = 2
    BOTTOM_AREA = 3
    TOP_LEFT_AREA = 4
    TOP_RIGHT_AREA = 5
    BOTTOM_RIGHT_AREA = 6
    BOTTOM_LEFT_AREA = 7

    # the modifiers to control the transforms
    scale_uniform_modifiers = Qt.ShiftModifier
    scale_center_modifiers = Qt.AltModifier
    rotate_modifiers = Qt.ControlModifier

    hovered_area = None
    scale_factor = 1.0
    angle = 0.0
    edges_margins = 10

    # private variables
    __is_locked = False
    __is_in_edit_mode = False
    __minimum_width = 20
    __maximum_width = None
    __minimum_height = 20
    __maximum_height = None
    __extend_cursor_icon = resources.get_icon("cursors/extend_cursor.svg")

    def __init__(self, *args, **kwargs):
        """Initialize the object."""

        # inheritance
        super(TransformableItem, self).__init__(*args, **kwargs)

        # setup the item
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # add an anchor point to the item
        self.anchor = TransformableItemAnchorPoint(self)

        # set an initial rect
        self.set_size(self.get_minimum_width(), self.get_minimum_height())
        self.center_anchor_point()

        # make sure the item is not in edit mode
        self.edit(True)

    # methods

    def lock(self):
        """Lock the item."""
        self.set_locked(True)

    def unlock(self):
        """Unlock the item."""
        self.set_locked(False)

    def set_locked(self, value):
        """Lock or unlock the item.

        Arguments:
            value (bool): True to lock the item, else False.
        """
        self.__is_locked = value
        if value:
            self.edit(False)

    def is_locked(self):
        """Get if the current item is locked.

        Returns:
            bool: True if the item is locked, else False.
        """
        return self.__is_locked

    def edit(self, value):
        """Set the item in edit mode to be able to resize it and modify its anchor.

        Arguments:
            value (bool): True to edit the item, else False.
        """
        self.__is_in_edit_mode = value
        self.anchor.setVisible(value)

    def is_in_edit_mode(self):
        """Get if the item is in edit mode.

        Returns:
            bool: True if the item is in edit mode, else False.
        """
        return self.__is_in_edit_mode

    # size methods

    def setRect(self, rect):
        """Set the bounding rect of the current item.

        Arguments:
            rect (QRectF): The rect to set.
        """
        # get the current rect
        current_rect = self.rect()
        x, y = self.transformOriginPoint().toTuple()

        # inheritance
        super(TransformableItem, self).setRect(rect)

        # get the relative coordinates of the anchor point
        new_x, new_y = utils.get_rect_relative_coordinates(x, y, current_rect, rect)
        # update the anchor coordinates
        self.setTransformOriginPoint(new_x, new_y)

    def get_minimum_width(self):
        """Get the minimum width of the current widget.

        Returns:
            int: The minimum width of the current item.
        """
        return self.__minimum_width

    def set_minimum_width(self, value):
        """Set the minimum width of the current item.

        Arguments:
            value (int): The minimum width of the current item.
        """
        self.__minimum_width = value

    def get_minimum_height(self):
        """Get the minimum height of the current widget.

        Returns:
            int: The minimum height of the current item.
        """
        return self.__minimum_height

    def set_minimum_height(self, value):
        """Set the minimum height of the current item.

        Arguments:
            value (int): The minimum height of the current item.
        """
        self.__minimum_height = value

    def get_minimum_size(self):
        """Get the minimum size of the current widget.

        Returns:
            tuple: The minimum size of the current item.
        """
        return self.get_minimum_width(), self.get_minimum_height()

    def set_minimum_size(self, width, height):
        """Set the minimum size of the current item.

        Arguments:
            width (int, float): The minimum width of the current item.
            height (int, float): The minimum height of the current item.
        """
        self.set_minimum_width(width), self.set_minimum_height(height)

    def get_maximum_width(self):
        """Get the maximum width of the current widget.

        Returns:
            int: The maximum width of the current item.
        """
        return self.__maximum_width

    def set_maximum_width(self, value):
        """Set the maximum width of the current item.

        Arguments:
            value (int): The maximum width of the current item.
        """
        self.__maximum_width = value

    def get_maximum_height(self):
        """Get the maximum height of the current widget.

        Returns:
            int: The maximum height of the current item.
        """
        return self.__maximum_height

    def set_maximum_height(self, value):
        """Set the maximum height of the current item.

        Arguments:
            value (int): The maximum height of the current item.
        """
        self.__maximum_height = value

    def get_maximum_size(self):
        """Get the maximum size of the current widget.

        Returns:
            tuple: The maximum size of the current item.
        """
        return self.get_maximum_width(), self.get_maximum_height()

    def set_maximum_size(self, width, height):
        """Set the maximum size of the current item.

        Arguments:
            width (int, float): The maximum width of the current item.
            height (int, float): The maximum height of the current item.
        """
        self.set_maximum_width(width), self.set_maximum_height(height)

    def set_fixed_width(self, value):
        """Set the fixed width of the current item.

        Arguments:
            value (int): The fixed width of the current item.
        """
        self.set_minimum_width(value)
        self.set_maximum_width(value)

    def set_fixed_height(self, value):
        """Set the fixed height of the current item.

        Arguments:
            value (int): The fixed height of the current item.
        """
        self.set_minimum_height(value)
        self.set_maximum_height(value)

    def set_fixed_size(self, width, height):
        """Set the fixed size of the item.

        Arguments:
            width (int, float): The fixed width of the current item.
            height (int, float): The fixed height of the current item.
        """
        self.set_minimum_size(width, height)
        self.set_maximum_size(width, height)

    # paint methods

    def paint(self, painter, option, widget=None):
        """Override the paint method to add custom behaviours.

        Arguments:
            painter (QPainter): The painter to use to draw the item.
            option (QStyleOptionGraphicsItem): To add style options for the item.

        Keyword Arguments:
            widget (QWidget, optional): The widget to paint on. Default to None.
        """
        # inheritance
        super(TransformableItem, self).paint(painter, option, widget)

        if self.is_in_edit_mode():
            utils.draw_rect(
                painter,
                self.rect(),
                line_color="#000000",
                line_width=2,
                fill_color=None,
            )

    # transform methods

    def transformOriginPoint(self):
        """Override the transformOriginPoint method.

        Returns:
            QPointF: The position of the anchor.
        """
        return self.anchor.pos()

    def setTransformOriginPoint(self, *args, **kwargs):
        """Override the setTransformOriginPoint method."""

        # get the current position of the item
        # to restore it later if the anchor point changes and the item has a rotation
        start_pos = self.sceneBoundingRect().topLeft()

        # inheritance
        super(TransformableItem, self).setTransformOriginPoint(*args, **kwargs)

        # get the offset that got created by moving the anchor point
        # with the item having a rotation
        offset = start_pos - self.sceneBoundingRect().topLeft()

        # move the item and the anchor point to seamlessly move the anchor point
        self.setPos(self.pos() + offset)
        super(TransformableItemAnchorPoint, self.anchor).setPos(
            super(TransformableItem, self).transformOriginPoint()
        )

    def update_anchor_point(self, current_rect, new_rect):
        """Update the anchor point to stay on the same proportional spot.

        Arguments:
            current_rect (QRectF): The current rect.
            new_rect (QRectF): The new rect.
        """
        anchor_x, anchor_y = self.transformOriginPoint().toTuple()
        x = maths.remap(
            anchor_x,
            current_rect.left(),
            current_rect.right(),
            new_rect.left(),
            new_rect.right(),
        )
        y = maths.remap(
            anchor_y,
            current_rect.top(),
            current_rect.bottom(),
            new_rect.top(),
            new_rect.bottom(),
        )
        self.setTransformOriginPoint(x, y)

    def center_anchor_point(self):
        """Center the anchor point."""
        self.setTransformOriginPoint(self.boundingRect().center())

    # events

    def resize_event(self, event):  # noqa C901
        """Resize the item.

        Arguments:
            event (QEvent): The event that has been triggered.
        """
        if not self.is_in_edit_mode():
            return

        # get the current modifiers
        modifiers = event.modifiers()
        center = modifiers & self.scale_center_modifiers
        uniform = modifiers & self.scale_uniform_modifiers

        # get the needed coordinates
        rect = self.rect()
        current_rect = QRectF(rect)  # keep the current rect in memory
        cursor_pos = event.pos()
        cursor_x, cursor_y = cursor_pos.x(), cursor_pos.y()
        # get the size limits
        min_width, min_height = self.get_minimum_size()
        max_width, max_height = self.get_maximum_size()

        # get the variables to edit the rect with
        width = current_width = rect.width()
        height = current_height = rect.height()

        # process the new width and height
        if self.hovered_area in (
            self.TOP_LEFT_AREA,
            self.BOTTOM_LEFT_AREA,
            self.LEFT_AREA,
        ):
            width = maths.clamp(rect.right() - cursor_x, min_width, max_width)
        if self.hovered_area in (
            self.TOP_LEFT_AREA,
            self.TOP_RIGHT_AREA,
            self.TOP_AREA,
        ):
            height = maths.clamp(rect.bottom() - cursor_y, min_height, max_height)
        if self.hovered_area in (
            self.TOP_RIGHT_AREA,
            self.BOTTOM_RIGHT_AREA,
            self.RIGHT_AREA,
        ):
            width = maths.clamp(cursor_x - rect.left(), min_width, max_width)
        if self.hovered_area in (
            self.BOTTOM_LEFT_AREA,
            self.BOTTOM_RIGHT_AREA,
            self.BOTTOM_AREA,
        ):
            height = maths.clamp(cursor_y - rect.top(), min_height, max_height)

        # make sure the aspect ratio is kept
        if uniform:
            aspect_ratio = current_width / current_height
            if self.hovered_area in (
                self.TOP_LEFT_AREA,
                self.TOP_RIGHT_AREA,
                self.BOTTOM_RIGHT_AREA,
                self.BOTTOM_LEFT_AREA,
                self.LEFT_AREA,
                self.RIGHT_AREA,
            ):
                height = width / aspect_ratio
            else:
                width = height * aspect_ratio

        # resize and move the rect
        rect.setWidth(width)
        rect.setHeight(height)
        if self.hovered_area is self.TOP_LEFT_AREA:
            rect.translate(current_width - width, current_height - height)
        elif self.hovered_area in (self.LEFT_AREA, self.BOTTOM_LEFT_AREA):
            rect.translate(current_width - width, 0)
        elif self.hovered_area in (self.TOP_RIGHT_AREA, self.TOP_AREA):
            rect.translate(0, current_height - height)

        # resize arround the anchor point
        if center:
            x, y = self.transformOriginPoint().toTuple()
            new_x, new_y = utils.get_rect_relative_coordinates(x, y, current_rect, rect)
            rect.translate(x - new_x, y - new_y)

        # set the new bounding rect of the item
        self.setRect(rect)

    def rotate_event(self, event):
        """Rotate the item.

        Arguments:
            event (QEvent): The event that has been triggered.
        """
        if self.is_locked():
            return

        # get the current rect
        rect = self.rect()
        # get the corner beeing dragged
        if self.hovered_area == self.TOP_LEFT_AREA:
            corner = rect.topLeft()
        elif self.hovered_area == self.TOP_RIGHT_AREA:
            corner = rect.topRight()
        elif self.hovered_area == self.BOTTOM_LEFT_AREA:
            corner = rect.bottomLeft()
        elif self.hovered_area == self.BOTTOM_RIGHT_AREA:
            corner = rect.bottomRight()

        # process the new angle
        self.angle += maths.angle_between_points(
            anchor=self.transformOriginPoint().toTuple(),
            point1=corner.toTuple(),
            point2=event.pos().toTuple(),
            signed=True,
        )
        self.setRotation(self.angle)

    def hoverMoveEvent(self, event):  # naqa C901
        """Override the hoverMoveEvent method.

        Arguments:
            event (QEvent): The event that has been triggered.
        """
        if self.is_locked():
            return

        # inheritance
        super(TransformableItem, self).hoverMoveEvent(event)

        # get the cursor position
        pos = event.pos()
        x, y = pos.x(), pos.y()
        # get wich side the cursor hovers on
        rect = self.boundingRect()
        hover_left = maths.is_in_tolerance(x, rect.left(), self.edges_margins)
        hover_right = maths.is_in_tolerance(x, rect.right(), self.edges_margins)
        hover_top = maths.is_in_tolerance(y, rect.top(), self.edges_margins)
        hover_bottom = maths.is_in_tolerance(y, rect.bottom(), self.edges_margins)

        # get how many edges are hovered
        count = sum(map(int, (hover_left, hover_right, hover_top, hover_bottom)))

        # set the normal arrow and skip if no edge hovered
        if not count:
            self.hovered_area = None
            self.setCursor(Qt.ArrowCursor)
            return

        # get wich cursor to show wether we are resizing the item of rotating it
        if count == 2 and event.modifiers() == self.rotate_modifiers:
            rotate = True
            cursor = Qt.OpenHandCursor
        else:
            rotate = False
            cursor = QPixmap(self.__extend_cursor_icon).scaled(32, 32)

        # update the variables and cursor depending on the cursor hovering
        if hover_left:
            if hover_top:
                self.hovered_area = self.TOP_LEFT_AREA
            elif hover_bottom:
                self.hovered_area = self.BOTTOM_LEFT_AREA
            else:
                self.hovered_area = self.LEFT_AREA
        elif hover_right:
            if hover_top:
                self.hovered_area = self.TOP_RIGHT_AREA
            elif hover_bottom:
                self.hovered_area = self.BOTTOM_RIGHT_AREA
            else:
                self.hovered_area = self.RIGHT_AREA
        elif hover_top:
            self.hovered_area = self.TOP_AREA
        elif hover_bottom:
            self.hovered_area = self.BOTTOM_AREA

        # orient the resizing cursor if necessary depending on the hovered edge
        if not rotate:
            angle = self.angle
            if self.hovered_area in (self.BOTTOM_LEFT_AREA, self.TOP_RIGHT_AREA):
                angle -= 45
            elif self.hovered_area in (self.TOP_LEFT_AREA, self.BOTTOM_RIGHT_AREA):
                angle += 45
            elif self.hovered_area in (self.TOP_AREA, self.BOTTOM_AREA):
                angle += 90
            cursor = cursor.transformed(QTransform().rotate(angle))

        # set the cursor's shape
        self.setCursor(QCursor(cursor))

    def mousePressEvent(self, event):
        """Override the mousePressEvent method.

        Arguments:
            event (QEvent): The event that has been triggered.
        """
        # close the cursor's hand if needed
        if self.cursor().shape() == Qt.OpenHandCursor:
            self.setCursor(Qt.ClosedHandCursor)

        # inheritance
        super(TransformableItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Override the mouseMoveEvent method.

        Arguments:
            event (QEvent): The event that has been triggered.
        """
        if self.is_locked():
            return

        # rotate
        if event.modifiers() == self.rotate_modifiers and self.hovered_area in (
            self.TOP_LEFT_AREA,
            self.TOP_RIGHT_AREA,
            self.BOTTOM_LEFT_AREA,
            self.BOTTOM_RIGHT_AREA,
        ):
            self.rotate_event(event)
        # scale
        elif self.hovered_area is not None:
            self.resize_event(event)
        # inheritance
        else:
            super(TransformableItem, self).mouseMoveEvent(event)


class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 800, 600)

        rect_item = TransformableItem()
        rect_item.setRect(QRectF(100, 100, 150, 150))
        self.scene.addItem(rect_item)

        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MainWindow()
    view.setWindowTitle("QGraphicsItem Transform Example")
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
