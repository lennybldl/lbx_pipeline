"""Manage the nodes."""

from lbx_pipeline.api.abstract import features


class Node(features.NodalFeature):
    """Manage the base class for nodes."""

    category = "nodes"
