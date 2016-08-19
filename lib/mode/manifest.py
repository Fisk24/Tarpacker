"""
TODO:
    everything

    in mplib which you probably used in this, make it so that comments can be written using #
    # Example comment, this is ignored by the parser but persists when manifests writes in additions
"""

import os
from lib.config import Config
from lib.mplib  import ManifestParser

class Manifest():
    def __init__(self, args, setup):
        # Create config object
        self.conf  = Config(setup.configdir+"/settings.json")

        # flags...
        self.args  = args

        # Create ManifestParser
        self.manifest = self.argsInFile()
        self.manifest.parseManifest()

        # Directories
        self.setup = setup

        print(self.args)

        #self.manifest.data["misc"].append("/home/fisk/.config/tarpacker/settings.json")
        #self.manifest.generateManifest()
        
        self.argsEdit()
        self.argsStatus()
        self.addManifestEntry()

    def addManifestEntry(self):
        pass

    def argsStatus(self):
        if self.args.status:
            self.manifest.info()

    def argsInFile(self):
        if self.args.in_file:
            return ManifestParser(self.args.in_file)
        else:
            return ManifestParser(self.conf.data["manifest"]["file"])

    def argsEdit(self):
        if self.args.edit:
            self.manualEdit()

    def manualEdit(self):
        os.system("vim {0}".format(self.setup.manifestdir))
