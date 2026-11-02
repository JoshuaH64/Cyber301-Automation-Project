# Cyber301-Automation-Project

## Project Selected
**Renaming Files with American-Style Dates to European-Style Dates**, from
Al Sweigart's [*Automate the Boring Stuff with Python*](https://automatetheboringstuff.com/).

## What the Script Does
`rename_dates.py` scans a folder for files whose names contain a date in
American format (`MM-DD-YYYY`) and renames them to European format
(`DD-MM-YYYY`). For example:

| Before | After |
|---|---|
| `report_03-15-2024.txt` | `report_15-03-2024.txt` |
| `spam_12-25-2023_eggs.txt` | `spam_25-12-2023_eggs.txt` |
| `photo_7-4-2022.jpg` | `photo_4-7-2022.jpg` |

Files with no date, or with an impossible date (like `02-30-2024` or month 13),
are left untouched.

## How to Run
Requires Python 3.6 or newer. No extra packages are needed.

```bash
# 1. Preview the changes without renaming anything (recommended first)
python rename_dates.py sample_files --dry-run

# 2. Rename the files for real
python rename_dates.py sample_files

# 3. Include subfolders
python rename_dates.py sample_files --recursive
```

### Sample Output
```
WOULD RENAME: photo_7-4-2022.jpg -> photo_4-7-2022.jpg
WOULD RENAME: report_03-15-2024.txt -> report_15-03-2024.txt
WOULD RENAME: spam_12-25-2023_eggs.txt -> spam_25-12-2023_eggs.txt

Done. 3 file(s) would be renamed.
```

The `sample_files/` folder contains empty practice files, including some with
invalid dates, so you can test safely.

## Improvements and Modifications
Beyond the version in the book, I added:
- **Command-line arguments** (`argparse`) instead of hard-coding the folder
- **`--dry-run` mode** to preview changes before renaming
- **`--recursive` option** to process subfolders
- **Date validation** so impossible dates (e.g., `02-30-2024`) are skipped
- **Overwrite protection**: a file is skipped if the new name already exists
- Uses `pathlib` for cleaner path handling

## Challenges I Encountered
I had trouble handling dates without leading zeros. My first version of the regular expression only matched dates written with two digits, like 03-15-2024.

## Notes
- Dates are assumed to be `MM-DD-YYYY`. A name like `04-07-2022` is always
  treated as April 7 (it becomes `07-04-2022`), and the script cannot tell if
  it was already European-style. Run it only once per set of files.
