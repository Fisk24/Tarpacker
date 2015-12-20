import argparse

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

#parser.add_argument("status", action="store_true")

status = subparser.add_parser("status")

manifest = subparser.add_parser("manifest")
manifest.add_argument("--add", "-a", action="store", help="In manifest mode, add a file to the manifest. Format is {file:group}. Group must be preexisting, use -f to auto-add an unknown group or -g to add the group before hand.")
manifest.add_argument("--force", "-f", action="store_true", help="In manifest mode, forcefuly add a file to an unknown group by first creating the unknown group and then adding the file to it")
manifest.add_argument("--add-group", "-g", action="store", help="In manifest mode, add a group to the manifest")
manifest.add_argument("--set", "-s", action="store", help="In manifest mode, set the manifest file location, the file is created if it does not exist.\n All manifest files are initiated with the group \"Misc\" all ready added.")

packing = subparser.add_parser("pack")
packing.add_argument("--man", "-m", action="store", help="Specifies manifest file to be loaded. Overrides value in the config file.")
packing.add_argument("--location", "-l", action="store", help="Specifies directory to place archive files. Overrides value in the config file.")
packing.add_argument("--off-site", "-s", action="store", help="####NOT IMPLEMENTED#### Specify whether of not to send archive files to a server through ssh protocol. Overrides value in config file.")

config = subparser.add_parser("config")
config.add_argument("--place-holder", action="store_true", help="does nothing")

args = parser.parse_args()
