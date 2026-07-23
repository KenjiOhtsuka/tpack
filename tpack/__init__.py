"""
tpack
========

A lightweight text-based archiver for packing directories into a single file
and unpacking them in another environment.

This package provides:
- pack: pack a directory into a text archive
- unpack: unpack a text archive into a directory

CLI usage:
    $ tpack <source_dir> -o output.txt
    $ tpack -u output.txt -d extracted_dir
"""

from .packer import pack
from .unpacker import unpack

__all__ = [
    "pack",
    "unpack",
]

__version__ = "0.1.0"
