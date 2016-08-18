"""
TODO:
    everything

    in mplib which you probably used in this, make it so that comments can be written using #
    # Example comment, this is ignored by the parser but persists when manifests writes in additions
"""

import os

class Manifest():
    def __init__(self, args, setup):
        os.system("vim {0}".format(setup.manifestdir))
