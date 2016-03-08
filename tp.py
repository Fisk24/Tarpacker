#! /usr/bin/python3

import os
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
            else:
                print("\nPlease pick a mode. Use --help for assistance\n")
        except:
            logger.report()

if __name__ == "__main__":
    main = TarPacker()
