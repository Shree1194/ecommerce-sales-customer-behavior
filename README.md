# E-Commerce Sales & Customer Behavior Analysis

Production-style data analyst portfolio project using the Brazilian Olist e-commerce dataset. The project turns nine raw marketplace CSV files into cleaned analytical datasets, SQL KPIs, customer segments, cohort retention tables, executive dashboard specifications, and interview-ready business insights.

## Business Problem

Marketplace leaders need to understand which products, sellers, regions, and customer segments drive profitable growth. They also need to identify where late deliveries, weak reviews, freight costs, and low repeat purchase rates create risk.

## Dataset

Source: Brazilian E-Commerce Public Dataset by Olist from Kaggle.

Expected files:

- customers
- orders
- order items
- payments
- reviews
- products
- sellers
- geolocation
- product category translation

Raw data is not committed. Place the CSVs in `data/raw`.

## Architecture

```text
data/raw CSVs
    -> src.data_loader validates source files
    -> src.cleaning standardizes and cleans each table
    -> src.cleaning builds order-item analytical dataset
    -> src.rfm creates customer segments
    -> src.cohort creates monthly retention matrix
    -> src.visualizations exports core EDA charts
    -> Power BI consumes cleaned CSV outputs
```

## Project Structure

```text
E-Commerce/
|-- data/
|   |-- raw/
|   `-- cleaned/
|-- notebooks/
|-- sql/
|-- src/
|-- dashboard/
|-- reports/
|-- images/
|-- README.md
|-- requirements.txt
`-- .gitignore
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Add the Kaggle CSV files to `data/raw`, then run:

```bash
python -m src.run_pipeline
```

## Outputs

The pipeline writes:

- `data/cleaned/*_cleaned.csv`
- `data/cleaned/olist_analytical_dataset.csv`
- `data/cleaned/rfm_segments.csv`
- `data/cleaned/monthly_cohort_retention.csv`
- `data/cleaned/executive_kpis.csv`
- chart files in `images/`

## Feature Engineering

Key engineered columns include:

- order month, quarter, and year
- delivery days
- shipping delay
- late delivery flag
- revenue
- estimated profit
- customer lifetime value
- first and last purchase date
- repeat customer flag
- seller performance score

## KPIs

- Total Revenue
- Total Orders
- Average Order Value
- Active Customers
- Repeat Customer Rate
- On-Time Delivery %
- Average Review Score
- Estimated Profit
- Customer Lifetime Value

## Analysis Modules

- Data cleaning and validation: `src/cleaning.py`
- RFM segmentation: `src/rfm.py`
- Cohort retention: `src/cohort.py`
- Visual exports: `src/visualizations.py`
- One-command pipeline: `src/run_pipeline.py`

## SQL

The `sql` folder contains:

- schema and KPI view definitions
- 60 interview-level SQL queries covering joins, CTEs, window functions, ranking, subqueries, revenue KPIs, seller performance, delivery performance, and retention analysis

## Dashboard

The Power BI blueprint includes:

- Executive Overview
- Sales Dashboard
- Customer Dashboard
- Seller Dashboard
- Product Dashboard
- Delivery Dashboard
- RFM Dashboard

See `dashboard/power_bi_dashboard_blueprint.md`.

## Business Insights

The project is designed to answer:

- Which product categories generate the highest revenue?
- Which products underperform?
- Which states contribute the most revenue?
- Which sellers deliver fastest?
- Which sellers receive poor reviews?
- Does delivery speed affect customer ratings?
- Which customers should be retained?
- Which regions need logistics improvement?
- What drives repeat purchases?
- What actions could increase revenue?

See `reports/business_insights.md`.

## Interview Preparation

The `reports` folder includes SQL, Python, Power BI, statistics, business case, HR-style project explanation, resume bullets, LinkedIn copy, GitHub description, and a portfolio case study.

## Future Improvements

- Add automated data quality tests with Great Expectations or pandera.
- Load cleaned outputs into PostgreSQL or BigQuery.
- Publish a Power BI `.pbix` file after local data refresh.
- Add forecasting for monthly revenue and delivery demand.
- Add customer propensity modeling for repeat purchases.
