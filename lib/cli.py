import argparse

# parse system arguments to decide best course of action to take
parser = argparse.ArgumentParser()

### ARGUMENTS ###
# Add or remove commandline arguments here
parser.add_argument("-m", "--manifest", help="Specify a diffrent manifest file fo read from", action="store")

### END ARGUMENTS ###
args = parser.parse_args()
