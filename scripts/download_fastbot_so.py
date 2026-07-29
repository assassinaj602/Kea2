#!/usr/bin/env python3
"""Download historical Fastbot native libraries into a local cache.

The downloaded files are intended to be consumed by Kea2's future
``--fastbot-so-version`` runtime option.  The requested version is used as a
Git tag or commit ref on the Kea2 repositories.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kea2.fastbot_so_downloader import (
    ABIS,
    GIT_REF_PATTERN,
    default_cache_dir,
    ensure_libraries,
    is_valid_library,
    library_path,
    missing_abis,
    raw_library_urls,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Historical SO version (e.g., v1.2.3; Git tag or commit SHA).")
    parser.add_argument("--cache-dir", type=Path, default=default_cache_dir(), help="Root directory for downloaded libraries.")
    parser.add_argument("--force", action="store_true", help="Re-download libraries even when a valid cached file exists.")
    parser.add_argument("--timeout", type=int, default=30, help="Per-file HTTP timeout in seconds.")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    if not GIT_REF_PATTERN.fullmatch(args.version):
        parser.error("--version must be a Git tag or commit ref containing only letters, digits, '.', '_' and '-'")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = ensure_libraries(
            args.version,
            cache_dir=args.cache_dir,
            timeout=args.timeout,
            force=args.force,
            progress=print,
        )
    except (RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Fastbot {args.version} libraries cached in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
