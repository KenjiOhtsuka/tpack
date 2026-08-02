from pathlib import Path

from tpack.packer import pack
from tpack.unpacker import unpack


def test_pack_and_unpack(tmp_path):
    src = tmp_path / "src"
    src.mkdir()

    (src / "a.txt").write_text("hello\nworld\n")
    (src / "b.txt").write_text("line1\n\nline2\n")

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"
    restored = tmp_path / "restored"

    pack([src], packed, config)
    unpack(packed, restored, config)

    assert (restored / "src" / "a.txt").read_text() == "hello\nworld\n"
    assert (restored / "src" / "b.txt").read_text() == "line1\n\nline2\n"


def test_pack_with_files_and_dir(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "a.txt").write_text("hello")

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"
    restored = tmp_path / "restored"

    pack([sub], packed, config, files=[sub / "a.txt"])
    unpack(packed, restored, config)

    assert (restored / "sub" / "a.txt").read_text() == "hello\n"


def test_pack_with_files_default_root(tmp_path):
    (tmp_path / "root.txt").write_text("root")

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"
    restored = tmp_path / "restored"

    pack([tmp_path], packed, config, files=[tmp_path / "root.txt"])
    unpack(packed, restored, config)

    dir_name = tmp_path.name
    assert (restored / dir_name / "root.txt").read_text() == "root\n"


def test_exclude(tmp_path):
    src = tmp_path / "src"
    src.mkdir()

    (src / "keep.txt").write_text("keep")
    (src / "ignore.log").write_text("ignore")

    config = {
        "exclude": ["*.log"],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"
    restored = tmp_path / "restored"

    pack([src], packed, config)
    unpack(packed, restored, config)

    assert (restored / "src" / "keep.txt").exists()
    assert not (restored / "src" / "ignore.log").exists()


def test_remove_blank_lines(tmp_path):
    src = tmp_path / "src"
    src.mkdir()

    (src / "a.txt").write_text("line1\n\nline2\n")

    config = {
        "exclude": [],
        "remove_blank_lines": True,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"
    restored = tmp_path / "restored"

    pack([src], packed, config)
    unpack(packed, restored, config)

    assert (restored / "src" / "a.txt").read_text() == "line1\nline2\n"


def test_header_format(tmp_path):
    src = tmp_path / "src"
    src.mkdir()

    (src / "x.txt").write_text("data")

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "##", "border_char": "-"},
    }

    packed = tmp_path / "archive.txt"
    pack([src], packed, config)

    text = packed.read_text()

    assert "##-----------##" in text
    assert "## src/x.txt ##" in text


def test_pack_multiple_dirs(tmp_path):
    src1 = tmp_path / "lib"
    src1.mkdir()
    (src1 / "helper.py").write_text("def help(): pass")

    src2 = tmp_path / "docs"
    src2.mkdir()
    (src2 / "readme.txt").write_text("docs here")

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"
    restored = tmp_path / "restored"

    pack([src1, src2], packed, config)
    unpack(packed, restored, config)

    assert (restored / "lib" / "helper.py").read_text() == "def help(): pass\n"
    assert (restored / "docs" / "readme.txt").read_text() == "docs here\n"


def test_file_outside_root_raises(tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text("secret")
    inside = tmp_path / "inside"
    inside.mkdir()

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"

    import pytest
    with pytest.raises(ValueError, match="outside"):
        pack([inside], packed, config, files=[outside])


def test_pack_no_source_raises(tmp_path):
    packed = tmp_path / "archive.txt"

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
    }

    import pytest
    with pytest.raises(ValueError, match="exist"):
        pack([tmp_path / "nonexistent"], packed, config)


def test_unpack_rejects_parent_dir_traversal(tmp_path):
    dest = tmp_path / "dest"
    archive = tmp_path / "archive.txt"
    archive.write_text(
        "===============\n"
        "== ../outside.txt ==\n"
        "===============\n"
        "malicious\n"
    )
    config = {"encoding": "utf-8"}

    import pytest
    with pytest.raises(ValueError, match="outside"):
        unpack(archive, dest, config)
    assert not (tmp_path / "outside.txt").exists()


def test_unpack_rejects_deep_parent_traversal(tmp_path):
    dest = tmp_path / "a" / "b" / "c"
    archive = tmp_path / "archive.txt"
    archive.write_text(
        "=========================\n"
        "== ../../../../outside.txt ==\n"
        "=========================\n"
        "gotcha\n"
    )
    config = {"encoding": "utf-8"}

    import pytest
    with pytest.raises(ValueError, match="outside"):
        unpack(archive, dest, config)


def test_unpack_rejects_absolute_path(tmp_path):
    dest = tmp_path / "dest"
    archive = tmp_path / "archive.txt"
    archive.write_text(
        "===================\n"
        "== /tmp/evil.txt ==\n"
        "===================\n"
        "evil\n"
    )
    config = {"encoding": "utf-8"}

    import pytest
    with pytest.raises(ValueError, match="outside"):
        unpack(archive, dest, config)


def test_unpack_allows_normal_subdir_path(tmp_path):
    dest = tmp_path / "dest"
    archive = tmp_path / "archive.txt"
    archive.write_text(
        "===================\n"
        "== normal/file.txt ==\n"
        "===================\n"
        "content\n"
    )
    config = {"encoding": "utf-8"}
    unpack(archive, dest, config)
    assert (dest / "normal" / "file.txt").read_text() == "content\n"


def test_roundtrip_byte_fidelity(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.txt").write_bytes(b"line1\nline2\n")

    config = {
        "exclude": [],
        "remove_blank_lines": False,
        "encoding": "utf-8",
        "header": {"prefix": "==", "border_char": "="},
    }

    packed = tmp_path / "archive.txt"
    restored = tmp_path / "restored"

    pack([src], packed, config)
    unpack(packed, restored, config)

    assert b"\r\n" not in packed.read_bytes()
    assert (restored / "src" / "a.txt").read_bytes() == b"line1\nline2\n"


def test_unpack_overwrites_existing_files(tmp_path):
    dest = tmp_path / "dest"
    target = dest / "normal" / "file.txt"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"old\n")

    archive = tmp_path / "archive.txt"
    archive.write_text(
        "===================\n"
        "== normal/file.txt ==\n"
        "===================\n"
        "content\n",
        newline="\n",
    )
    config = {"encoding": "utf-8"}

    unpack(archive, dest, config)
    unpack(archive, dest, config)

    assert (dest / "normal" / "file.txt").read_bytes() == b"content\n"


def test_unpack_rejects_symlink_escape(tmp_path):
    import pytest
    outside = tmp_path / "outside"
    outside.mkdir()
    dest = tmp_path / "dest"
    dest.mkdir()
    link = dest / "link"

    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("cannot create symlinks on this system")

    archive = tmp_path / "archive.txt"
    archive.write_text(
        "====================\n"
        "== link/evil.txt ==\n"
        "====================\n"
        "evil\n"
    )
    config = {"encoding": "utf-8"}

    import pytest
    with pytest.raises(ValueError, match="outside"):
        unpack(archive, dest, config)
    assert not (outside / "evil.txt").exists()
