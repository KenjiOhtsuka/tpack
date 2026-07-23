"""
CLI interface for tpack: pack directories or unpack archives.
"""

from pathlib import Path  # standard library first
import click              # third-party

from .packer import pack
from .unpacker import unpack as unpack_archive  # avoid name shadowing
from .config import load_config


@click.command()
@click.argument("path")
@click.option(
    "-u", "--unpack",
    is_flag=True,
    help="Unpack mode: restore files from a packed text archive."
)
@click.option(
    "-o", "--output",
    default=None,
    help="Output file path for packing."
)
@click.option(
    "-d", "--dest",
    default=None,
    help="Destination directory for unpacking."
)
@click.option(
    "-c", "--config",
    default=None,
    help="Path to config YAML file."
)
def cli(path, unpack, output, dest, config):
    """
    tpack: pack directories into a text archive or unpack them.
    """

    cfg = load_config(config)

    if unpack:
        if dest is None:
            raise click.UsageError("Unpack mode requires --dest option.")
        unpack_archive(Path(path), Path(dest), cfg)
        click.echo(f"Unpacked into: {dest}")
    else:
        if output is None:
            raise click.UsageError("Pack mode requires --output option.")
        pack(Path(path), Path(output), cfg)
        click.echo(f"Packed into: {output}")

if __name__ == "__main__":
    cli()