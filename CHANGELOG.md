# Change Log
All notable changes to this project will be documented in this file.

## [UNRELEASED] -

### Changed
- Tp can now keep track of when it was last used to create a backup.
- Tp can now auto generate a config directory, a default manifest file, and a temp directory if such files do not already exist
- Setup.sh was added to handle installing tarpacker on new systems! 

## [a0.0.2] - 2016-02-25  

### Added
- Packing mode is ready for use!
- Infrastructure for mode classes, every mode has its own module
- Config class in "lib/config.py" now handles all user setting data

## [a0.0.1] - 2015-12-20

### Changed
- Removed --set command line parameter under manifest mode.
This functionality should be handled by config mode.

- Added command line parameters for all modes "pack, unpack, config, manifest"

