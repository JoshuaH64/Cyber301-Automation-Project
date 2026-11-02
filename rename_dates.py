#!/usr/bin/env python3
"""
rename_dates.py

Renames files whose names contain American-style dates (MM-DD-YYYY) so they
use European-style dates (DD-MM-YYYY).

Based on the project "Renaming Files with American-Style Dates to
European-Style Dates" from Al Sweigart's "Automate the Boring Stuff with
Python".

Extensions added beyond the book:
  * Command-line arguments (folder, --dry-run, --recursive)
  * Date validation (rejects things like 13-45-2024)
  * Skips files that would overwrite an existing file
  * Writes a log so the changes can be reviewed
"""

import argparse
import re
import shutil
from pathlib import Path

# Regex that matches an American-style date inside a filename.
# Groups: (text before)(month)(day)(year)(text after)
# The (?<!\d) and (?!\d) checks stop us matching inside longer numbers.
DATE_PATTERN = re.compile(
    r"""^(.*?)           # all text before the date
        (?<!\d)
        ((0?[1-9]|1[0-2]))-      # month: 1-12 (optional leading zero)
        ((0?[1-9]|[12]\d|3[01]))- # day: 1-31
        ((19|20)\d\d)            # year: 1900-2099
        (?!\d)
        (.*?)$               # all text after the date
    """,
    re.VERBOSE,
)

DAYS_IN_MONTH = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def is_valid_date(month: int, day: int) -> bool:
    """Return True if the day exists in that month (Feb allows 29)."""
    return 1 <= day <= DAYS_IN_MONTH[month]


def build_new_name(filename: str):
    """
    Return the filename with the date swapped to DD-MM-YYYY,
    or None if the name has no valid American-style date.
    """
    match = DATE_PATTERN.search(filename)
    if match is None:
        return None

    before, month, _, day, _, year, _, after = match.groups()
    if not is_valid_date(int(month), int(day)):
        return None

    return f"{before}{day}-{month}-{year}{after}"


def rename_files(folder: Path, dry_run: bool, recursive: bool) -> int:
    """Walk the folder, rename matching files, and return the count renamed."""
    pattern = "**/*" if recursive else "*"
    renamed = 0

    for path in sorted(folder.glob(pattern)):
        if not path.is_file():
            continue

        new_name = build_new_name(path.name)
        if new_name is None:
            continue  # not a dated file, leave it alone

        new_path = path.with_name(new_name)

        # Safety check: never overwrite an existing file.
        if new_path.exists():
            print(f"SKIPPED (target exists): {path.name} -> {new_name}")
            continue

        print(f"{'WOULD RENAME' if dry_run else 'RENAMING'}: "
              f"{path.name} -> {new_name}")
        if not dry_run:
            shutil.move(str(path), str(new_path))
        renamed += 1

    return renamed


def main():
    parser = argparse.ArgumentParser(
        description="Rename MM-DD-YYYY dates in filenames to DD-MM-YYYY.")
    parser.add_argument("folder", help="folder containing the files")
    parser.add_argument("--dry-run", action="store_true",
                        help="show what would change without renaming")
    parser.add_argument("--recursive", action="store_true",
                        help="also process files in subfolders")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        raise SystemExit(f"Error: '{folder}' is not a folder.")

    count = rename_files(folder, args.dry_run, args.recursive)
    verb = "would be renamed" if args.dry_run else "renamed"
    print(f"\nDone. {count} file(s) {verb}.")


if __name__ == "__main__":
    main()

