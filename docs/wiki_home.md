# FilesInfo Wiki

FilesInfo is a compact toolkit that answers two key questions about any filename:

1. **What kind of file is this extension?**
2. **Which operating systems or sandboxes should handle it?**

The project ships as both a Python package and a command-line tool, backed by thousands of curated extension records. This page collects the essential information to help you get the most out of FilesInfo.

---

## Table of Contents

- [Overview](#overview)
- [Dataset Structure](#dataset-structure)
- [CLI Quick Reference](#cli-quick-reference)
- [Python API Examples](#python-api-examples)
- [Dataset Update Workflow](#dataset-update-workflow)
- [Visual Snapshot](#visual-snapshot)
- [Publishing Checklist](#publishing-checklist)
- [Useful Links](#useful-links)

---

## Overview

FilesInfo combines static extension catalogs with a dynamically generated MIME-based dataset. Each entry records:

- Extension (e.g. `.exe`, `.pyc`)
- Human-readable description
- Target platform(s) (`windows`, `linux`, `macos`, `cross-platform`, etc.)
- Category (`executable`, `developer`, `system`, …)

The repository includes:

- `filesinfo/` — Python package with API and CLI
- `filesinfo/data/external_extensions.json` — auto-generated MIME dataset
- `scripts/update_extension_dataset.py` — pulls fresh MIME info
- `tests/` — unittests covering key behaviors
- `docs/` — internal publishing notes, dataset charts (optional)

---

## Dataset Structure

| Category       | Description                                      | Source                        |
|----------------|--------------------------------------------------|-------------------------------|
| `executable`   | Native binaries, scripts, installers              | curated static list           |
| `commondata`   | Documents, archives, multimedia                   | curated static list           |
| `system`       | OS-specific artifacts (logs, configs, caches)     | curated static list           |
| `developer`    | Code, project files, tool metadata                | curated static list           |
| `commontext`   | Plain text, configs, markup                       | curated static list           |
| `crossplatform`| Extension is likely to work anywhere              | curated static list           |
| `external`     | MIME-derived entries (cross-platform by default)  | `update_extension_dataset.py` |

Lookup helpers provide:

- `file_info_expert("payload.exe") -> ["windows"]`
- `get_extensions_for_platform("linux")`
- `get_extension_records_for_platform("macos")`
- `get_dataset_issues()` to inspect validation warnings

---

## CLI Quick Reference

```bash
# Resolve platforms for filenames
filesinfo payload.exe archive.tar.gz

# List extensions for given platforms
filesinfo --platform windows --platform linux

# Include cross-platform records
filesinfo --platform linux --include-cross-platform

# Detailed metadata (extension + category, description, platform)
filesinfo --platform macos --details

# Show dataset validation issues (if any)
filesinfo --show-dataset-issues
```

---

## Python API Examples

```python
from filesinfo import file_info_expert, get_extension_records_for_platform

# Find platforms for a filename
print(file_info_expert("installer.run"))  # ['linux']

# Detailed records for Windows (first 3 entries as sample)
windows_records = get_extension_records_for_platform("windows")
for record in windows_records[:3]:
    print(record.extension, record.category, record.description)
```

---

## Dataset Update Workflow

1. Run the MIME update script:
   ```bash
   python3 scripts/update_extension_dataset.py
   ```
   Generates `filesinfo/data/external_extensions.json`.

2. Run tests:
   ```bash
   python3 -m unittest
   ```

3. Rebuild the package:
   ```bash
   rm -rf dist/*
   PIP_USER=0 python3 -m build
   ```

4. Upload:
   ```bash
   # TestPyPI (optional)
   python3 -m twine upload --repository testpypi dist/*

   # PyPI
   python3 -m twine upload dist/*
   ```

---

## Visual Snapshot

> (Optional) Generate a pie chart or table to summarize the dataset. Example approach:

```python
# scripts/generate_stats.py (example)
from collections import Counter
from filesinfo import FORMAT_REGISTRY
import matplotlib.pyplot as plt

counter = Counter()
for records in FORMAT_REGISTRY.values():
    for record in records:
        counter[record.platform or "cross-platform"] += 1

labels, values = zip(*counter.most_common())
plt.figure(figsize=(6, 6))
plt.pie(values, labels=labels, autopct="%1.1f%%")
plt.title("File Extension Coverage by Platform")
plt.savefig("docs/platform_distribution.png")
```

Once generated, embed the image here:

![Platform Distribution](../docs/platform_distribution.png)

---

## Publishing Checklist

1. Update version in `pyproject.toml` and `filesinfo/__init__.py`.
2. Draft release notes in `CHANGELOG.md`.
3. Refresh dataset (if needed), run tests, build artifacts.
4. Upload with Twine.
5. Tag and push (`git tag v0.x.y && git push origin main --tags`).
6. Update README / Wiki if new features or data sources were added.

---

## Useful Links

- **GitHub Repository:** [https://github.com/cagritas/filesinfo](https://github.com/cagritas/filesinfo)
- **Documentation:** This wiki + README
- **PyPI Package:** (pending) `pip install filesinfo`
- **Publishing Guide:** [`docs/publishing.md`](../docs/publishing.md)
- **Issue Tracker:** GitHub Issues

---

Need improvements or have ideas? Open an issue or submit a PR!
