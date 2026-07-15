# Week 10 dataset — data dictionary

You have a folder of daily transaction files for a small retail chain, one file
per day, named `txn_YYYY-MM-DD.csv`. Each row is one sales transaction. The data
is synthetic teaching data, built to behave like a real point-of-sale export.
Stacked together, the files are a population of a few thousand transactions.

Your job is to build one **revenue journal entry** from all of the files, and to
write any odd records to a separate flagged file for review.

## Columns

| Column | Type | Meaning |
|---|---|---|
| `transaction_id` | text | Record id, normally unique. A couple are duplicated on purpose. |
| `date` | date | The transaction date. Normally matches the file name. A few are wrong on purpose. |
| `store_id` | text | Which store rang the sale (S01 through S05). |
| `sku` | text | Product code. |
| `product` | text | Product name. |
| `quantity` | number | Units sold. Normally 1 to 6. A few are negative (returns). |
| `unit_price` | number ($) | Price per unit. A few are 0 or 10x too high on purpose. |
| `amount` | number ($) | `quantity * unit_price`, rounded to the cent. |
| `tax` | number ($) | `amount * 0.0725` (a fixed 7.25% sales tax), rounded to the cent. |
| `payment_method` | text | cash, card, or online. |

## The tax rule

`tax = round(amount * 0.0725, 2)`. The tax rate is a fixed 7.25%. Gross (the
cash collected) is `amount + tax`. The revenue journal entry splits gross into
net revenue and sales tax payable:

- **Dr Cash** = total amount + total tax
- **Cr Sales Revenue** = total amount
- **Cr Sales Tax Payable** = total tax

The debit equals the sum of the two credits, so the entry balances.

## About the odd records

Some records are unusual on purpose: extreme amounts, negative amounts, zero
prices, duplicate ids, and bad dates. This is what real exported data looks like.

Two rules for the odd records:

1. **Keep them in the journal entry.** The entry is auto-created from every row,
   odd data included. Do not filter them out of the totals.
2. **Flag them anyway.** Write the odd records to `flagged_transactions.csv` so a
   reviewer can find them later if the entry has to be backed out and rebooked.

There are several defensible ways to find the odd records (percentiles, IQR,
z-score, duplicate checks, date-range checks). Pick a method, apply it, and write
a short note on what you did.
