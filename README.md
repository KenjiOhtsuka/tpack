# tpack

tpack is a lightweight text-based archiver that packs a directory into a single text file and restores it in another environment.  
Unlike binary formats such as ZIP or TAR, tpack produces a fully readable UTF‑8 text archive that preserves file boundaries using configurable headers.

- Cross‑platform (Windows / macOS / Linux)
  - Output is always UTF‑8 with LF (`\n`) newlines
  - Configurable exclude rules, header format, and whitespace handling
  - Designed as a simple and portable CLI tool installable via pip

---

## ✨ Features

- **Pack**: Convert a directory into a single text archive  
  - **Unpack**: Restore files from a text archive  
  - **Configurable behavior** via YAML:
    - Glob-based exclude patterns
    - Optional blank-line removal
    - Custom header prefix and border characters
    - Custom encoding (default: UTF‑8)
  - Binary files are automatically skipped
  - Deterministic output format suitable for version control or diff tools

---

## 📦 Installation

```bash
pip install tpack
```

---

## 🚀 Usage

### Pack a directory

```bash
tpack <source_dir> -o output.txt
```

Example:

```bash
tpack src -o archive.txt
```

#### Output File Safety

When packing a directory, tpack automatically excludes the output file if it
is located inside the source directory. This prevents the archive from
accidentally including or overwriting itself.

Example:

```bash
tpack src -o src/archive.txt
```


In this case, `archive.txt` is inside `src/`, so tpack will automatically
exclude it from the pack operation. This behavior applies whether the paths are
specified as absolute or relative; tpack normalizes paths internally to
ensure correct detection.

If the output file is outside the source directory, no exclusion is applied.

---

### Unpack an archive

```bash
tpack -u archive.txt -d restored_dir
```

Example:

```bash
tpack -u archive.txt -d restored
```

---

## ⚙ Configuration (config.yaml)

tpack supports a YAML configuration file to customize its behavior.

```yaml
exclude:
  - node_modules
  - "*.log"
  - "*.jar"

remove_blank_lines: true
encoding: "utf-8"

header:
  prefix: "=="
  border_char: "="
```

### Apply configuration

```bash
tpack src -o archive.txt -c config.yaml
tpack -u archive.txt -d restored -c config.yaml
```

---

## 📁 Output Format Example

```
===========
== a.txt ==
===========
hello
world
```

The header format is controlled by `prefix` and `border_char`.

---

## 🧪 Testing

tpack includes pytest-based tests.

```bash
pytest -q
```

---

## 📂 Project Structure

```
tpack/
  tpack/
    __init__.py
    cli.py
    packer.py
    unpacker.py
    config.py
  pyproject.toml
  README.md
  tests/
    test_tpack.py
```

---

## 📜 License

MIT License

---

## 🤝 Contributing

Issues and pull requests are welcome.
