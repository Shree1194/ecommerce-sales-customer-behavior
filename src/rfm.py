"""RFM segmentation for customer retention analysis."""

from __future__ import annotations

import pandas as pd


def build_rfm(orders: pd.DataFrame, snapshot_date: pd.Timestamp | None = None) -> pd.DataFrame:
    """Calculate Recency, Frequency, Monetary metrics and customer segments."""
    required = {"customer_unique_id", "order_id", "order_purchase_timestamp", "revenue"}
    missing = required.difference(orders.columns)
    if missing:
        raise ValueError(f"Missing required columns for RFM: {sorted(missing)}")

    df = orders.dropna(subset=["customer_unique_id", "order_purchase_timestamp"]).copy()
    snapshot = snapshot_date or df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("customer_unique_id").agg(
        recency=("order_purchase_timestamp", lambda values: (snapshot - values.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("revenue", "sum"),
    )

    rfm["r_score"] = pd.qcut(rfm["recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["rfm_score"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)
    rfm["segment"] = rfm.apply(_segment_customer, axis=1)
    return rfm.reset_index()


def _segment_customer(row: pd.Series) -> str:
    if row["r_score"] >= 4 and row["f_score"] >= 4 and row["m_score"] >= 4:
        return "Champions"
    if row["f_score"] >= 4 and row["m_score"] >= 3:
        return "Loyal Customers"
    if row["r_score"] >= 4 and row["f_score"] >= 2:
        return "Potential Loyalists"
    if row["r_score"] == 5 and row["f_score"] <= 2:
        return "New Customers"
    if row["r_score"] <= 2 and row["f_score"] >= 3:
        return "At Risk"
    if row["r_score"] <= 2 and row["f_score"] <= 2:
        return "Lost Customers"
    return "Needs Attention"
