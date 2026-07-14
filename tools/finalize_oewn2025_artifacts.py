#!/usr/bin/env python3
"""Copy mandatory upstream attribution and seal the OEWN artifact manifest."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", required=True, type=Path)
    parser.add_argument("--artifact-root", required=True, type=Path)
    args = parser.parse_args()
    source = args.source_repo.resolve()
    root = args.artifact_root.resolve()
    root.mkdir(parents=True, exist_ok=True)

    for name, destination in (
        ("LICENSE.md", "UPSTREAM_LICENSE.md"),
        ("WNDB_License.txt", "UPSTREAM_WNDB_LICENSE.txt"),
    ):
        origin = source / name
        if not origin.is_file():
            raise FileNotFoundError(origin)
        shutil.copyfile(origin, root / destination)

    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    repository_artifacts = root.parent
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == manifest_path:
            continue
        files.append(
            {
                "path": path.relative_to(repository_artifacts).as_posix(),
                "sha256": digest(path),
                "bytes": path.stat().st_size,
            }
        )
    manifest["files"] = files
    manifest["license_files"] = ["UPSTREAM_LICENSE.md", "UPSTREAM_WNDB_LICENSE.txt"]
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
