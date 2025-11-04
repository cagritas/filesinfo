"""Fetch external file-extension datasets and build normalized JSON."""

from __future__ import annotations

import json
import pathlib
import sys
import urllib.request


MIME_DB_URL = "https://raw.githubusercontent.com/jshttp/mime-db/master/db.json"


def fetch_mime_db(url: str = MIME_DB_URL) -> dict:
    with urllib.request.urlopen(url) as response:  # nosec - controlled URL
        return json.load(response)


def build_extension_index(mime_db: dict) -> dict:
    extensions = {}
    for mime_type, payload in mime_db.items():
        for ext in payload.get("extensions", []) or []:
            ext = ext.strip().lower()
            if not ext:
                continue

            info = extensions.setdefault(
                f".{ext}",
                {
                    "ext": f".{ext}",
                    "mime_types": set(),
                    "sources": set(),
                    "compressible": set(),
                },
            )

            info["mime_types"].add(mime_type)
            source = payload.get("source")
            if source:
                info["sources"].add(source)
            if "compressible" in payload:
                info["compressible"].add(str(bool(payload["compressible"])) )

    # Convert to JSON serialisable structures
    for record in extensions.values():
        record["mime_types"] = sorted(record["mime_types"])
        record["sources"] = sorted(record["sources"])
        record["compressible"] = sorted(record["compressible"])

    return extensions


def write_dataset(dataset: dict, output_path: pathlib.Path) -> None:
    serialisable = []
    for data in sorted(dataset.values(), key=lambda item: item["ext"]):
        description = ", ".join(data["mime_types"])
        sources = ", ".join(data["sources"]) if data["sources"] else "unknown"
        compressible = ", ".join(data["compressible"]) if data["compressible"] else None

        serialisable.append(
            {
                "ext": data["ext"],
                "type": f"MIME: {description}" if description else "MIME",
                "os": "cross-platform",
                "sources": sources,
                "compressible": compressible,
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as stream:
        json.dump(serialisable, stream, ensure_ascii=False, indent=2)


def main() -> int:
    output_path = (
        pathlib.Path(__file__).resolve().parent.parent
        / "filesinfo"
        / "data"
        / "external_extensions.json"
    )
    print(f"Downloading MIME database from {MIME_DB_URL}…")
    mime_db = fetch_mime_db()
    print("Building extension index…")
    dataset = build_extension_index(mime_db)
    print(f"Writing {len(dataset)} records to {output_path}")
    write_dataset(dataset, output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
