# FilesInfo

FilesInfo is a Python toolkit for mapping file extensions to rich metadata and recommended execution platforms. It ships with an extensive extension catalog, powerful lookup helpers, and a convenient CLI for exploring the data.

## Installation

Clone the repository and install the package in editable mode (or publish to PyPI/TestPyPI and install from there):

```bash
pip install .
```

The installation exposes the `filesinfo` command-line tool automatically.

## Command-Line Usage

```bash
# Inspect platform recommendations for file names
filesinfo payload.exe archive.tar.gz

# List extensions supported on specific platforms
filesinfo --platform windows --platform linux --include-cross-platform

# Show detailed metadata for each match
filesinfo --platform macos --details

# Review dataset validation warnings
filesinfo --show-dataset-issues
```

For backwards compatibility the legacy `run_demo.py` script simply forwards to the same CLI entry point.

## Python API Example

```python
from filesinfo import file_info_expert, get_extensions_for_platform

print(file_info_expert("payload.exe"))
# ['windows']

print(get_extensions_for_platform("linux", include_cross_platform=False)[:10])
```

## Updating the Dataset

Regenerate the MIME-driven extension dataset whenever you want the latest upstream metadata:

```bash
python3 scripts/update_extension_dataset.py
```

The command writes a fresh `filesinfo/data/external_extensions.json` file that is packaged with the library.

## Tests

```bash
python3 -m unittest
```

The test suite verifies the core lookups, platform alias behaviour, and integration with the external dataset.
