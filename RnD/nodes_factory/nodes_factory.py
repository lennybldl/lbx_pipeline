import random


class Builder(object):
    """Node creator."""

    def create_node(self, name, node_type):
        if node_type == "Mult":
            _class = Mult
        elif node_type == "ExtendedMult":
            _class = ExtendedMult

        inputs = _class.input_attributes
        outputs = _class.output_attributes
        compute = _class.compute
        methods = dict()
        for method_name in dir(_class):
            if not method_name.startswith("_"):
                method = getattr(_class, method_name)
                if callable(method) and method is not compute:
                    methods[method_name] = method

        return Node(name, inputs, outputs, compute, methods)


class Node(object):
    """Manage a node."""

    input_attributes = None
    output_attributes = None

    def __init__(self, name, inputs, outputs, compute, methods):
        self.name = name
        self.input_attributes = {o: random.randint(1, 10) for o in inputs}
        self.output_attributes = {o: None for o in outputs}
        self.compute = compute
        self.methods = methods

    def eval(self):
        """Evaluate the node."""
        print(self.compute)
        outputs = self.compute(self, self.input_attributes)
        for attribute, value in outputs.items():
            self.output_attributes[attribute] = value

    def execute(self, name):
        method = self.methods.get(name)
        if method:
            method(self, self.input_attributes)


class CustomNode(object):
    """Create a class that allows to setup custom nodes."""

    def compute(self, inputs):
        return dict()


class Mult(CustomNode):
    """Create a custom mult node."""

    input_attributes = ["inputA", "inputB"]
    output_attributes = ["output"]

    def compute(self, inputs):
        return {"output": inputs.get("inputA") * inputs.get("inputB")}

    def public_method(self, inputs):
        print("public", inputs)


class ExtendedMult(Mult):
    """Create a subnode from the mult node."""

    def compute(self, inputs):
        output = Mult.compute(self, inputs)
        print("extented")
        output["output"] = str(output["output"])
        return output


if __name__ == "__main__":
    builder = Builder()
    node = builder.create_node("test", "ExtendedMult")

    print(node.input_attributes)
    print(node.output_attributes)
    node.eval()
    print(node.output_attributes)
    print(node.methods)
    node.execute("public_method")
