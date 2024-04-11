"""Manage the macros."""

from lbx_pipeline.api.abstract import features, networks


class Macro(networks.Network, features.NodalFeature):
    """Manage the base class for macros."""

    category = "macros"
