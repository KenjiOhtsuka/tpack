"""
Unpack text archives created by tpack.
"""

import os
import re
from pathlib import Path

METADATA_RE = re.compile(
    r"^# tpack-archive header\.prefix: (\S+) header\.border_char: (\S+)$"
)


def _parse_metadata(line):
    m = METADATA_RE.match(line)
    if m:
        return m.group(1), m.group(2)
    return None, None


def _header_rel_path(line, prefix):
    if not prefix:
        return None
    start = prefix + " "
    end = " " + prefix
    if not line.startswith(start) or not line.endswith(end):
        return None
    rel = line[len(prefix) + 1 : -(len(prefix) + 1)]
    return rel or None


def _is_border(line, prefix, border_char):
    if not prefix or not border_char:
        return False
    if len(line) <= len(prefix) * 2:
        return False
    if not (line.startswith(prefix) and line.endswith(prefix)):
        return False
    inner = line[len(prefix) : -len(prefix)]
    if not inner or len(inner) % len(border_char) != 0:
        return False
    return inner == border_char * (len(inner) // len(border_char))


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

    header_cfg = config.get("header", {})
    prefix = header_cfg.get("prefix", "==")
    border_char = header_cfg.get("border_char", "=")

    current_path = None
    initialized_paths = set()

    with open(input_file, "r", encoding=encoding) as f:
        first_line = f.readline()
        meta_prefix, meta_border = _parse_metadata(first_line)
        if meta_prefix is not None:
            prefix = meta_prefix
            border_char = meta_border
        else:
            f.seek(0)

        for raw_line in f:
            line = raw_line.rstrip("\n")

            if _is_border(line, prefix, border_char):
                continue

            rel_path = _header_rel_path(line, prefix)
            if rel_path:
                target = dest_dir.joinpath(rel_path)
                _check_path_within_dest(target.resolve(), dest_resolved)

                current_path = target
                initialized_paths.discard(current_path)
                current_path.parent.mkdir(parents=True, exist_ok=True)
                continue

            if current_path:
                mode = "a" if current_path in initialized_paths else "w"
                initialized_paths.add(current_path)
                with open(current_path, mode, encoding=encoding, newline="\n") as out:
                    out.write(raw_line)
