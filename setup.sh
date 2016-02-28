#! /bin/bash

echo Creating symlinks for TarPacker...
cwd = pwd
ln -s $cwd/tp.py /usr/bin/tp
