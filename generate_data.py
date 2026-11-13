# =====================================================
# ENGAGEMENT 1: Duka Electronics (seed 2026)
# Writes duka_sales.csv
# =====================================================
# PYTHON · DATASET GENERATOR

import numpy as np

import pandas as pd



rng = np.random.default_rng(2026)

n = 1000

products = {"Phone": 15000, "Laptop": 65000, "Headphones": 2500,

            "Tablet": 28000, "Charger": 1200}



sales = pd.DataFrame({

    "order_id": range(1001, 1001 + n),

    "order_date": pd.to_datetime("2026-01-01")

                  + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),

    "branch": rng.choice(["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"], n,

                         p=[0.4, 0.2, 0.15, 0.15, 0.1]),

    "product": rng.choice(list(products), n),

    "quantity": rng.integers(1, 6, n),

    "channel": rng.choice(["In-store", "Online", "Phone order"], n,

                          p=[0.55, 0.35, 0.10]),

})

sales["unit_price"] = sales["product"].map(products)

sales.to_csv("duka_sales.csv", index=False)


# =====================================================
# ENGAGEMENT 2: Mobile money agent network (seed 44)
# Writes agents.csv and agent_transactions.csv
# =====================================================
import numpy as np, pandas as pd

rng = np.random.default_rng(44)

n = 600

agents = pd.DataFrame({

    "agent_id": [f"AG{i:03d}" for i in range(1, 21)],

    "county": rng.choice(["Nairobi", "Kiambu", "Nakuru", "Mombasa", "Kisumu"], 20),

    "onboarded": pd.date_range("2024-01-01", periods=20, freq="MS")

                   .strftime("%Y-%m-%d"),

})

txns = pd.DataFrame({

    "txn_id": [f"TX{i:05d}" for i in range(1, n + 1)],

    "agent_id": rng.choice(agents["agent_id"], n),

    "txn_type": rng.choice(["Deposit", "withdrawal", "DEPOSIT ",

                            "Withdrawal", "deposit"], n),

    "amount": rng.lognormal(7.5, 0.8, n).round(0).astype(str),

    "txn_date": (pd.to_datetime("2026-03-01")

                 + pd.to_timedelta(rng.integers(0, 60, n), unit="D"))

                .strftime("%Y-%m-%d"),

})

idx = rng.choice(n, 30, replace=False)

txns.loc[idx[:15], "amount"] = np.nan

txns.loc[idx[15:20], "amount"] = "N/A"

txns.loc[idx[20:25], "amount"] = "250000"

txns.loc[idx[25:], "txn_date"] = txns.loc[idx[25:], "txn_date"].str.replace("-", "/")

txns = pd.concat([txns, txns.sample(12, random_state=1)], ignore_index=True)

txns.loc[rng.choice(len(txns), 8, replace=False), "agent_id"] = "AG099"

agents.to_csv("agents.csv", index=False)

txns.to_csv("agent_transactions.csv", index=False)
