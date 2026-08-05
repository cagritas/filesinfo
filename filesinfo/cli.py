"""Command-line entry point for the FilesInfo package."""

from __future__ import annotations

import argparse
import json
from typing import Any, List, Optional, Tuple

from . import (
    file_info_expert,
    get_dataset_issues,
    get_extension_records_for_platform,
    get_extensions_for_platform,
)


def resolve_names(filenames: List[str]) -> List[Tuple[str, List[str]]]:
    results = []
    for name in filenames:
        platforms = file_info_expert(name)
        results.append((name, platforms))
    return results


def describe_platforms(
    platforms: List[str],
    include_cross_platform: bool = False,
    include_details: bool = False,
) -> List[Tuple[str, Any]]:
    reports = []
    for name in platforms:
        if include_details:
            records = get_extension_records_for_platform(
                name, include_cross_platform=include_cross_platform
            )
            entries = [
                {
                    "extension": record.extension,
                    "description": record.description,
                    "category": record.category,
                    "platform": record.platform,
                }
                for record in records
            ]
        else:
            entries = get_extensions_for_platform(
                name, include_cross_platform=include_cross_platform
            )

        reports.append((name, entries))

    return reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect file extension metadata and platform mappings."
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="File names (with extensions) to evaluate",
    )
    parser.add_argument(
        "-p",
        "--platform",
        dest="platforms",
        action="append",
        help="Platform name to list extensions for (repeatable)",
    )
    parser.add_argument(
        "--include-cross-platform",
        action="store_true",
        help="Include cross-platform extensions when listing by platform",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Show detailed records instead of only extension strings",
    )
    parser.add_argument(
        "--show-dataset-issues",
        action="store_true",
        help="Display dataset validation warnings",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.filenames and not args.platforms:
        parser.error("Provide at least one file name or --platform")

    output_data = {}

    if args.filenames:
        output_data["filenames"] = [
            {"filename": name, "platforms": platforms}
            for name, platforms in resolve_names(args.filenames)
        ]

    if args.platforms:
        output_data["platforms"] = [
            {"platform": name, "extensions": entries}
            for name, entries in describe_platforms(
                args.platforms,
                include_cross_platform=args.include_cross_platform,
                include_details=args.details,
            )
        ]

    if args.show_dataset_issues:
        output_data["dataset_issues"] = list(get_dataset_issues())

    if args.json:
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        if "filenames" in output_data:
            for item in output_data["filenames"]:
                platforms = (
                    ", ".join(item["platforms"]) if item["platforms"] else "unknown"
                )
                print(f"{item['filename']}: {platforms}")

        if "platforms" in output_data:
            for item in output_data["platforms"]:
                print(f"\nPlatform: {item['platform']}")
                if not item["extensions"]:
                    print("  (No extensions found)")
                else:
                    for ext in item["extensions"]:
                        if isinstance(ext, dict):
                            print(f"  {ext['extension']:<15} {ext['description']}")
                        else:
                            print(f"  {ext}")

        if "dataset_issues" in output_data:
            print("\nDataset Issues:")
            for issue in output_data["dataset_issues"]:
                print(f"  - {issue}")


if __name__ == "__main__":  # pragma: no cover
    main()
