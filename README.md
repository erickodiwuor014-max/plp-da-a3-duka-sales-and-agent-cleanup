# plp-da-a3-duka-sales-and-agent-cleanup

PLP Data Analytics, Week 3 assignment. Two engagements in one repository.

## Engagement 1: Duka Electronics sales exploration
Half-year (January to June 2026) analysis of 1,000 orders for the Head of Sales: inspection, derived columns, branch and product rankings, weekend versus weekday sales, best and worst month, Premium online orders from Nairobi and Mombasa, and a spreadsheet reconciliation.

**Executive Summary**
- Duka Electronics earned KES 71,792,500 from 1,000 orders between January and June 2026, an average of KES 71,793 per order.
- Nairobi is the largest branch with KES 26,106,100 (36.4% of revenue) from 376 orders, and all five branches rank the same by revenue and by orders.
- Laptops generate 57.9% of revenue (KES 41,535,000) even though tablets sell more units (691 against 639).
- Monthly revenue peaked at KES 13,518,300 in April and fell to KES 10,903,400 in June, a 24.0% gap between the best and worst month.
- Weekends bring in 27.8% of revenue, and a weekend day earns KES 383,390 against KES 405,127 on a weekday, only about 5% less.

## Engagement 2: Mobile money agent network
Audit, cleaning and summary of a deliberately flawed transaction extract (600 transactions intended, 20 agents, five counties). Cleaning rules are in `cleaning_pipeline.py` as `clean_agent_data(txns, agents)`, which returns `(clean_df, log)`.

**Agent data before and after cleaning**

| Stage | Rows |
|---|---|
| Raw `agent_transactions.csv` | 612 |
| Duplicate transactions removed (repeated `txn_id`) | 12 |
| Clean `agent_transactions_clean.csv` | 600 |

The agent register has 20 rows. Seven clean transactions belong to agent AG099, which is not in the register. They are kept, with county "Unknown" and `unknown_agent = True`. Five transactions of exactly KES 250,000 are flagged `is_outlier` and recommended for verification.

## Repository contents
| File | Purpose |
|---|---|
| `generate_data.py` | Both dataset generators (Duka, seed 2026; agents, seed 44) |
| `duka_sales_exploration.ipynb` | Engagement 1 notebook |
| `excel/duka_branch_summary.xlsx` | SUMIFS ranking, XLOOKUP region column, PivotTable by branch and channel |
| `outputs/premium_online_coast_capital.csv` | Premium online orders from Nairobi and Mombasa |
| `cleaning_pipeline.py` | `clean_agent_data()` |
| `agent_cleanup.ipynb` | Engagement 2 notebook with audit, summaries and Data Quality Report |
| `outputs/agent_transactions_clean.csv` | Clean agent transactions |
| `requirements.txt` | pandas, numpy, openpyxl |

## How to run
1. Install the libraries: `pip install -r requirements.txt`
2. Regenerate the data (the raw CSVs are not committed): `python generate_data.py`
   This creates `duka_sales.csv`, `agents.csv` and `agent_transactions.csv`.
3. Open `duka_sales_exploration.ipynb` and choose Restart kernel and Run all.
4. Open `agent_cleanup.ipynb` and choose Restart kernel and Run all. It imports `clean_agent_data` from `cleaning_pipeline.py`.

Both notebooks also work in Google Colab: they clone this repository and generate the data if the files are missing.
## Where to find each deliverable
| Requirement | Location |
|---|---|
| Duka Executive Summary (after title) | [duka_sales_exploration.ipynb](https://github.com/erickodiwuor014-max/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/duka_sales_exploration.ipynb) |
| Tasks 3 to 7 (branches, products, weekend, month, premium export) | same notebook, sections 3 to 7 |
| Premium online export | [outputs/premium_online_coast_capital.csv](https://github.com/erickodiwuor014-max/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/outputs/premium_online_coast_capital.csv) |
| Excel: SUMIFS, XLOOKUP, PivotTable | [excel/duka_branch_summary.xlsx](https://github.com/erickodiwuor014-max/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/excel/duka_branch_summary.xlsx) |
| Data generators (unchanged) | [generate_data.py](https://github.com/erickodiwuor014-max/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/generate_data.py) |
| Cleaning function | [cleaning_pipeline.py](https://github.com/erickodiwuor014-max/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/cleaning_pipeline.py) |
| Audit table, summaries, Data Quality Report with privacy paragraph | [agent_cleanup.ipynb](https://github.com/erickodiwuor014-max/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/agent_cleanup.ipynb) |
| Clean agent data | [outputs/agent_transactions_clean.csv](https://github.com/erickodiwuor014-max/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/outputs/agent_transactions_clean.csv) |
