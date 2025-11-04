# Changelog

## [0.1.2] - 2025-11-04

### Changed
- Rewrote README in English and clarified CLI/API examples.
- Added internal publishing guide under `docs/publishing.md` for TestPyPI/PyPI releases.

## [0.1.0] - 2025-11-04

### Added
- External MIME-based dataset downloader at `scripts/update_extension_dataset.py` to enrich extension metadata automatically.
- JSON dataset `filesinfo/data/external_extensions.json` with 1 243 additional cross-platform extensions, complete with source and compressibility metadata.
- CLI options for platform lookups (`--platform`, `--include-cross-platform`, `--details`) and dataset inspection (`--show-dataset-issues`).
- Public helpers `get_extension_records_for_platform`, `get_extensions_for_platform`, and `get_dataset_issues` for richer API access.
- Installable Python package layout (`filesinfo`), exposing a public `__init__` API and console entry point.

### Changed
- Core logic now lives under `filesinfo/core.py`, building indices from both static tables and external datasets while returning normalized platform tags (e.g. `windows`, `linux`).
- Test suite expanded to cover platform aliasing, cross-platform toggling, and external dataset integration.
- README updated with new usage examples, dataset refresh instructions, and validation tips.
