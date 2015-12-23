#! /usr/bin/python3

import os
from lib.cli   import *

from lib.mode.status   import Status
from lib.mode.manifest import Manifest
from lib.mode.pack     import Pack
from lib.mode.unpack   import Unpack
from lib.mode.config   import Config

class TarPacker():
    def __init__(self):
        #determine the mode and run proper function
        if args.subparser_name == "status":
            Status(args)
        elif args.subparser_name == "manifest":
            Manifest(args)
        elif args.subparser_name == "pack":
            Pack(args)
        elif args.subparser_name == "unpack":
            Unpack(args)
        elif args.subparser_name == "config":
            Config(args)

if __name__ == "__main__":
    main = TarPacker()
