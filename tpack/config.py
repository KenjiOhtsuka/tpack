"""
Configuration loader for tpack.
"""

from pathlib import Path
import yaml

DEFAULT_CONFIG = {
    "exclude": [],
    "remove_blank_lines": False,
    "encoding": "utf-8",
    "header": {
        "prefix": "==",
        "border_char": "=",
    },
}


def load_config(path):
    """
    Load configuration from YAML file and merge with defaults.
    """

    if path is None:
        return DEFAULT_CONFIG.copy()

    path = Path(path)
    if not path.exists():
        return DEFAULT_CONFIG.copy()

    with open(path, "r", encoding="utf-8") as f:
        user_cfg = yaml.safe_load(f) or {}

    merged = DEFAULT_CONFIG.copy()

    for key, value in user_cfg.items():
        if key == "header":
            merged_header = DEFAULT_CONFIG["header"].copy()
            merged_header.update(value or {})
            merged["header"] = merged_header
        else:
            merged[key] = value

    return merged
