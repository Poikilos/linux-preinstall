#!/usr/bin/env python3
from __future__ import print_function
import os
import sys
from zipfile import ZipFile, BadZipFile

"""
Extract all files from a series of archives to the same directory,
MERGING and OVERWRITING anywhere the files from previous archives have
the same relative paths and names.

unsplitarc.py <source> <destination>

source                This should be a directory containing zip files.
destination         This can be any directory, but must exist already.
"""

def echo0(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def usage():
    print("Usage:")
    print(__doc__)


def unsplit_arc(src, dst):
    for sub in os.listdir(src):
        sub_path = os.path.join(src, sub)
        try:
            with ZipFile(sub_path, 'r') as thisZip:
                thisZip.extractall(dst)
        except BadZipFile:
            echo0("* ERROR: {} is a BadZipFile".format(sub_path))


def main():
    if len(sys.argv) < 2:
        usage()
        echo0("You must specify a source and target directory.")
        return 1
    if len(sys.argv) < 3:
        usage()
        echo0("You must also specify a target directory.")
        return 1
    unsplit_arc(sys.argv[1], sys.argv[2])
    return 0

if __name__ == "__main__":
    sys.exit(main())
