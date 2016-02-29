import os

class Manifest():
    def __init__(self, args, setup):
        os.system("vim {0}".format(setup.manifestdir))
