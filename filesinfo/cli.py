"""Command-line entry point for the FilesInfo package."""

import argparse
from pprint import pprint

from . import (
    file_info_expert,
    get_dataset_issues,
    get_extension_records_for_platform,
    get_extensions_for_platform,
)


def resolve_names(filenames):
    results = []
    for name in filenames:
        platforms = file_info_expert(name)
        results.append((name, platforms))
    return results


def describe_platforms(platforms, include_cross_platform=False, include_details=False):
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


def build_parser():
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
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.filenames and not args.platforms:
        parser.error("Provide at least one file name or --platform")

    if args.filenames:
        for name, platforms in resolve_names(args.filenames):
            pprint({"filename": name, "platforms": platforms})

    if args.platforms:
        for name, entries in describe_platforms(
            args.platforms,
            include_cross_platform=args.include_cross_platform,
            include_details=args.details,
        ):
            pprint({"platform": name, "extensions": entries})

    if args.show_dataset_issues:
        pprint({"dataset_issues": list(get_dataset_issues())})


if __name__ == "__main__":  # pragma: no cover
    main()
