# Week 10 dataset — Automate a Journal Entry

Synthetic transaction data for the Week 10 lab. You build one revenue journal
entry from a folder of daily files, and you write any odd records to a separate
file for review.

## Files

| File | What it is |
|---|---|
| `transactions.zip` | The data. Unzip it to get a `transactions/` folder of ~100 daily CSVs. |
| `je_template.csv` | The journal-entry output format. Fill in debit and credit. |
| `flagged_transactions_template.csv` | The format for your outliers file, with two example rows. |
| `sample_journal_entry.csv` | A filled example on 3 made-up transactions, so you can see what "done" looks like. Not the answer. |
| `data_dictionary.md` | Column definitions, the tax rule, and how the odd records work. |
| `starter.ipynb` | A Colab starter notebook: it downloads and unzips the data and reads the folder, then leaves stubs for your work. |

## How to fetch

In Colab, open `starter.ipynb` and run it. It downloads the zip with:

    https://raw.githubusercontent.com/sean-mccaman/acctg5150-090/main/2026-summer/week-10/transactions.zip

then unzips it and reads every daily file into one DataFrame. You can also
download the zip by hand and load the folder with Excel Power Query.

## What you submit

Three files: your notebook (`.ipynb`), your `journal_entry.csv`, and your
`flagged_transactions.csv`.
