## Local Development

tpack can be developed and tested locally without installation.

### Run the CLI directly

During development, you can run the CLI using Python:

```bash
python tpack/cli.py <source_dir> -o output.txt
python tpack/cli.py -u archive.txt -d restored
```

### Run as a module

The package also supports module execution:

```bash
python -m tpack <source_dir> -o output.txt
python -m tpack -u archive.txt -d restored
```

This is useful when testing the package layout or import behavior.

### Run tests

```bash
pytest -q
python -m pytest tests
```
