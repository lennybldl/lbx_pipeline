"""Manage the application's graphics views."""

from PySide2.QtCore import Qt
from lbx_qt.widgets import GraphicsView

from lbx_plumber.ui.widgets import graphics_scenes


class NetworkView(GraphicsView):
    """Manage the network view."""

    # movement variables
    is_panning = False
    zoom_factor = 1.25
    zoom = 0
    zoom_step = 1
    zoom_range = (-10, 20)

    def __init__(self, parent=None, *args, **kwargs):
        """Initialize the object."""

        # inheritance
        super(NetworkView, self).__init__(parent=parent, *args, **kwargs)

        # setup the view and scene
        # add a scene to the view
        self.add_scene(graphics_scenes.NetworkScene(self))
        # enable antialiasing
        self.set_antialiasing(True)
        # update the full view to avoid caches artefacts
        self.set_update_mode("all")
        # zoom under mouse
        self.set_transformation_anchor("mouse")
        # hide the scroll bars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # events

    def mousePressEvent(self, event, *args, **kwargs):
        """Add navigation control.

        Arguments:
            event (QMouseEvent): The PySide2 QMouseEvent.
        """
        # implement panning with drag in viewport
        if event.button() == Qt.LeftButton:
            self.is_panning = True
            self.setDragMode(self.ScrollHandDrag)

        # inheritance
        super(NetworkView, self).mousePressEvent(event, *args, **kwargs)

    def mouseReleaseEvent(self, event, *args, **kwargs):
        """Add navigation control.

        Arguments:
            event (QMouseEvent): The PySide2 QMouseEvent.
        """
        # stop panning
        if event.button() == Qt.LeftButton and self.is_panning:
            self.is_panning = False
            self.setDragMode(self.NoDrag)

        # inheritance
        super(NetworkView, self).mouseReleaseEvent(event, *args, **kwargs)

    def wheelEvent(self, event, *args, **kwargs):
        """Add zoom behaviour.

        Arguments:
            event (QWheelEvent): The PySide2 QWheelEvent.
        """
        # calculate zoom factor
        if event.angleDelta().y() > 0:
            # zoom in
            zoom_factor = self.zoom_factor
            self.zoom += self.zoom_step
        else:
            # zoom out
            zoom_factor = 1 / self.zoom_factor
            self.zoom -= self.zoom_step

        # clamp the zoom
        if self.zoom < self.zoom_range[0]:
            self.zoom = self.zoom_range[0]
        elif self.zoom > self.zoom_range[1]:
            self.zoom = self.zoom_range[1]
        else:
            # do scale the scene
            self.scale(zoom_factor, zoom_factor)
