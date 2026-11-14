"""Cleaning pipeline for the mobile-money agent network data."""
import pandas as pd


def clean_agent_data(txns, agents):
    """Clean raw agent transactions and merge them with the agent register.

    Parameters
    ----------
    txns : pandas.DataFrame
        Raw transactions with columns txn_id, agent_id, txn_type, amount, txn_date.
    agents : pandas.DataFrame
        Agent register with columns agent_id, county, onboarded.

    Returns
    -------
    clean_df : pandas.DataFrame
        One row per transaction with numeric amount, datetime txn_date, the
        agent county, and the flag columns amount_imputed, is_outlier and
        unknown_agent.
    log : pandas.DataFrame
        One row per cleaning rule applied: step, dimension, column, issue,
        rows_affected and action.
    """
    df = txns.copy()
    reg = agents.copy()
    log = []
    rows_in = len(df)

    def note(step, dimension, column, issue, rows, action):
        log.append({"step": step, "dimension": dimension, "column": column,
                    "issue": issue, "rows_affected": int(rows), "action": action})

    # 1. Keys: remove stray whitespace
    for col in ["txn_id", "agent_id"]:
        df[col] = df[col].astype(str).str.strip()
    reg["agent_id"] = reg["agent_id"].astype(str).str.strip()

    # 2. Consistency: standardise txn_type to exactly two values
    raw_type = df["txn_type"].astype(str)
    std_type = raw_type.str.strip().str.lower().map(
        {"deposit": "Deposit", "withdrawal": "Withdrawal"})
    fixed = ((raw_type != std_type) & std_type.notna()).sum()
    unrecognised = std_type.isna().sum()
    df["txn_type"] = std_type
    note(1, "Consistency", "txn_type", "Mixed case and trailing spaces", fixed,
         "Stripped spaces, lower-cased, mapped to Deposit / Withdrawal")
    note(1, "Validity", "txn_type", "Unrecognised transaction type", unrecognised,
         "Left as missing (none expected)")

    # 3. Consistency and validity: parse dates to ISO datetime
    raw_date = df["txn_date"].astype(str).str.strip()
    with_slash = raw_date.str.contains("/", regex=False).sum()
    df["txn_date"] = pd.to_datetime(
        raw_date.str.replace("/", "-", regex=False), format="%Y-%m-%d", errors="coerce")
    note(2, "Consistency", "txn_date", "Dates written with slashes", with_slash,
         "Replaced / with - and parsed to datetime")
    note(2, "Validity", "txn_date", "Dates that could not be parsed",
         df["txn_date"].isna().sum(), "Left as missing (none expected)")

    # 4. Validity and completeness: convert amount to numeric
    raw_amount = df["amount"]
    amount = pd.to_numeric(raw_amount, errors="coerce")
    text_values = (amount.isna() & raw_amount.notna()).sum()
    amount = amount.where(amount > 0)  # zero or negative amounts are invalid
    df["amount"] = amount
    note(3, "Validity", "amount", "Text in amount (for example 'N/A')", text_values,
         "Converted to numeric; invalid text became missing")
    note(3, "Completeness", "amount", "Missing amounts (blank or N/A)",
         df["amount"].isna().sum(), "Imputed in step 6 and flagged amount_imputed")

    # 5. Uniqueness: one row per txn_id, preferring a copy with a registered agent
    df["_known_agent"] = df["agent_id"].isin(reg["agent_id"])
    duplicates = df["txn_id"].duplicated().sum()
    df = (df.sort_values("_known_agent", ascending=False, kind="stable")
            .drop_duplicates(subset="txn_id", keep="first")
            .sort_index()
            .reset_index(drop=True)
            .drop(columns="_known_agent"))
    note(4, "Uniqueness", "txn_id", "Duplicate transactions (repeated txn_id)", duplicates,
         "Kept one row per txn_id, preferring the copy whose agent_id is registered")

    # 6. Merge with the agent register (left join keeps every transaction)
    reg["onboarded"] = pd.to_datetime(reg["onboarded"], errors="coerce")
    n_before = len(df)
    df = df.merge(reg[["agent_id", "county", "onboarded"]], on="agent_id",
                  how="left", validate="many_to_one")
    if len(df) != n_before:
        raise ValueError("Merge changed the number of transactions")
    df["unknown_agent"] = df["county"].isna()
    df["county"] = df["county"].fillna("Unknown")
    note(5, "Validity", "agent_id", "agent_id not in the agent register",
         df["unknown_agent"].sum(),
         "Kept (the money moved), county set to 'Unknown', flagged unknown_agent")
    note(5, "Timeliness", "txn_date", "Transactions dated before the agent was onboarded",
         (df["txn_date"] < df["onboarded"]).sum(), "Checked only (none expected)")

    # 7. Accuracy: flag IQR outliers; impute missing amounts with the median by type
    known = df["amount"].notna()
    q1, q3 = df.loc[known, "amount"].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    df["is_outlier"] = known & ((df["amount"] < low) | (df["amount"] > high))
    note(6, "Accuracy", "amount", f"IQR outliers (fences {low:,.0f} to {high:,.0f})",
         df["is_outlier"].sum(), "Flagged is_outlier, not removed")
    note(6, "Accuracy", "amount", "Amount of exactly 250,000",
         (df["amount"] == 250000).sum(),
         "Flagged as outliers; recommend verification before use")

    fill = (df.groupby("txn_type")["amount"].transform("median")
              .fillna(df["amount"].median()).round(0))
    df["amount_imputed"] = df["amount"].isna()
    df["amount"] = df["amount"].fillna(fill)
    note(6, "Completeness", "amount", "Missing amounts imputed",
         df["amount_imputed"].sum(),
         "Filled with the median amount of the same txn_type; flagged amount_imputed")

    columns = ["txn_id", "agent_id", "county", "txn_type", "amount", "txn_date",
               "amount_imputed", "is_outlier", "unknown_agent"]
    clean = df[columns].copy()
    note(7, "All", "all", "Rows removed overall", rows_in - len(clean),
         f"{rows_in} rows in, {len(clean)} rows out")
    return clean, pd.DataFrame(log)
