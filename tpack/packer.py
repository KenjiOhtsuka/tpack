"""
Pack directories into a single text archive.
"""

from pathlib import Path


def _make_header(rel_path, prefix, border_char):
    # 中央行を先に作る
    middle = f"{prefix} {rel_path} {prefix}"

    # 中央行の長さに合わせて border を生成
    # border は prefix を除いた部分の長さにする
    border_len = len(middle) - len(prefix) * 2
    border = border_char * border_len
    return (
        f"{prefix}{border}{prefix}\n"
        f"{middle}\n"
        f"{prefix}{border}{prefix}\n"
    )


def pack(source_dir, output_path, config):
    """
    Pack a directory into a single text archive.
    """

    source_dir = Path(source_dir).resolve()
    output_path = Path(output_path).resolve()

    exclude_patterns = config.get("exclude", []).copy()
    remove_blank_lines = config.get("remove_blank_lines", False)
    encoding = config.get("encoding", "utf-8")

    # When the output_path is in source_dir,
    # add output_path to exclude_patterns.
    try:
        if output_path.is_relative_to(source_dir):
            exclude_patterns.append(output_path.name)
    except AttributeError:
        # Python < 3.9 fallback
        if str(output_path).startswith(str(source_dir)):
            exclude_patterns.append(output_path.name)

    header_cfg = config.get("header", {})
    prefix = header_cfg.get("prefix", "==")
    border_char = header_cfg.get("border_char", "=")

    with open(output_path, "w", encoding=encoding) as out:
        for file_path in source_dir.rglob("*"):
            if not file_path.is_file():
                continue

            if any(file_path.match(p) for p in exclude_patterns):
                continue

            rel_path = file_path.relative_to(source_dir)
            out.write(_make_header(rel_path, prefix, border_char))

            try:
                text = file_path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue

            if remove_blank_lines:
                text = "\n".join(
                    line for line in text.splitlines() if line.strip()
                )

            # 余計な改行を防ぐ
            out.write(text.rstrip("\n") + "\n")
