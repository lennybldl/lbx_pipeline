"""Setup the package."""

from lbx_python_core import system


NAME = "lbx_pipeline"
VERSION = "2.0.0"
PATH = system.File(__file__).get_upstream(3)


def doc():
    """Open the autodoc documentation in a browser."""

    html = system.File(PATH, "docs", "build", "index.html")
    if html.exists():
        html.open()
