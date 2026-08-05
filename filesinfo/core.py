from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from importlib import resources
from typing import List, Tuple

import filetype

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class FormatRecord:
    """Normalized representation for a single file format entry."""

    extension: str
    description: str
    platform: str
    category: str


def _load_internal_dataset():
    resource = resources.files(__package__).joinpath("data", "internal_extensions.json")
    if not resource.exists():
        log.warning("Internal extension dataset %s is missing.", resource)
        return {}

    try:
        with resource.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
            if not isinstance(data, dict):
                raise ValueError("Dataset must be a dict of categories")
            return data
    except Exception as exc:
        log.error("Failed to load internal dataset %s: %s", resource, exc)
        return {}


STATIC_DATASETS = _load_internal_dataset()


def _load_external_dataset():
    resource = resources.files(__package__).joinpath("data", "external_extensions.json")
    if not resource.exists():
        log.warning("External extension dataset %s is missing.", resource)
        return []

    try:
        with resource.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
            if not isinstance(data, list):
                raise ValueError("Dataset must be a list of objects")
            return data
    except Exception as exc:  # pragma: no cover - defensive logging
        log.error("Failed to load external dataset %s: %s", resource, exc)
        return []


def _normalize_extension(value):
    if not value:
        return None
    value = value.lower()
    if not value.startswith("."):
        value = f".{value}"
    return value


def _normalize_platform(value):
    if not value:
        return None
    return value.strip().lower()


def _build_indices(static_datasets):
    extension_registry = {}
    platform_registry = {}
    issues = []

    def add_issue(message):
        issues.append(message)

    def normalise_entry(category, entry):
        if not isinstance(entry, dict):
            add_issue(f"{category}: entry {entry!r} is not a dictionary")
            return None

        extension = entry.get("ext")
        if not extension:
            add_issue(f"{category}: entry {entry!r} is missing 'ext'")
            return None

        extension = str(extension).strip()
        if not extension:
            add_issue(f"{category}: entry {entry!r} has blank 'ext'")
            return None

        if not extension.startswith("."):
            add_issue(
                f"{category}: extension {extension!r} normalised with leading dot"
            )
            extension = f".{extension.lstrip('.')}"

        description = entry.get("type", "")
        if description is None:
            description = ""
        description = str(description).strip()

        platform = entry.get("os", "")
        if platform is None:
            platform = ""
        platform = str(platform).strip()

        return extension, description, platform

    def register_record(category, extension, description, platform):
        normalized_extension = extension.lower()
        normalized_platform = _normalize_platform(platform) or ""

        record = FormatRecord(
            extension=extension,
            description=description,
            platform=normalized_platform,
            category=category,
        )

        extension_registry.setdefault(normalized_extension, set()).add(record)

        if normalized_platform:
            platform_registry.setdefault(normalized_platform, set()).add(record)

    for category, entries in static_datasets.items():
        for entry in entries:
            normalised = normalise_entry(category, entry)
            if not normalised:
                continue
            register_record(category, *normalised)

    for entry in _load_external_dataset():
        normalised = normalise_entry("external", entry)
        if not normalised:
            continue
        register_record("external", *normalised)

    normalized_extension_registry = {
        extension: tuple(
            sorted(
                records,
                key=lambda record: (
                    record.category,
                    record.platform,
                    record.description,
                ),
            )
        )
        for extension, records in extension_registry.items()
    }

    normalized_platform_registry = {
        platform: tuple(
            sorted(
                records,
                key=lambda record: (
                    record.extension,
                    record.category,
                    record.description,
                ),
            )
        )
        for platform, records in platform_registry.items()
    }

    return normalized_extension_registry, normalized_platform_registry, tuple(issues)


FORMAT_REGISTRY, PLATFORM_REGISTRY, DATASET_ISSUES = _build_indices(STATIC_DATASETS)
DEFAULT_PLATFORMS = ["unknown"]


def get_dataset_issues() -> Tuple[str, ...]:
    """Return validation notices collected while loading datasets."""

    return DATASET_ISSUES


if DATASET_ISSUES:
    log.warning(
        "Dataset validation reported %d issue(s). Use get_dataset_issues() to inspect them.",
        len(DATASET_ISSUES),
    )

PLATFORM_ALIASES = {
    "win": ["windows"],
    "win7": ["windows"],
    "win10": ["windows"],
    "win11": ["windows"],
    "windows7": ["windows"],
    "windows10": ["windows"],
    "windows11": ["windows"],
    "linux22": ["linux"],
    "gnu/linux": ["linux"],
    "mac": ["macos"],
    "osx": ["macos"],
    "os x": ["macos"],
    "iphone": ["ios"],
    "ipad": ["ios"],
    "androidos": ["android"],
    "all": ["cross-platform"],
}


def _resolve_platform_keys(platform_name):
    normalized = _normalize_platform(platform_name)
    if not normalized:
        return ()

    if normalized in PLATFORM_REGISTRY:
        return (normalized,)

    aliases = PLATFORM_ALIASES.get(normalized)
    if aliases:
        return tuple(aliases)

    return ()


def get_extension_metadata(file_extension: str) -> Tuple[FormatRecord, ...]:
    """Return all recorded metadata for the requested extension."""

    normalized_extension = _normalize_extension(file_extension)
    if not normalized_extension:
        return ()
    return FORMAT_REGISTRY.get(normalized_extension, ())


def get_extension_records_for_platform(
    platform_name: str, include_cross_platform: bool = True
) -> Tuple[FormatRecord, ...]:
    """Return rich metadata for extensions associated with the given platform."""

    keys = _resolve_platform_keys(platform_name)
    if not keys:
        return ()

    records = set()
    for key in keys:
        records.update(PLATFORM_REGISTRY.get(key, ()))

    if include_cross_platform and "cross-platform" not in keys:
        records.update(PLATFORM_REGISTRY.get("cross-platform", ()))

    return tuple(
        sorted(
            records,
            key=lambda record: (record.extension, record.category, record.description),
        )
    )


def get_extensions_for_platform(
    platform_name: str, include_cross_platform: bool = True
) -> List[str]:
    """Return the ordered list of extensions associated with the given platform."""

    records = get_extension_records_for_platform(
        platform_name, include_cross_platform=include_cross_platform
    )
    extension_order = []
    seen = set()
    for record in records:
        if record.extension not in seen:
            extension_order.append(record.extension)
            seen.add(record.extension)
    return extension_order


def get_platforms_for_extension(file_extension: str) -> List[str]:
    """Return the list of normalized platforms associated with an extension."""

    records = get_extension_metadata(file_extension)
    if not records:
        return []

    platforms = {record.platform for record in records if record.platform}

    if not platforms:
        return []

    if "cross-platform" in platforms and len(platforms) > 1:
        platforms.discard("cross-platform")

    if not platforms and any(record.platform == "cross-platform" for record in records):
        return ["cross-platform"]

    return sorted(platforms)


def get_os_by_extension(file_extension: str) -> List[str]:
    platforms = get_platforms_for_extension(file_extension)
    if platforms:
        return platforms

    log.warning(
        "No file metadata was found for the extension %s. Falling back to %s.",
        file_extension,
        ", ".join(DEFAULT_PLATFORMS),
    )
    return DEFAULT_PLATFORMS


def file_info_expert(filename: str) -> List[str]:
    # Check magic bytes if file exists
    if os.path.isfile(filename):
        try:
            kind = filetype.guess(filename)
            if kind is not None:
                magic_ext = "." + kind.extension
                platforms = get_os_by_extension(magic_ext)
                if platforms and platforms != DEFAULT_PLATFORMS:
                    return platforms
        except Exception as e:
            log.debug("Failed to guess filetype for %s: %s", filename, e)

    parts = filename.split(".")

    if len(parts) > 1:
        basic_extension = "." + parts[-1]
    else:
        basic_extension = os.path.splitext(filename)[1]

    platforms = get_os_by_extension(basic_extension)

    if len(parts) > 2 and platforms in (DEFAULT_PLATFORMS, ["cross-platform"]):
        full_extension = "." + ".".join(parts[-2:])
        extended_match = get_os_by_extension(full_extension)
        if extended_match:
            platforms = extended_match

    return platforms
