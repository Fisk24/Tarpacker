import argparse

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

#parser.add_argument("status", action="store_true")

status = subparser.add_parser("status")

#manifest = parser.add_group()
manifest = subparser.add_parser("manifest")
#manifest.add_argument("--Manifest", "-M", action="store_true", help="Set Tarpacker to manifest mode to add or remove files from the manifest, aswell as change the manifest file location.")
manifest.add_argument("--add", "-a", action="store", help="In manifest mode, add a file to the manifest. Format is {file:group}. Group must be preexisting, use -f to auto-add an unknown group or -g to add the group before hand.")
manifest.add_argument("--force", "-f", action="store_true", help="In manifest mode, forcefuly add a file to an unknown group by first creating the unknown group and then adding the file to it")
manifest.add_argument("--add-group", "-g", action="store", help="In manifest mode, add a group to the manifest")
manifest.add_argument("--set", "-s", action="store", help="In manifest mode, set the manifest file location, the file is created if it does not exist.\n All manifest files are initiated with the group \"Misc\" all ready added.")

config = subparser.add_parser("config")
config.add_argument("--place-holder", action="store_true", help="does nothing")

args = parser.parse_args()
