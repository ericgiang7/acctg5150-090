# Summit Gear — customer accounts dataset

`summit_gear_customers.csv` — 2,200 business (B2B) customer accounts for Summit
Gear, a wholesale outdoor-equipment company. Each row is one account. The data is
synthetic teaching data, built to behave like a real accounts-receivable file.

You will use it two ways this week:

- **OLS (a number):** predict `days_to_pay` — how long an account takes to pay an
  invoice — from the account's attributes.
- **Logistic (yes/no):** predict `defaulted` — whether the account defaulted.

## Columns

| Column | Type | Meaning |
|---|---|---|
| `customer_id` | text | Unique account ID. An identifier, not a predictor. |
| `region` | category | Sales region: Mountain North, Mountain Central, Desert Southwest. |
| `segment` | category | Account segment: Outdoor Retail, School District, Resort, Outfitter. |
| `industry` | category | Account industry (Retail, Hospitality, Education, and so on). |
| `tenure_months` | number | Months the account has been active. |
| `credit_limit` | number ($) | The account's credit limit. |
| `avg_balance` | number ($) | Average outstanding balance. |
| `annual_spend` | number ($) | Total spend over the last 12 months. |
| `prior_late_count` | number | Count of prior invoices the account paid late. |
| `days_since_last_order` | number | Days since the account's most recent order. |
| `orders_per_year` | number | Orders the account places per year. |
| `discount_rate` | number (%) | Average discount rate offered to the account. |
| `avg_order_value` | number ($) | Average dollar value per order. |
| `noise_a` | number | An auxiliary field from the data export. |
| `noise_b` | number | An auxiliary field from the data export. |
| `days_to_pay` | number (days) | **OLS target.** Days from invoice to payment. |
| `defaulted` | 0/1 | **Logistic target.** 1 if the account defaulted, else 0. |

## Notes for the Excel work

- The two **target** columns are `days_to_pay` (the OLS exercise) and `defaulted`
  (the logistic exercise). Everything else is a candidate predictor.
- The three **category** columns (`region`, `segment`, `industry`) are text. To use
  one in a regression you encode it as dummy (0/1) columns and leave one level out
  as the base case — do not feed a 1-2-3 code.
- Not every numeric column is worth including. Part of the skill is deciding which
  predictors earn their place; more columns is not automatically a better model.
- The file has a header row and 2,200 data rows, a realistic size for Excel.
