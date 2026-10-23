#!/usr/bin/env python3
"""Check (and optionally rewrite) Helm chart .tgz for macOS junk files.

Forbidden archive members:
  - AppleDouble siblings: basename starts with '._'
  - Finder junk: .DS_Store
  - zip-style macOS metadata dir: __MACOSX/

Exit code 0 = clean; 1 = dirty or error.

Examples:
  python3 scripts/check-chart-tgz.py charts/*.tgz
  python3 scripts/check-chart-tgz.py --fix charts/velero-12.2.1.tgz
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


JUNK_HINTS = ("._*", ".DS_Store", "__MACOSX")


def is_junk(name: str) -> bool:
    parts = Path(name).parts
    base = Path(name).name
    if base.startswith("._"):
        return True
    if base == ".DS_Store":
        return True
    if "__MACOSX" in parts:
        return True
    return False


def list_junk(archive: Path) -> list[str]:
    with tarfile.open(archive, "r:gz") as tf:
        return [m.name for m in tf.getmembers() if is_junk(m.name)]


def chart_root_name(members: list[tarfile.TarInfo]) -> str | None:
    """Best-effort top-level chart directory name."""
    for m in members:
        parts = Path(m.name).parts
        if not parts:
            continue
        if is_junk(m.name):
            continue
        return parts[0]
    return None


def fix_archive(archive: Path) -> None:
    """Filter junk and re-package with helm package when possible."""
    with tempfile.TemporaryDirectory(prefix="chart-fix-") as tmp:
        tmp_path = Path(tmp)
        extract_dir = tmp_path / "src"
        extract_dir.mkdir()
        with tarfile.open(archive, "r:gz") as tf:
            members = [m for m in tf.getmembers() if not is_junk(m.name)]
            root = chart_root_name(members)
            if not root:
                raise RuntimeError(f"{archive}: no valid chart members")
            for m in members:
                if m.name.startswith("/") or ".." in Path(m.name).parts:
                    continue
                tf.extract(m, extract_dir, set_attrs=False)

        chart_dir = extract_dir / root
        if not (chart_dir / "Chart.yaml").is_file():
            raise RuntimeError(f"{archive}: missing {root}/Chart.yaml after extract")

        # Drop any junk that landed on disk (xattr siblings created on extract)
        for p in chart_dir.rglob("*"):
            if p.name.startswith("._") or p.name == ".DS_Store":
                p.unlink(missing_ok=True)

        # Prefer helm package (does not emit AppleDouble)
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        env = os.environ.copy()
        env["COPYFILE_DISABLE"] = "1"
        try:
            subprocess.run(
                ["helm", "package", str(chart_dir), "-d", str(out_dir)],
                check=True,
                env=env,
                capture_output=True,
                text=True,
            )
            built = next(out_dir.glob("*.tgz"))
        except (FileNotFoundError, subprocess.CalledProcessError, StopIteration):
            # Fallback: tar with COPYFILE_DISABLE
            built = out_dir / archive.name
            subprocess.run(
                ["tar", "--exclude=._*", "--exclude=.DS_Store", "--exclude=__MACOSX", "-czf", str(built), root],
                check=True,
                cwd=extract_dir,
                env=env,
            )

        shutil.copy2(built, archive)

        leftover = list_junk(archive)
        if leftover:
            raise RuntimeError(f"{archive}: still dirty after fix: {leftover[:5]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+", type=Path, help="chart .tgz paths")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="rewrite archives in place without macOS junk (uses helm package when available)",
    )
    args = parser.parse_args()

    dirty = 0
    for archive in args.archives:
        if not archive.is_file():
            print(f"ERROR: not a file: {archive}", file=sys.stderr)
            return 1
        junk = list_junk(archive)
        if not junk:
            print(f"OK   {archive}  (clean)")
            continue
        print(f"DIRTY {archive}  junk={len(junk)}")
        for name in junk[:12]:
            print(f"       {name}")
        if len(junk) > 12:
            print(f"       ... +{len(junk) - 12} more")
        if args.fix:
            print(f"FIX  {archive}")
            fix_archive(archive)
            print(f"OK   {archive}  (rewritten)")
        else:
            dirty += 1

    if dirty:
        print(
            f"\n{dirty} archive(s) contain {', '.join(JUNK_HINTS)}. "
            "Re-run with --fix or package via: COPYFILE_DISABLE=1 helm package ./chart",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
