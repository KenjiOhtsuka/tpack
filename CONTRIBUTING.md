## Local Development

tpack can be developed and tested locally without installation.

### Run as a module

The package supports module execution:

```bash
python -m tpack -d <dir> -o output.txt
python -m tpack archive.txt -u -o restored
```

This is useful when testing the package layout or import behavior.

### Run tests

```bash
pytest -q
python -m pytest tests
```
