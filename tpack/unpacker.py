"""
Unpack text archives created by tpack.
"""

import os
import re
from pathlib import Path

HEADER_RE = re.compile(r"^=+\s+(.+)\s+=+$")


def _check_path_within_dest(target_resolved, dest_resolved):
    target_norm = os.path.normcase(str(target_resolved))
    dest_norm = os.path.normcase(str(dest_resolved))
    dest_parent = dest_norm.rstrip(os.sep) + os.sep
    if target_norm != dest_norm and not target_norm.startswith(dest_parent):
        raise ValueError(
            f"Refusing to write outside destination directory: "
            f"path resolves to '{target_resolved}'"
        )


def unpack(input_file, dest_dir, config):
    """
    Unpack a text archive created by tpack.
    """

    input_file = Path(input_file)
    dest_dir = Path(dest_dir)
    encoding = config.get("encoding", "utf-8")
    dest_resolved = dest_dir.resolve()

    current_path = None

    with open(input_file, "r", encoding=encoding) as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")

            if re.match(r"^=+$", line):
                continue

            if line.startswith("== ") and line.endswith(" =="):
                m = HEADER_RE.match(line)
                if not m:
                    continue

                rel_path = m.group(1).strip()
                target = dest_dir.joinpath(rel_path)
                _check_path_within_dest(target.resolve(), dest_resolved)

                current_path = target
                current_path.parent.mkdir(parents=True, exist_ok=True)
                continue

            if current_path:
                with open(current_path, "a", encoding=encoding, newline="\n") as out:
                    out.write(raw_line)
