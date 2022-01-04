"""Manage the layout / animation tools."""

import os

from pipeline.api.maya import maya_asset
from pipeline.api.maya.tools import rig
from pipeline.utils import database

ASSET = maya_asset.MayaAsset()
DATABASE = database.Database()

# layout methods


def import_reference(asset_name, times=1):
    """Import an asset as reference multiple times.

    :param asset_name: The name of the asset to import.
    :type asset_name: str
    :param times: The number of times to import the asset
    :type times: int
    """

    from maya import cmds

    # get the asset path from the asset name
    path = ASSET.get_path_from_name(asset_name)

    # get the file to import
    export = os.path.join(path, "rig", "export", asset_name + ".ma")
    if os.path.exists(export):
        path = export
        file_type = "mayaAscii"
    else:
        export = os.path.join(path, "modeling", "export", asset_name + ".fbx")
        if os.path.exists(export):
            path = export
            file_type = "FBX"
        else:
            raise ValueError(
                "# Pipeline : No maya export found for {} ".format(asset_name)
                + "in modeling or rig."
            )

    # import the asset as reference
    for _ in range(times):
        cmds.file(
            path,
            reference=True,
            type=file_type,
            ignoreVersion=True,
            groupLocator=True,
            mergeNamespacesOnClash=False,
            namespace=asset_name,
            options="v=0;",
        )

    print("# Pipeline : Imported {}x -> {}".format(times, path))


# animation methods


def get_exportable_animateds(pipe_nodes=None):
    """Get all the assets in the current animation scene with a rig pipe node group.

    :param pipe_nodes: A list of pipe nodes to get the joints to export from
    :type pipe_nodes: list, none
    """

    from maya import cmds

    # get pipenode from data
    app_data = DATABASE.app_data

    if pipe_nodes is None:
        pipe_node = app_data["tasks"]["rig"]["pipe_node"]
        pipe_nodes = cmds.ls("*:" + pipe_node)

    animateds = dict()
    for pipe_node in pipe_nodes:
        animateds.update(
            {
                pipe_node.rpartition(":")[0]: {
                    "asset_name": cmds.getAttr(pipe_node + ".AssetName"),
                },
            }
        )

    return animateds


def bake_animations(pipe_nodes=None):
    """Bake the animations of all the specifyied assets.

    :param pipe_nodes: A list of pipe_nodes to get the joints to export from.
        If none, bake all.
    :type pipe_nodes: list, none

    :return: The dictionnary of assets to export
    :rtype: dict
    """

    from maya import cmds

    # get assets to export
    animateds = get_exportable_animateds(pipe_nodes)

    # bake the animations
    cmds.select(clear=True)
    for asset_namespace in animateds.keys():
        # select all the joints to bake
        rig.select_joints_to_export(asset_namespace + ":RIG", add=True)

    # bake them
    cmds.bakeResults(
        cmds.ls(sl=True),
        simulation=True,
        time=(
            cmds.playbackOptions(q=True, min=True),
            cmds.playbackOptions(q=True, max=True),
        ),
        sampleBy=1,
    )

    return animateds
