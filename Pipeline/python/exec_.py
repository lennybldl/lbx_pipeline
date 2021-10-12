"""Execute the script from the computer."""

from PySide2.QtWidgets import QApplication
from python_core.pyside2.config import config

from pipeline.ui import main, theme

config.set("debug.show_tooltip", False)

app = QApplication()
theme.theme(app)

window = main.Main()
window.window_size = (300, 600)
window.populate()
window.show()

app.exec_()
