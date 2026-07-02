#!/usr/bin/env python3
"""Lab 2 worked example: clean JEA Detail.txt and count journal entries per user.

Built from lab02_spec.md. The script reads the raw export (UTF-16 LE,
tab-separated), removes the report header, the upper header line, and the
page-break rows, fixes the Amount and ID columns, then prints a descriptive
summary and writes lab_02_cleaned.csv and lab_02_user_counts.csv.

Two interchangeable paths produce the same output:
  - pandas, the path a student gets from Colab (used when pandas is installed)
  - the Python standard library (used automatically when pandas is not
    installed, so the script runs anywhere)

Run it with no arguments. It looks for a local copy of "JEA Detail.txt" next
to the script or in the working folder, and downloads the course copy from
the web if it finds none. You can also pass a path: python lab02_analysis.py
/path/to/JEA_Detail.txt
"""

import io
import os
import sys
import urllib.request

DATA_URL = ("https://raw.githubusercontent.com/sean-mccaman/acctg5150-090/"
            "main/week-02/JEA%20Detail.txt")
DATA_FILE = "JEA Detail.txt"

# The ten real columns, in order, from the complete (lower) header line.
COLUMNS = ["Account", "Category", "Date", "Period", "ID",
           "Manual", "Description", "Number", "Location", "Amount"]

# Lines above the complete header: the seven report-header lines, the ====
# divider, and the upper (partial) header line.
HEADER_LINES = 9

CLEANED_CSV = "lab_02_cleaned.csv"
COUNTS_CSV = "lab_02_user_counts.csv"


def load_text():
    """Return the raw file as text.

    The file is UTF-16 LE (it opens with the FF FE byte-order mark), so it is
    decoded as utf-16. A UTF-8 read would fail on the first byte. This is the
    defect Power Query hides in Part 1 and a script must be told about.
    """
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [os.path.join(here, DATA_FILE), DATA_FILE]
        path = next((p for p in candidates if os.path.exists(p)), None)
    if path:
        with open(path, encoding="utf-16") as fh:
            return fh.read()
    print("No local copy of " + DATA_FILE + " found; downloading the course copy.")
    with urllib.request.urlopen(DATA_URL) as resp:
        return resp.read().decode("utf-16")


def clean_with_pandas(text):
    """The pandas path. Spec operations 1 through 8, in order."""
    import pandas as pd

    # 1-3. Tab-separated, quote-aware read (quoting is on by default, which
    # keeps the ID cells that contain a line break in one row). Skip the nine
    # junk lines, promote the complete header, keep only the ten real columns.
    df = pd.read_csv(io.StringIO(text), sep="\t",
                     skiprows=HEADER_LINES, header=0, dtype=str)
    df = df[COLUMNS]

    # 4. Drop the page-break rows: every "==== " divider and " PAGE 000n "
    # row is blank in Category; every real journal-entry row is not.
    df = df.dropna(subset=["Category"])
    df = df[df["Category"].str.strip() != ""]

    # 5. Amount: strip the padding spaces, remove the thousands commas,
    # convert to a real number. Credits keep their minus sign.
    df["Amount"] = (df["Amount"].str.strip()
                    .str.replace(",", "", regex=False)
                    .astype(float))

    # 6. ID: strip the surrounding whitespace, including the leading line
    # break on BeanCounter25's values.
    df["ID"] = df["ID"].str.strip()

    # 7. Count journal entries per user, largest first.
    counts = df.groupby("ID").size().sort_values(ascending=False)

    # 8. Write the two output files.
    df.to_csv(CLEANED_CSV, index=False, float_format="%.2f")
    (counts.rename("journal_entries").rename_axis("ID").reset_index()
           .to_csv(COUNTS_CSV, index=False))

    return {
        "entries": len(df),
        "users": df["ID"].nunique(),
        "accounts": df["Account"].nunique(),
        # + 0.0 turns a floating-point -0.0 residual into a plain 0.0
        "amount_net": round(float(df["Amount"].sum()), 2) + 0.0,
        "per_user": list(counts.items()),
    }


def clean_with_stdlib(text):
    """The standard-library path. Same operations, same output."""
    import csv
    from collections import Counter

    # 1-3. csv.reader with a tab delimiter and the default quote handling
    # keeps the quoted ID cells (which contain a line break) in one row.
    reader = csv.reader(io.StringIO(text), delimiter="\t", quotechar='"')
    rows = list(reader)[HEADER_LINES:]   # rows[0] is now the complete header

    cleaned = []
    for row in rows[1:]:
        # 4. Page-break rows: the ==== dividers and PAGE rows are blank in
        # Category (and the divider parses as a single cell).
        if len(row) < len(COLUMNS) or not row[1].strip():
            continue
        rec = row[:len(COLUMNS)]         # keep the ten real columns
        rec[4] = rec[4].strip()          # 6. ID: drop the leading line break
        amount = float(rec[9].strip().replace(",", ""))   # 5. Amount
        rec[9] = "%.2f" % amount
        cleaned.append((rec, amount))

    # 7. Count journal entries per user, largest first.
    counts = Counter(rec[4] for rec, _ in cleaned).most_common()

    # 8. Write the two output files.
    with open(CLEANED_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(COLUMNS)
        writer.writerows(rec for rec, _ in cleaned)
    with open(COUNTS_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["ID", "journal_entries"])
        writer.writerows(counts)

    return {
        "entries": len(cleaned),
        "users": len({rec[4] for rec, _ in cleaned}),
        "accounts": len({rec[0] for rec, _ in cleaned}),
        # + 0.0 turns a floating-point -0.0 residual into a plain 0.0
        "amount_net": round(sum(amount for _, amount in cleaned), 2) + 0.0,
        "per_user": counts,
    }


def print_summary(stats):
    """The descriptive summary the spec's Expected output section requires."""
    print("Lab 2 descriptive summary")
    print("  Journal entries:   {0:,}".format(stats["entries"]))
    print("  Distinct users:    {0}".format(stats["users"]))
    print("  Distinct accounts: {0}".format(stats["accounts"]))
    print("  Amount nets to:    {0:.2f}  (a balanced journal nets to 0.00)"
          .format(stats["amount_net"]))
    print("  Journal entries per user:")
    for user, n in stats["per_user"]:
        print("    {0:<16}{1:>8,}".format(user, n))
    print("Wrote " + CLEANED_CSV + " and " + COUNTS_CSV + ".")


def main():
    text = load_text()
    try:
        import pandas                    # noqa: F401  (path selection only)
        stats = clean_with_pandas(text)
        path_used = "pandas"
    except ImportError:
        stats = clean_with_stdlib(text)
        path_used = "standard library (pandas not installed)"
    print("Cleaning path: " + path_used)
    print_summary(stats)


if __name__ == "__main__":
    main()
