import os
asset_folder = os.path.join(os.path.dirname(__file__), os.path.pardir, os.pardir, "assets")


def get_asset(name):
    return os.path.join(asset_folder, name)
