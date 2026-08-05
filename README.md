# FilesInfo

[![CI](https://github.com/cagritas/filesinfo/actions/workflows/ci.yml/badge.svg)](https://github.com/cagritas/filesinfo/actions/workflows/ci.yml)

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

# Output in JSON format for automated systems
filesinfo payload.exe archive.tar.gz --json

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

## Developer Commands (Makefile)

For developers contributing to this repository, a `Makefile` is provided to easily install dev dependencies, run tests, and format code:

```bash
make install  # Installs the package with [dev] dependencies
make test     # Runs the unittest suite
make lint     # Runs ruff and black check
make format   # Automatically formats the codebase with ruff and black
```

## Updating the Dataset

Regenerate the MIME-driven extension dataset whenever you want the latest upstream metadata:

```bash
python3 scripts/update_extension_dataset.py
```

The command writes a fresh `filesinfo/data/external_extensions.json` file that is packaged with the library.
