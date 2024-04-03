"""Manage the session's related elements."""

from lbx_pipeline.internal import logging, manager

logger = logging.SessionLogger()

MANAGER = None


def start(software):
    """Start the pipeline withoud any UI.

    Arguments:
        software (str): The software we're executing the pipeline in.
    """
    manager.Manager(software=software)


def get_manager():
    """Get the pipeline manager.

    Returns:
        Manager: The pipeline manager.
    """
    if MANAGER:
        return MANAGER
    logger.error("You first need to start the pipeline")
