"""
tpack
========

A lightweight text-based archiver for packing directories and files into a
single text archive and unpacking them.

This package provides:
- pack: pack directories/files into a text archive
- unpack: unpack a text archive into a directory

CLI usage:
    $ tpack -d <dir> -o output.txt          # pack a directory
    $ tpack -f <file> ... -o output.txt     # pack specific files
    $ tpack archive.txt -u -o extracted_dir # unpack
"""

from .packer import pack
from .unpacker import unpack

__all__ = [
    "pack",
    "unpack",
]

__version__ = "1.0.2"
