from pathlib import Path
import argparse
import sys

from .packer import pack
from .unpacker import unpack as unpack_archive
from .config import load_config


def cli():
    parser = argparse.ArgumentParser(
        description="tpack: pack directories/files into a text archive or unpack them."
    )

    parser.add_argument(
        "archive",
        nargs="?",
        default=None,
        metavar="ARCHIVE",
        help="Archive file (required in unpack mode)."
    )

    parser.add_argument(
        "-d", "--dir",
        action="append",
        default=[],
        dest="dirs",
        help="Source directory to pack (can be specified multiple times)."
    )

    parser.add_argument(
        "-f", "--files",
        action="append",
        default=[],
        dest="files",
        help="Specific file to pack (can be specified multiple times)."
    )

    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output archive file (pack) or destination directory (unpack)."
    )

    parser.add_argument(
        "-u", "--unpack",
        action="store_true",
        help="Unpack mode: restore files from a packed text archive."
    )

    parser.add_argument(
        "-c", "--config",
        default=None,
        help="Path to config YAML file."
    )

    parser.add_argument(
        "--follow-symlinks",
        action="store_true",
        help="Follow symlinks that resolve outside the source directory."
    )

    args = parser.parse_args()
    cfg = load_config(args.config)

    if args.unpack:
        if args.archive is None:
            parser.error("unpack mode requires an archive file as argument.")
        if args.output is None:
            parser.error("unpack mode requires --output (-o) destination directory.")
        if args.dirs:
            parser.error("unpack mode does not accept --dir (-d).")
        if args.files:
            parser.error("unpack mode does not accept --files (-f).")

        unpack_archive(Path(args.archive), Path(args.output), cfg)
        print(f"Unpacked into: {args.output}")
    else:
        if args.archive is not None:
            parser.error(
                "unexpected argument. To pack a directory, use -d <dir>. "
                "To unpack, use -u ARCHIVE -o DEST."
            )
        if args.output is None:
            parser.error("pack mode requires --output (-o) option.")
        if not args.dirs and not args.files:
            parser.error(
                "specify at least one source via --dir (-d) or --files (-f)."
            )

        pack(
            dirs=[Path(d) for d in args.dirs],
            files=[Path(f) for f in args.files],
            output_path=Path(args.output),
            config=cfg,
            follow_symlinks=args.follow_symlinks,
        )
        print(f"Packed into: {args.output}")


if __name__ == "__main__":
    cli()
