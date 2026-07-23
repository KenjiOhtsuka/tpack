import os
from pathlib import Path

from tpack.packer import pack
from tpack.unpacker import unpack
from tpack.config import load_config


def test_pack_and_unpack(tmp_path):
    # Arrange: create sample directory
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

    # Act: pack → unpack
    pack(src, packed, config)
    unpack(packed, restored, config)

    # Assert: restored files match original
    assert (restored / "a.txt").read_text() == "hello\nworld\n"
    assert (restored / "b.txt").read_text() == "line1\n\nline2\n"


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

    pack(src, packed, config)
    unpack(packed, restored, config)

    assert (restored / "keep.txt").exists()
    assert not (restored / "ignore.log").exists()


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

    pack(src, packed, config)
    unpack(packed, restored, config)

    assert (restored / "a.txt").read_text() == "line1\nline2\n"


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
    pack(src, packed, config)

    text = packed.read_text()

    # header should look like:
    # ##-------##
    # ## x.txt ##
    # ##-------##
    assert "##-------##" in text
    assert "## x.txt ##" in text
