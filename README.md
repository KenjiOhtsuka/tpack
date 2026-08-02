# tpack

tpack is a lightweight text-based archiver that packs a directory into a single text file and restores it in another environment.  
Unlike binary formats such as ZIP or TAR, tpack produces a fully readable UTF‑8 text archive that preserves file boundaries using configurable headers.  
The archive can be inspected, diffed, pasted into documentation, or even provided to AI tools as plain text, while still allowing complete reconstruction of the original directory structure when needed.

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
- Archives are fully readable as plain text: you can inspect the entire directory structure without unpacking, paste it into documentation or chat tools, and even provide it directly to AI systems. When needed, the same archive can be unpacked to fully reconstruct the original directory structure.

---

## 📦 Installation

```bash
pip install tpack
```

---

## 🚀 Usage

### Pack directories or files

```bash
tpack -d <dir> -o output.txt
tpack -f <file> ... -o output.txt
tpack -d <dir> -f <file> ... -o output.txt
```

Examples:

```bash
tpack -d src -o archive.txt
tpack -f README.md -o single_file.txt
tpack -d src -d docs -o combined.txt
```

#### Output File Safety

When packing, tpack automatically excludes the output file if it
is located inside one of the source directories.

Example:

```bash
tpack -d src -o src/archive.txt
```

In this case, `archive.txt` is inside `src/`, so tpack will automatically
exclude it from the pack operation.

---

### Unpack an archive

```bash
tpack <archive> -u -o <dest_dir>
```

Example:

```bash
tpack archive.txt -u -o restored
```

---

### CLI Options

tpack provides several command-line options to control packing and unpacking.

| Option                       | Description                                                                                                                       |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `ARCHIVE` (positional)       | Archive file (required in unpack mode).                                                                                           |
| `-d`, `--dir`                | Source directory to pack (can be specified multiple times).                                                                       |
| `-f`, `--files`              | Specific file to pack (can be specified multiple times).                                                                          |
| `-o`, `--output`             | Output archive file (pack mode) or destination directory (unpack mode). Required.                                                 |
| `-u`, `--unpack`             | Enable unpack mode. Without this flag, tpack runs in pack mode.                                                                   |
| `-c`, `--config`             | Path to a YAML configuration file. If not provided, tpack uses built‑in defaults.                                                |
| `--follow-symlinks`          | Follow symlinks that resolve outside the source directory.                                                                        |

In pack mode: at least one of `-d` or `-f` is required, plus `-o`.
In unpack mode: `ARCHIVE` and `-o` are required.

---

## ⚙ Configuration (config.yaml)

tpack supports a YAML configuration file to customize its behavior.  
All fields are optional—missing fields fall back to built‑in defaults.

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

### Configuration Fields

- **exclude**  
  Glob-based patterns for files or directories to skip during packing.  
  Useful for ignoring build artifacts, dependency folders, or logs.

- **remove_blank_lines**  
  If `true`, blank lines are removed from file content before packing.  
  Helps produce compact archives or normalize whitespace.

- **encoding**  
  Character encoding used when reading files.  
  Defaults to UTF‑8.

- **header.prefix / header.border_char**  
  Controls how file boundaries are displayed in the text archive.  
  For example, the above config produces:

  ```
  ===========
  == a.txt ==
  ===========
  ```

### Apply configuration

```bash
tpack -d src -o archive.txt -c config.yaml
tpack archive.txt -u -o restored -c config.yaml
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
    __main__.py
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

---

## Links

[PyPi page](https://pypi.org/project/tpack/)
