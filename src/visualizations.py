"""Generate portfolio-ready EDA charts from the analytical dataset."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from src.config import IMAGES_DIR


def save_core_visualizations(df: pd.DataFrame, output_dir: Path = IMAGES_DIR) -> None:
    """Save a focused set of executive charts used in README and reports."""
    output_dir.mkdir(parents=True, exist_ok=True)

    monthly = df.groupby("order_month", as_index=False)["revenue"].sum()
    fig = px.line(monthly, x="order_month", y="revenue", title="Monthly Revenue Trend")
    fig.write_html(output_dir / "monthly_revenue_trend.html")

    category = (
        df.groupby("product_category_name_english", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(15)
    )
    fig = px.bar(category, x="revenue", y="product_category_name_english", orientation="h", title="Top Categories by Revenue")
    fig.write_html(output_dir / "top_categories_revenue.html")

    state = df.groupby("customer_state", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(state, x="customer_state", y="revenue", title="Revenue by Customer State")
    fig.write_html(output_dir / "revenue_by_state.html")

    plt.figure(figsize=(10, 6))
    df["review_score"].dropna().hist(bins=5)
    plt.title("Review Score Distribution")
    plt.xlabel("Review Score")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.savefig(output_dir / "review_score_distribution.png", dpi=160)
    plt.close()

    save_extended_visualizations(df, output_dir)


def save_extended_visualizations(df: pd.DataFrame, output_dir: Path = IMAGES_DIR) -> None:
    """Export a broad EDA chart pack for portfolio review."""
    output_dir.mkdir(parents=True, exist_ok=True)

    chart_specs = [
        ("monthly_orders", ["order_month"], "order_id", "nunique", "bar", "Monthly Orders"),
        ("quarterly_revenue", ["order_quarter"], "revenue", "sum", "bar", "Quarterly Revenue"),
        ("revenue_by_city_top20", ["customer_city"], "revenue", "sum", "bar", "Top Cities by Revenue"),
        ("revenue_by_seller_top20", ["seller_id"], "revenue", "sum", "bar", "Top Sellers by Revenue"),
        ("top_products_revenue", ["product_id"], "revenue", "sum", "bar", "Top Products by Revenue"),
        ("worst_products_revenue", ["product_id"], "revenue", "sum", "bar_asc", "Lowest Revenue Products"),
        ("top_customers_clv", ["customer_unique_id"], "customer_lifetime_value", "max", "bar", "Top Customers by CLV"),
        ("repeat_customer_trend", ["order_month"], "repeat_customer_flag", "mean", "line", "Repeat Customer Share"),
        ("customer_growth", ["order_month"], "customer_unique_id", "nunique", "line", "Customer Growth"),
        ("daily_orders", ["order_purchase_timestamp"], "order_id", "nunique", "line", "Daily Orders"),
        ("avg_delivery_by_state", ["customer_state"], "delivery_days", "mean", "bar", "Delivery Days by State"),
        ("late_rate_by_state", ["customer_state"], "late_delivery_flag", "mean", "bar", "Late Delivery Rate by State"),
        ("payment_type_revenue", ["payment_type"], "revenue", "sum", "bar", "Revenue by Payment Type"),
        ("installment_orders", ["payment_installments"], "order_id", "nunique", "bar", "Orders by Installments"),
        ("freight_by_category", ["product_category_name_english"], "freight_value", "mean", "bar", "Freight by Category"),
        ("seller_performance_top20", ["seller_id"], "seller_performance_score", "mean", "bar", "Seller Performance Score"),
        ("review_by_category", ["product_category_name_english"], "review_score", "mean", "bar", "Review by Category"),
        ("aov_by_month", ["order_month"], "revenue", "mean", "line", "Average Item Revenue by Month"),
        ("profit_by_category", ["product_category_name_english"], "estimated_profit", "sum", "bar", "Estimated Profit by Category"),
        ("order_status_breakdown", ["order_status"], "order_id", "nunique", "bar", "Order Status Breakdown"),
        ("customer_distribution_state", ["customer_state"], "customer_unique_id", "nunique", "bar", "Customers by State"),
        ("seller_distribution_state", ["seller_state"], "seller_id", "nunique", "bar", "Sellers by State"),
        ("delivery_by_category", ["product_category_name_english"], "delivery_days", "mean", "bar", "Delivery by Category"),
        ("late_rate_by_category", ["product_category_name_english"], "late_delivery_flag", "mean", "bar", "Late Rate by Category"),
        ("revenue_by_year", ["order_year"], "revenue", "sum", "bar", "Revenue by Year"),
        ("freight_by_state", ["customer_state"], "freight_value", "sum", "bar", "Freight by State"),
        ("review_by_payment_type", ["payment_type"], "review_score", "mean", "bar", "Review by Payment Type"),
        ("profit_by_seller_top20", ["seller_id"], "estimated_profit", "sum", "bar", "Estimated Profit by Seller"),
        ("clv_by_state", ["customer_state"], "customer_lifetime_value", "mean", "bar", "Average CLV by State"),
    ]

    for filename, group_cols, value_col, agg_func, chart_type, title in chart_specs:
        if not set(group_cols + [value_col]).issubset(df.columns):
            continue
        plot_df = _aggregate_for_chart(df, group_cols, value_col, agg_func, chart_type)
        if plot_df.empty:
            continue
        x_col = group_cols[0]
        if chart_type == "line":
            fig = px.line(plot_df, x=x_col, y=value_col, title=title)
        else:
            fig = px.bar(plot_df, x=x_col, y=value_col, title=title)
        fig.write_html(output_dir / f"{filename}.html")

    if {"delivery_days", "review_score"}.issubset(df.columns):
        fig = px.scatter(
            df.dropna(subset=["delivery_days", "review_score"]).sample(
                min(len(df), 5000), random_state=42
            ),
            x="delivery_days",
            y="review_score",
            color="late_delivery_flag" if "late_delivery_flag" in df.columns else None,
            title="Delivery Days vs Review Score",
        )
        fig.write_html(output_dir / "delivery_vs_review_score.html")

    if {"customer_state", "product_category_name_english", "revenue"}.issubset(df.columns):
        heatmap_df = (
            df.groupby(["customer_state", "product_category_name_english"], as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
            .head(150)
        )
        fig = px.density_heatmap(
            heatmap_df,
            x="customer_state",
            y="product_category_name_english",
            z="revenue",
            title="State and Category Revenue Heatmap",
        )
        fig.write_html(output_dir / "state_category_revenue_heatmap.html")


def _aggregate_for_chart(
    df: pd.DataFrame,
    group_cols: list[str],
    value_col: str,
    agg_func: str,
    chart_type: str,
) -> pd.DataFrame:
    working = df.copy()
    if group_cols == ["order_purchase_timestamp"]:
        working["order_purchase_timestamp"] = working["order_purchase_timestamp"].dt.date

    grouped = working.groupby(group_cols, as_index=False).agg({value_col: agg_func})
    ascending = chart_type == "bar_asc"
    if chart_type.startswith("bar"):
        grouped = grouped.sort_values(value_col, ascending=ascending).head(20)
    return grouped
