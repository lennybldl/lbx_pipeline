"""Manage the constant variables of the application."""

from lbx_pipeline.api import attributes, parameters

ATTRIBUTE_TYPES = {
    "bool": attributes.BoolAttribute,
    "int": attributes.IntAttribute,
    "float": attributes.FloatAttribute,
    "str": attributes.StrAttribute,
}

PARAMETERS_TYPES = {
    "bool": parameters.BoolParameter,
    "int": parameters.IntParameter,
    "float": parameters.FloatParameter,
    "str": parameters.StrParameter,
}
