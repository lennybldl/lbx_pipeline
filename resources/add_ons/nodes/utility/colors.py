"""Create a custom color maker node."""

from lbx_python import colors

from lbx_pipeline import open_api


class RGBAToHex(open_api.BaseNode):
    """Convert a RGBA color to an hexadecimal color code."""

    inputs = [
        open_api.node_input(name="R", data_type="Int", default=255, min=0, max=255),
        open_api.node_input(name="G", data_type="Int", default=255, min=0, max=255),
        open_api.node_input(name="B", data_type="Int", default=255, min=0, max=255),
        open_api.node_input(name="A", data_type="Int", default=255, min=0, max=255),
    ]
    outputs = [
        open_api.node_output(name="output", data_type="Str"),
    ]

    def compute(self, inputs):
        """Perform some action when the node gets evaluated.

        Arguments:
            inputs (dict): A dictionary of input attributes names and their value.

        Returns:
            dict: A dictionary containing the value for each output attribute.
        """
        # convert the color from the input RGBA code
        return {
            "output": colors.Color([inputs.get(c) for c in "RGBA"]).get_hex(
                complete=False
            )
        }


class HexToRGBA(open_api.BaseNode):
    """Convert a RGBA color to an hexadecimal color code."""

    inputs = [
        open_api.node_input(name="input", data_type="Str"),
    ]
    outputs = [
        open_api.node_output(name="R", data_type="Int"),
        open_api.node_output(name="G", data_type="Int"),
        open_api.node_output(name="B", data_type="Int"),
        open_api.node_output(name="A", data_type="Int"),
    ]

    def compute(self, inputs):
        """Perform some action when the node gets evaluated.

        Arguments:
            inputs (dict): A dictionary of input attributes names and their value.

        Returns:
            dict: A dictionary containing the value for each output attribute.
        """
        # convert the color from input to RGBA code
        red, green, blue, alpha = colors.Color(inputs.get("input")).rgba
        return {
            "R": red,
            "G": green,
            "B": blue,
            "A": alpha,
        }
