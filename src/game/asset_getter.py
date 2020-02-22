import os
asset_folder = os.path.join(os.curdir, os.path.pardir, os.pardir, "assets")

def get_asset(name):
    return os.path.join(asset_folder, name)