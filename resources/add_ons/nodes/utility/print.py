"""Create a custom print node."""

from lbx_pipeline import open_api


class Print(open_api.BaseNode):
    """Manage the print node that prints data."""

    inputs = [open_api.node_input(name="input", data_type="Str")]

    def compute(self, inputs):
        """Perform some action when the node gets evaluated.

        Arguments:
            inputs (dict): A dictionary of input attributes names and their value.

        Returns:
            dict: A dictionary containing the value for each output attribute.
        """
        outputs = dict()
        print(inputs.get("input"))
        return outputs
