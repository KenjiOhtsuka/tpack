"""
Unpack text archives created by tpack.
"""

import re
from pathlib import Path

HEADER_RE = re.compile(r"^=+\s+(.+)\s+=+$")


def unpack(input_file, dest_dir, config):
    """
    Unpack a text archive created by tpack.
    """

    input_file = Path(input_file)
    dest_dir = Path(dest_dir)
    encoding = config.get("encoding", "utf-8")

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
                current_path = dest_dir.joinpath(rel_path)
                current_path.parent.mkdir(parents=True, exist_ok=True)
                continue

            if current_path:
                with open(current_path, "a", encoding=encoding) as out:
                    out.write(raw_line)
