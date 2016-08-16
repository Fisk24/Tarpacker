#! /usr/bin/python3

from lib.cli   import *

from lib               import logger
from lib.mode.status   import Status
from lib.mode.manifest import Manifest
from lib.mode.pack     import Pack
from lib.mode.unpack   import Unpack
from lib.mode.config   import Config
from lib.mode.setup    import Setup

class TarPacker():
    def __init__(self):
        try:
            # Try first time setup
            setup = Setup()
            # determine the mode and run proper function
            if args.subparser_name == "status":
                Status(args, setup)
            elif args.subparser_name == "manifest":
                Manifest(args, setup)
            elif args.subparser_name == "pack":
                Pack(args, setup)
            elif args.subparser_name == "unpack":
                Unpack(args, setup)
            elif args.subparser_name == "config":
                Config(args, setup)
            elif args.version: 
                self.getVersionInfo()
            else:
                print("\nPlease pick a mode. Use --help for assistance\n")
        except:
            logger.report()

    def getVersionInfo(self):
        import sys, subprocess
        output = subprocess.check_output(["git","rev-list","HEAD","--count"]).decode("utf-8")
        gitcount = output.replace("\n", "")
        print("Tarpacker Version: git [{ver}]".format(ver=gitcount))
        print("Running on Python: {ver}".format(ver=sys.version))


if __name__ == "__main__":
    main = TarPacker()
