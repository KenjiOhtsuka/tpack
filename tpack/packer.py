from pathlib import Path
import sys


def _make_header(rel_path, prefix, border_char):
    middle = f"{prefix} {rel_path} {prefix}"
    border_len = len(middle) - len(prefix) * 2
    border = border_char * border_len
    return (
        f"{prefix}{border}{prefix}\n"
        f"{middle}\n"
        f"{prefix}{border}{prefix}\n"
    )


def _is_under(child, parent):
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _find_root(resolved_path, roots):
    best = None
    max_len = -1
    for root_resolved, dir_prefix in roots:
        if _is_under(resolved_path, root_resolved):
            if len(str(root_resolved)) > max_len:
                best = (root_resolved, dir_prefix)
                max_len = len(str(root_resolved))
    return best


def pack(dirs, output_path, config, files=None, follow_symlinks=False):
    output_path = Path(output_path).resolve()
    exclude_patterns = config.get("exclude", []).copy()
    remove_blank_lines = config.get("remove_blank_lines", False)
    encoding = config.get("encoding", "utf-8")
    header_cfg = config.get("header", {})
    prefix = header_cfg.get("prefix", "==")
    border_char = header_cfg.get("border_char", "=")

    dirs = [Path(d) for d in dirs] if dirs else []
    files = [Path(f) for f in files] if files else []

    if not dirs and not files:
        dirs = [Path(".")]

    roots = []
    for d in dirs:
        resolved = d.resolve()
        if not resolved.is_dir():
            raise ValueError(f"Directory does not exist: {resolved}")
        roots.append((resolved, resolved.name))

    entries = []
    violations = []
    warnings_list = []
    seen = set()

    for root_resolved, dir_prefix in roots:
        for file_path in root_resolved.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.resolve() == output_path:
                continue

            if any(file_path.match(p) for p in exclude_patterns):
                continue

            is_sym = file_path.is_symlink()
            resolved = file_path.resolve()

            if is_sym and not _is_under(resolved, root_resolved):
                if not follow_symlinks:
                    warnings_list.append(
                        f"Symlink points outside source dir, skipping: {file_path}"
                    )
                    continue

            if resolved in seen:
                continue
            seen.add(resolved)

            archive_rel = resolved.relative_to(root_resolved)
            archive_path = Path(dir_prefix) / archive_rel
            entries.append((resolved, archive_path))

    if files:
        cwd = Path.cwd().resolve()
        for f in files:
            resolved = f.resolve()

            if not resolved.exists():
                violations.append(f"File does not exist: {f}")
                continue

            if not resolved.is_file():
                violations.append(f"Not a file: {f}")
                continue

            is_sym = f.is_symlink()
            matched = _find_root(resolved, roots) if roots else None

            if matched:
                root_resolved, dir_prefix = matched
                if is_sym and not _is_under(resolved, root_resolved):
                    if not follow_symlinks:
                        warnings_list.append(
                            f"Symlink points outside source dir, skipping: {f}"
                        )
                        continue
                if resolved in seen:
                    continue
                seen.add(resolved)

                archive_rel = resolved.relative_to(root_resolved)
                archive_path = Path(dir_prefix) / archive_rel
                entries.append((resolved, archive_path))
            elif roots:
                if is_sym and not follow_symlinks:
                    warnings_list.append(
                        f"Symlink points outside source dir, skipping: {f}"
                    )
                    continue
                violations.append(
                    f"File is outside all specified directories: {f}"
                )
            else:
                if _is_under(resolved, cwd):
                    if resolved in seen:
                        continue
                    seen.add(resolved)
                    archive_path = resolved.relative_to(cwd)
                    entries.append((resolved, archive_path))
                elif is_sym:
                    if follow_symlinks:
                        if resolved in seen:
                            continue
                        seen.add(resolved)
                        archive_path = Path(f.name)
                        entries.append((resolved, archive_path))
                    else:
                        warnings_list.append(
                            f"Symlink points outside working directory, skipping: {f}"
                        )
                        continue
                else:
                    violations.append(
                        f"File is outside the working directory: {f}"
                    )

    if violations:
        raise ValueError("\n".join(violations))

    for w in warnings_list:
        print(f"warning: {w}", file=sys.stderr)

    entries.sort(key=lambda e: e[1])

    with open(output_path, "w", encoding=encoding) as out:
        for resolved_path, archive_path in entries:
            out.write(_make_header(archive_path.as_posix(), prefix, border_char))
            try:
                text = resolved_path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
            if remove_blank_lines:
                text = "\n".join(
                    line for line in text.splitlines() if line.strip()
                )
            out.write(text.rstrip("\n") + "\n")
