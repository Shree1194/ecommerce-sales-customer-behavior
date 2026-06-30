"""Data cleaning routines for the Brazilian Olist e-commerce dataset."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import CURRENCY_COLUMNS, DATA_CLEANED, DATA_RAW, DATE_COLUMNS
from src.data_loader import load_raw_tables

logger = logging.getLogger(__name__)


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def _parse_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def _clean_currency(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").round(2)
            df[column] = df[column].clip(lower=0)
    return df


def clean_tables(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Clean every raw table while preserving the Olist relational keys."""
    cleaned = {name: _standardize_columns(df).drop_duplicates() for name, df in tables.items()}

    for name, columns in DATE_COLUMNS.items():
        cleaned[name] = _parse_dates(cleaned[name], columns)

    for name, columns in CURRENCY_COLUMNS.items():
        cleaned[name] = _clean_currency(cleaned[name], columns)

    cleaned["customers"] = cleaned["customers"].dropna(subset=["customer_id", "customer_unique_id"])
    cleaned["orders"] = cleaned["orders"].dropna(subset=["order_id", "customer_id"])
    cleaned["order_items"] = cleaned["order_items"].dropna(subset=["order_id", "product_id", "seller_id"])
    cleaned["sellers"] = cleaned["sellers"].dropna(subset=["seller_id"])
    cleaned["products"]["product_category_name"] = cleaned["products"]["product_category_name"].fillna("unknown")

    reviews = cleaned["reviews"]
    reviews["review_score"] = pd.to_numeric(reviews["review_score"], errors="coerce")
    reviews["review_score"] = reviews["review_score"].fillna(reviews["review_score"].median()).astype(int)
    reviews["review_comment_title"] = reviews["review_comment_title"].fillna("")
    reviews["review_comment_message"] = reviews["review_comment_message"].fillna("")
    cleaned["reviews"] = reviews

    geo = cleaned["geolocation"]
    geo = geo.dropna(subset=["geolocation_zip_code_prefix"])
    if {"geolocation_lat", "geolocation_lng"}.issubset(geo.columns):
        geo = geo.dropna(subset=["geolocation_lat", "geolocation_lng"])
        geo = geo[
            geo["geolocation_lat"].between(-35, 6)
            & geo["geolocation_lng"].between(-75, -30)
        ]
    cleaned["geolocation"] = geo.drop_duplicates(subset=["geolocation_zip_code_prefix"])

    return cleaned


def build_analytical_dataset(cleaned: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create an order-item level analytical dataset for BI and EDA."""
    order_items = cleaned["order_items"].copy()
    orders = cleaned["orders"].copy()
    customers = cleaned["customers"].copy()
    products = cleaned["products"].copy()
    sellers = cleaned["sellers"].copy()
    reviews = cleaned["reviews"].copy()
    payments = cleaned["payments"].copy()
    translations = cleaned["category_translation"].copy()

    products = products.merge(translations, on="product_category_name", how="left")
    products["product_category_name_english"] = products["product_category_name_english"].fillna(
        products["product_category_name"]
    )

    payment_summary = payments.groupby("order_id", as_index=False).agg(
        payment_value=("payment_value", "sum"),
        payment_installments=("payment_installments", "max"),
        payment_type=("payment_type", lambda values: values.mode().iat[0] if not values.mode().empty else np.nan),
    )

    review_summary = reviews.sort_values("review_answer_timestamp").groupby("order_id", as_index=False).agg(
        review_score=("review_score", "mean"),
        review_count=("review_id", "nunique"),
    )

    df = (
        order_items.merge(orders, on="order_id", how="left", validate="many_to_one")
        .merge(customers, on="customer_id", how="left", validate="many_to_one")
        .merge(products, on="product_id", how="left", validate="many_to_one")
        .merge(sellers, on="seller_id", how="left", validate="many_to_one")
        .merge(payment_summary, on="order_id", how="left", validate="many_to_one")
        .merge(review_summary, on="order_id", how="left", validate="many_to_one")
    )

    df["revenue"] = df["price"].fillna(0) + df["freight_value"].fillna(0)
    df["estimated_profit"] = (df["price"].fillna(0) * 0.18 - df["freight_value"].fillna(0) * 0.05).round(2)
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    df["order_quarter"] = df["order_purchase_timestamp"].dt.to_period("Q").astype(str)
    df["order_year"] = df["order_purchase_timestamp"].dt.year
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    df["shipping_delay"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days
    df["late_delivery_flag"] = df["shipping_delay"].gt(0).fillna(False).astype(int)

    customer_dates = df.groupby("customer_unique_id")["order_purchase_timestamp"].agg(
        first_purchase_date="min",
        last_purchase_date="max",
    )
    customer_order_counts = df.groupby("customer_unique_id")["order_id"].nunique().rename("customer_order_count")
    customer_clv = df.groupby("customer_unique_id")["revenue"].sum().rename("customer_lifetime_value")
    df = df.merge(customer_dates, on="customer_unique_id", how="left")
    df = df.merge(customer_order_counts, on="customer_unique_id", how="left")
    df = df.merge(customer_clv, on="customer_unique_id", how="left")
    df["repeat_customer_flag"] = df["customer_order_count"].gt(1).astype(int)

    seller_score = df.groupby("seller_id").agg(
        seller_avg_review=("review_score", "mean"),
        seller_late_rate=("late_delivery_flag", "mean"),
        seller_revenue=("revenue", "sum"),
    )
    seller_score["seller_performance_score"] = (
        seller_score["seller_avg_review"].fillna(0) * 20
        + (1 - seller_score["seller_late_rate"].fillna(1)) * 50
        + pd.qcut(seller_score["seller_revenue"].rank(method="first"), 10, labels=False, duplicates="drop").fillna(0) * 3
    ).round(2)
    df = df.merge(seller_score[["seller_performance_score"]], on="seller_id", how="left")

    return df


def save_outputs(cleaned: dict[str, pd.DataFrame], analytical: pd.DataFrame, output_dir: Path = DATA_CLEANED) -> None:
    """Persist cleaned tables and the main analytical table."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, df in cleaned.items():
        df.to_csv(output_dir / f"{name}_cleaned.csv", index=False)
    analytical.to_csv(output_dir / "olist_analytical_dataset.csv", index=False)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    tables = load_raw_tables(DATA_RAW)
    cleaned = clean_tables(tables)
    analytical = build_analytical_dataset(cleaned)
    save_outputs(cleaned, analytical)
    logger.info("Saved cleaned tables and analytical dataset to %s", DATA_CLEANED)


if __name__ == "__main__":
    main()
