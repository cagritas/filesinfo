"""Public package interface for File Info Expert."""

from .core import (
    DEFAULT_PLATFORMS,
    FormatRecord,
    file_info_expert,
    get_dataset_issues,
    get_extension_metadata,
    get_extension_records_for_platform,
    get_extensions_for_platform,
    get_os_by_extension,
    get_platforms_for_extension,
)

__all__ = [
    "DEFAULT_PLATFORMS",
    "FormatRecord",
    "file_info_expert",
    "get_dataset_issues",
    "get_extension_metadata",
    "get_extension_records_for_platform",
    "get_extensions_for_platform",
    "get_os_by_extension",
    "get_platforms_for_extension",
]

__version__ = "0.1.2"
