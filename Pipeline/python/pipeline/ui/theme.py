"""Manage the default style sheets of the application."""

import json
import os

from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt

from python_core.types import colors
from python_core.pyside2 import common

from pipeline.utils import database


DATABASE = database.Database()

# define primary and background color
PRIMARY = "#19C5F7"
BACKGROUND = "#343445"

# get the color palette
palette = colors.color_palette(PRIMARY)
palette.update(colors.get_shades(BACKGROUND, name="background"))

# get the background shades
BACKGROUND_0 = palette["background_0"]
BACKGROUND_1 = palette["background_1"]

# get text color
TEXT = "white"
INFORMATIVE_TEXT = "#DDDDDD"
TOOLTIPS_TEXT = "black"
TOOLTIPS_BG = BACKGROUND_1

# set the highlighted color
HIGHLIGHT = palette["background_5"] + colors.hexa_from_rgba(127).replace("#", "")


def default_stylesheets():
    """Set the styleSheets to default by setting the values in a json file."""

    stylesheets = {}

    with open(os.path.join(DATABASE.data_path, "styleSheets.json"), "w") as file:
        file.write(json.dumps(stylesheets, indent=4))


def theme(app):
    """Set the default app color theme.

    :param app: The application to set the theme to
    :type app: QApplication
    """
    # set the app style
    app.setStyle("Fusion")

    # set the app colors
    palette = QPalette()

    # set the window background color
    palette.setColor(QPalette.Window, common.qcolor_from_arg(BACKGROUND))
    # set the text color in the window
    palette.setColor(QPalette.WindowText, common.qcolor_from_arg(TEXT))
    # set the color of the background in the widgets
    # (ex : QLineEdits/QTreeWidgets/QListWidgets)
    palette.setColor(QPalette.Base, common.qcolor_from_arg(BACKGROUND_1))
    # DONT KNOW HOW IT WORKS
    palette.setColor(QPalette.AlternateBase, common.qcolor_from_arg(BACKGROUND))
    # the tooltips background
    palette.setColor(QPalette.ToolTipBase, common.qcolor_from_arg(TOOLTIPS_BG))
    # the tooltips text color
    palette.setColor(QPalette.ToolTipText, common.qcolor_from_arg(TOOLTIPS_TEXT))
    # The text color
    palette.setColor(QPalette.Text, common.qcolor_from_arg(TEXT))
    # The tab widgets for exemple
    palette.setColor(QPalette.Button, common.qcolor_from_arg(BACKGROUND))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # color when item is selected
    palette.setColor(QPalette.Highlight, common.qcolor_from_arg(HIGHLIGHT))
    # the color of the selected text
    palette.setColor(QPalette.HighlightedText, common.qcolor_from_arg(TEXT))

    # the colors for active and disabled widgets
    palette.setColor(
        QPalette.Active, QPalette.Button, common.qcolor_from_arg(BACKGROUND)
    )
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))

    # set the palette to the app
    app.setPalette(palette)
