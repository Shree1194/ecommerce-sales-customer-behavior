"""Monthly cohort retention utilities."""

from __future__ import annotations

import pandas as pd


def build_monthly_cohort(orders: pd.DataFrame) -> pd.DataFrame:
    """Return customer monthly retention matrix by acquisition cohort."""
    required = {"customer_unique_id", "order_purchase_timestamp"}
    missing = required.difference(orders.columns)
    if missing:
        raise ValueError(f"Missing required columns for cohort analysis: {sorted(missing)}")

    df = orders.dropna(subset=["customer_unique_id", "order_purchase_timestamp"]).copy()
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")
    df["cohort_month"] = df.groupby("customer_unique_id")["order_month"].transform("min")
    df["cohort_index"] = (
        (df["order_month"].dt.year - df["cohort_month"].dt.year) * 12
        + (df["order_month"].dt.month - df["cohort_month"].dt.month)
    ) + 1

    cohort_counts = df.groupby(["cohort_month", "cohort_index"])["customer_unique_id"].nunique().unstack(fill_value=0)
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_sizes, axis=0).round(4)
    retention.index = retention.index.astype(str)
    return retention
