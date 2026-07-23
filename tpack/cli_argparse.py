"""
CLI interface for tpack: pack directories or unpack archives.
"""

from pathlib import Path
import argparse

from .packer import pack
from .unpacker import unpack as unpack_archive
from .config import load_config


def cli():
    parser = argparse.ArgumentParser(
        description="tpack: pack directories into a text archive or unpack them."
    )

    parser.add_argument(
        "path",
        help="Source directory (pack) or archive file (unpack)."
    )

    parser.add_argument(
        "-u", "--unpack",
        action="store_true",
        help="Unpack mode: restore files from a packed text archive."
    )

    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path for packing."
    )

    parser.add_argument(
        "-d", "--dest",
        default=None,
        help="Destination directory for unpacking."
    )

    parser.add_argument(
        "-c", "--config",
        default=None,
        help="Path to config YAML file."
    )

    args = parser.parse_args()

    cfg = load_config(args.config)

    if args.unpack:
        if args.dest is None:
            parser.error("Unpack mode requires --dest option.")
        unpack_archive(Path(args.path), Path(args.dest), cfg)
        print(f"Unpacked into: {args.dest}")
    else:
        if args.output is None:
            parser.error("Pack mode requires --output option.")
        pack(Path(args.path), Path(args.output), cfg)
        print(f"Packed into: {args.output}")


if __name__ == "__main__":
    cli()
