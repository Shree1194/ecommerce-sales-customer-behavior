"""One-command project pipeline."""

from __future__ import annotations

import logging

import pandas as pd

from src.cleaning import build_analytical_dataset, clean_tables, save_outputs
from src.config import DATA_CLEANED, DATA_RAW
from src.cohort import build_monthly_cohort
from src.data_loader import load_raw_tables
from src.rfm import build_rfm
from src.visualizations import save_core_visualizations


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    tables = load_raw_tables(DATA_RAW)
    cleaned = clean_tables(tables)
    analytical = build_analytical_dataset(cleaned)
    save_outputs(cleaned, analytical)
    save_core_visualizations(analytical)

    order_level = analytical.drop_duplicates("order_id").copy()
    rfm = build_rfm(analytical)
    cohort = build_monthly_cohort(order_level)
    rfm.to_csv(DATA_CLEANED / "rfm_segments.csv", index=False)
    cohort.to_csv(DATA_CLEANED / "monthly_cohort_retention.csv")

    pd.DataFrame(
        {
            "metric": ["total_revenue", "total_orders", "aov", "on_time_delivery_pct", "avg_review_score"],
            "value": [
                analytical["revenue"].sum(),
                analytical["order_id"].nunique(),
                analytical.groupby("order_id")["revenue"].sum().mean(),
                1 - order_level["late_delivery_flag"].mean(),
                order_level["review_score"].mean(),
            ],
        }
    ).to_csv(DATA_CLEANED / "executive_kpis.csv", index=False)


if __name__ == "__main__":
    main()
