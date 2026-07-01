# Project 2 — Credit Default Data

Consumer-lending dataset for **Project 2 (Predicting Credit Default)**. 29,881
customer account records. It contains **no personally identifiable information**;
the columns are normalized and recoded, and it is adapted from public
credit-default research data for teaching use.

## Files

- `ar_default_data.csv` — the data as CSV (for pandas or Excel)
- `ar_default.sqlite` — the same data as a SQLite database (one table, `accounts`),
  for SQL tools or the in-browser explorer

## Load it in pandas

```python
import pandas as pd
url = "https://raw.githubusercontent.com/sean-mccaman/acctg5150-090/main/2026-summer/project-2/ar_default_data.csv"
df = pd.read_csv(url)
df.head()
```

## Columns

| Column | Description | Type | Role |
|---|---|---|---|
| `bad_ar` | Did the customer default next month (1 = yes, 0 = paid) | INTEGER | Target |
| `credit_limit` | Normalized credit limit extended (higher = more credit) | REAL | Feature |
| `outstanding_balance` | Normalized current balance owed | REAL | Feature |
| `pay_this_month` | Payment status this month (0 = on time, 1-3 = months behind) | INTEGER | Feature |
| `no_activity_this_month` | No payment activity this month (0 = active, 1 = inactive) | INTEGER | Feature |
| `last_payment_portion` | Fraction of the balance paid last cycle | REAL | Feature |
| `num_recent_payments` | Count of payments in recent months (0-6) | INTEGER | Feature |
| `gender` | Customer gender | TEXT | Demographic |
| `education` | Education level (graduate, university, high school, other) | TEXT | Demographic |
| `marital_status` | Marital status (married, single, other) | TEXT | Demographic |
| `age_decile` | Age group (20, 30, 40, 50, 60, 70) | INTEGER | Demographic |

## Notes

- The target `bad_ar` is imbalanced: about **22%** of accounts default. A model
  that predicts "everyone pays" is already ~78% accurate and useless, which is why
  Project 2 judges the model on precision, recall, and cost rather than accuracy.
- The four demographic columns (`gender`, `education`, `marital_status`,
  `age_decile`) are included so you can examine whether they *should* be used. They
  barely improve the model, and using them in a real credit decision raises serious
  fair-lending questions under the Equal Credit Opportunity Act (ECOA). See the
  project guide for how to treat this.
- In the SQLite database, all rows live in one table named `accounts`.
