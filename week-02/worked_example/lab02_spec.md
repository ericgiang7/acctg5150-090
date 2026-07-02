# Lab 02 Spec — Data Cleaning

The goal of this lab is to take one messy journal-entry export and get a trustworthy per-user count out of it two ways: once by hand in Excel, and once by writing a specification precise enough that an AI can build a Python script from it and land on the same number. The specification is the deliverable that gets graded on precision. Everything else in the lab checks that the specification actually worked.

## File manifest

- [x] lab_02_spec.md — this specification *(upload)*
- [x] Part 1 workbook, `.xlsx` — your by-hand cleaned workbook *(upload)*
- [x] lab_02_analysis.py — the script the AI builds from this spec *(upload)*
- [x] lab_02_explainer.html — the Part 3 explainer *(upload)*
- [x] lab_02_cleaned.csv — the cleaned dataset, written by the script
- [x] lab_02_user_counts.csv — the per-user count, written by the script

(Name each uploaded file so it starts with your university ID.)

## Build Requirements:

### Input

The file is `JEA Detail.txt`, a tab-separated text export of general ledger journal-entry detail for Company XYZ, dated as of 12/31/21. The script reads it from the public course copy at `https://raw.githubusercontent.com/sean-mccaman/acctg5150-090/main/week-02/JEA%20Detail.txt`, or from a copy of `JEA Detail.txt` saved in the same folder as the script.

The encoding is **UTF-16 LE**. VS Code shows `UTF-16 LE` in the status bar, and the file opens with the `FF FE` byte-order mark. An import that assumes UTF-8 fails on the first byte, before it reads a single row.

The ten real columns, in order, using the names on the complete header line: `Account`, `Category`, `Date`, `Period`, `ID`, `Manual`, `Description`, `Number`, `Location`, `Amount`. Every line also carries three empty trailing tab-separated cells that are not real columns.

The defects, exactly:

1. **A report header above the data.** Seven lines (the company name with `PAGE 0001`, the report date, blank lines, `GENERAL LEDGER DETAIL`, `AS OF 12/31/21`) followed by a `====` divider line.
2. **A two-line column header.** The upper line is partial (`Account`, `Post`, `User`, `Transaction` spread across cells); the lower line is the complete ten-name header. Only the lower line is the real header.
3. **Page-break rows scattered through the first few hundred rows.** Five page breaks, each one a line containing only ` PAGE 000n ` plus a `====` divider line, so ten junk lines in total. They do not repeat the column header.
4. **Quoted and spaced Amount values.** Every Amount is wrapped in double quotes with padding spaces and a thousands comma, for example `" 50,000.00 "`. Read naively, the column is text, not numbers. Credits carry a minus sign.
5. **A non-printing character in the ID column.** Every `ID` value for one user (`BeanCounter25`, 117 rows) begins with a line break inside the quoted cell. A line-by-line read splits each of those rows in two; a quote-aware read keeps the rows whole but leaves the stray character at the front of the value, so the label displays blank or misaligned.

### Operations

In order:

1. Read `JEA Detail.txt` with encoding `utf-16`, tab as the delimiter, and double-quote handling on, so the quoted `ID` cells that contain a line break stay together as one row.
2. Skip the first 9 lines: the seven report-header lines, the `====` divider, and the upper (partial) header line.
3. Use the next line, the complete ten-name header from `Account` through `Amount`, as the column header. Keep only those ten named columns and drop the empty trailing ones.
4. Remove the page-break rows: drop every row whose `Category` cell is blank. That removes the ` PAGE 000n ` lines and the `====` divider lines and nothing else, because every real journal-entry row has a `Category`.
5. Clean `Amount`: strip the padding spaces, remove the thousands commas, and convert the result to a number. Keep the minus sign on credits.
6. Clean `ID`: strip leading and trailing whitespace from every value, which removes the leading line break on `BeanCounter25`'s rows.
7. Count the journal entries per `ID`, sorted largest first.
8. Print the descriptive summary and write the two output files named in Expected output.

### Edge cases

- **The encoding.** The file is UTF-16 LE, not UTF-8. The script must be told `encoding="utf-16"` explicitly; a UTF-8 read fails immediately, and nothing in Python will detect the encoding for you the way Power Query did in Part 1.
- **The two-line header.** Keep only the lower, complete line. The upper partial line is removed with the report header in operation 2. If the upper line gets promoted instead, most column names come out blank and the rest of the spec cannot be carried out.
- **The page-break rows.** Five page breaks, each a ` PAGE 000n ` line plus a `====` line, ten junk rows total. Identify them by a blank `Category` cell, not by searching for the word `Account`: they do not repeat the column header. No row with a real `Category` may be dropped.
- **The quoted-and-spaced Amount values.** The `" 50,000.00 "` pattern. After operation 5, every `Amount` must parse as a number with no quotes, spaces, or commas left. Sanity check: the column nets to 0.00, because the journal balances.
- **The non-printing character in the ID column.** `BeanCounter25`'s 117 rows carry a line break at the front of the quoted `ID` cell. The read must be quote-aware (operation 1) so those rows are not split in two, and the strip in operation 6 must remove the character so the user appears exactly once in the per-user count, correctly labeled, with 117 entries. Space-only trimming does not remove it.

### Expected output

The script prints a descriptive summary — the total number of journal entries, the number of distinct users, the number of distinct accounts, and the count of journal entries per user — and writes two files: `lab_02_cleaned.csv` (the cleaned ten-column dataset) and `lab_02_user_counts.csv` (the per-user count).

## Review/Acceptance Criteria:

The per-user counts the script produces match the result you built by hand in Part 1, and `lab_02_cleaned.csv` passes the Lab 2 Output Validator with no issues.

## How this specification is graded

| Criterion | Pts |
|---|--:|
| Input — names the file, states its encoding, and lists every defect, precisely | 4 |
| Operations — every cleaning step is present and in the right order | 4 |
| Edge cases — each trap is named, with what the script should do about it | 4 |
| Expected output and Review/Acceptance — both stated; the whole spec is specific, no vague verbs | 3 |
| **Total** | **15** |

## Self-assessment

### Submission Gate Checklist

- [x] **SG-01 File Availability [OK]:** Every file in the manifest is produced and the four upload files are ready for the Lab 2 quiz.
  - Evidence: The workbook, this spec, the script, and the explainer all exist; the script writes both CSVs on every run. This is the instructor's worked copy, so the files carry no uID prefix; a student submission must add one to each uploaded file.
- [x] **SG-02 Specification Complete [OK]:** Input, Operations, and Edge cases are all filled in, specific, in order, with no vague verbs.
  - Evidence: Input names the file, the UTF-16 LE encoding, the ten columns, and all five defects; Operations is eight numbered steps in execution order; Edge cases names each of the five traps with the exact behavior required.
- [x] **SG-03 Output Matches the By-Hand Result [OK]:** The script's per-user count matches the count produced by hand in Part 1.
  - Evidence: Both show Automated 23,495, BeanCounter25 117, Laura4 78, Bob2 76, Karen15 70, CFO2 25, Kayla 2, total 23,863. The script matched on the first run because the spec named the encoding, the page-break test, and the ID strip before the script was built.
- [x] **SG-04 Validator Clean [OK]:** The Lab 2 Output Validator reports no issues on `lab_02_cleaned.csv`.
  - Evidence: 23,863 data rows, 10 columns, no leftover header or page-break rows, the Amount column all clean numbers, the ID column free of stray characters.
- [x] **SG-05 File Extensions [OK]:** Each file uses the correct extension (`.md`, `.xlsx`, `.py`, `.csv`, `.html`); the `.md` and `.py` files render as plain text.
  - Evidence: Checked each file in VS Code; the spec renders in Markdown preview and the script opens as plain Python source.

**Blocking Issues (if any):**
- None.

**Final Gate Decision:**
- [x] Ready to submit
- [ ] Not ready - fixes required
