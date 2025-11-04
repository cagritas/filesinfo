+ FilesInfo Publishing Guide

Internal notes for cutting a new release to TestPyPI and PyPI.

## 1. Bump version metadata

1. Update the version number in `pyproject.toml` (`[project] version`).
2. Update `filesinfo/__version__` in `filesinfo/__init__.py`.
3. Create a new section in `CHANGELOG.md` (e.g., `## [0.x.y] - YYYY-MM-DD`) and summarize the changes.

## 2. Refresh the dataset (optional)

If the external MIME dataset needs a refresh:

```bash
python3 scripts/update_extension_dataset.py
```

Commit the updated `filesinfo/data/external_extensions.json` if it changed.

## 3. Regenerate distributions

```bash
rm -rf dist/*
PIP_USER=0 python3 -m build
```

Artifacts will appear under `dist/` (wheel + sdist).

## 4. Upload to TestPyPI

Ensure `~/.pypirc` or environment variables provide the TestPyPI token (`username=__token__`). Then:

```bash
python3 -m twine upload --repository testpypi dist/*
```

Verify at `https://test.pypi.org/project/filesinfo/` and run a smoke test:

```bash
python3 -m venv tmpenv
source tmpenv/bin/activate
pip install -i https://test.pypi.org/simple/ filesinfo==<new-version>
filesinfo payload.exe
deactivate
rm -rf tmpenv
```

## 5. Upload to PyPI

Switch to the production token (still `username=__token__`).

```bash
python3 -m twine upload dist/*
```

Confirm at `https://pypi.org/project/filesinfo/`.

## 6. Tag & push

```bash
git add .
git commit -m "chore: release filesinfo v<new-version>"
git tag v<new-version>
git push origin main --tags
```

Optional: draft release notes on GitHub referencing the PyPI artifact.
