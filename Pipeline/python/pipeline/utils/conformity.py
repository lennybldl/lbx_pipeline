"""Check conformity on things."""

from python_core.types import strings


def conform_asset_name(asset_name):
    """Check the asset name conformity to be sur that it is well named.

    :param asset_name: The name of the asset
    :type asset_name: str

    :return: The conformed asset name
    :rtype: str
    """

    asset_name = strings.replace_specials(asset_name, "_")
    asset_name = asset_name.split("_")

    for index, word in enumerate(asset_name):
        if index == 0:
            asset_name[0] = strings.lower_at(word)
        else:
            asset_name[index] = strings.upper_at(word)

    return "".join(asset_name)
