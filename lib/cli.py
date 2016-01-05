import argparse

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="subparser_name")

#parser.add_argument("status", action="store_true")

status = subparser.add_parser("status")

manifest = subparser.add_parser("manifest")
manifest.add_argument("--add", "-A", action="store", help="Add a file to the manifest. Format is {file:group}. Group must be preexisting, use -f to auto-add an unknown group or -g to add the group before hand.")
manifest.add_argument("--force", "-f", action="store_true", help="Forcefuly add a file to an unknown group by first creating the unknown group and then adding the file to it")
manifest.add_argument("--add-group", "-g", action="store", help="Add a group to the manifest")
manifest.add_argument("--remove", "-R", action="store", help="Remove a file from the mainfest.")
manifest.add_argument("--remove-group", "-rg", action="store", help="Remove a group from the manifest. In addition, all entries for the group are deleted. Confermation is required by the user.")
manifest.add_argument("--status", action="store_true", help="Show information about the manifest")
#manifest.add_argument("--set", "-s", action="store", help="In manifest mode, set the manifest file location, the file is created if it does not exist.\n All manifest files are initiated with the group \"Misc\" all ready added.")

packing = subparser.add_parser("pack")
packing.add_argument("--man", "-m", action="store", help="Specifies manifest file to be loaded. Overrides value in the config file.")
packing.add_argument("--location", "-l", action="store", help="Specifies directory to place archive files. Overrides value in the config file.")
packing.add_argument("--section", action="store", help="List specific sections from the manifest to backup. Uses python list notation must be in quotes: ['section1','section2','section3']")
packing.add_argument("--off-site", "-s", action="store", help="####NOT IMPLEMENTED#### Specify whether of not to send archive files to a server through ssh protocol. Overrides value in config file.")

unpacking = subparser.add_parser("unpack")
unpacking.add_argument("--in-file", "-if", action="store", help="Specifies the archive file to be unpacked. Optionally, this value can be an archive manifest, which containes a list of archive files to be unpacked. If unpacking from a remote location eg: a server, use --off-site instead.")
unpacking.add_argument("--location-override", "-lo", action="store", help="Not recommended for batch extractions! Specifies a root directory to unpack all files and subdirectories into. This value will override the archive's root extraction location")
unpacking.add_argument("--off-site", "-s", action="store", help="####NOT IMPLEMENTED#### Specifies a server to download archive files from. This must be a full file path. Eg: user@server.com/path/to/archive.tar.gz")

config = subparser.add_parser("config")
config.add_argument("key", action="store", help="Configuration key to target. Syntax is {key=value} of {key}. If no value is passed then the targeted key is printed instead of edited.")
config.add_argument("--list", "-l", action="store_true", help="List every available key and its value")

args = parser.parse_args()
#print(args)
