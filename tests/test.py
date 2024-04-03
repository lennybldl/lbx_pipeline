import sys
import json

from lbx_python_core import items

sys.path.insert(0, items.File(__file__).get_upstream(2) + "/src")

from lbx_pipeline import commands  # noqa E402

commands.start("windows")
commands.load(items.File(__file__).directory)

from lbx_pipeline.api import nodes

node = nodes.Node("toto")
attribute = node.add_attribute("int", value=5, default=8)
attribute = node.add_attribute("str", min=2, max=10)
attribute = node.add_attribute("float", min=2, max=10)
attribute = node.add_attribute("bool", min=2, max=10)


data = node.serialize()
print(json.dumps(data, indent=4))
