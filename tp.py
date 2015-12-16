#! /usr/bin/python3

import os, tarfile, logging
from lib.cli import *
from lib.mplib import *

class TarPacker():
    def __init__(self):
        self.mparser = ManifestParser("manifest.mf")
        self.mparser.parseManifest()
        print(self.mparser)

    def preProcess(self):
        pass

    def createBackup(self):
        pass

    def restoreBackup(self):
        pass

if __name__ == "__main__":
    main = TarPacker()
