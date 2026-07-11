# Oklahoma Purchase-Card (P-Card) Transactions, FY2022-FY2026

`pcard.parquet` is five fiscal years of Oklahoma state purchase-card transactions,
combined into one file for the Week 10 / HW 10 pattern-discovery work.

- **Rows:** 2,055,905 (FY2022 through FY2026)
- **Format:** Parquet (zstd), 35 MB. Read it with DuckDB or pandas; no download step needed.
- **Source:** Oklahoma OpenData, the state purchase-card program transparency files
  (`data.ok.gov`, packages `purchase-card-pcard-fiscal-year-YYYY`).
- **License:** Creative Commons Attribution 4.0 (CC BY 4.0). Data © State of Oklahoma;
  used with attribution.

## What was done to the raw files

- Combined the twelve monthly CSVs for each of the five fiscal years and tagged each
  row with `FISCAL_YEAR`.
- Dropped the cardholder name columns (`LAST_NAME`, `FIRST_INITIAL`). These are public
  record, but they add nothing to the analysis and are left out for cleanliness.
- Parsed `AMOUNT` to a number and `TRANSACTION_DATE` / `POST_DATE` to dates.

## Columns

| Column | Meaning |
|---|---|
| `FISCAL_YEAR` | Oklahoma fiscal year (Jul 1 to Jun 30) the file was published under |
| `CALENDAR_YEAR`, `CALENDAR_MONTH` | posting month (follows `POST_DATE`) |
| `AGENCYNBR`, `AGENCYNAME` | the state agency that made the purchase |
| `ITEM_DESCR` | free-text line description |
| `AMOUNT` | transaction amount in dollars (negatives are refunds/credits) |
| `MERCHANT` | the vendor |
| `TRANSACTION_DATE`, `POST_DATE` | when the purchase happened / when it posted |
| `MCC_DESCRIPTION` | merchant category (what kind of vendor) |

## Use it

DuckDB reads the hosted file directly, in Colab or in the browser:

```python
!pip install -q duckdb
import duckdb
URL = "https://raw.githubusercontent.com/sean-mccaman/acctg5150-090/main/2026-summer/week-10/pcard.parquet"
duckdb.sql(f"SELECT AGENCYNAME, SUM(AMOUNT) AS spend FROM '{URL}' GROUP BY 1 ORDER BY 2 DESC LIMIT 10").df()
```

pandas works too: `pandas.read_parquet(URL)`.
