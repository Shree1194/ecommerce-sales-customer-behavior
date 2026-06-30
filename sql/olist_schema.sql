-- Analytical schema for cleaned Olist CSV exports.
-- Load data/cleaned/*.csv into equivalent tables before running queries.

CREATE TABLE customers_cleaned (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix INTEGER,
    customer_city TEXT,
    customer_state TEXT
);

CREATE TABLE orders_cleaned (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE order_items_cleaned (
    order_id TEXT,
    order_item_id INTEGER,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TIMESTAMP,
    price NUMERIC(12, 2),
    freight_value NUMERIC(12, 2)
);

CREATE TABLE olist_analytical_dataset (
    order_id TEXT,
    customer_id TEXT,
    customer_unique_id TEXT,
    product_id TEXT,
    seller_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_month TEXT,
    order_quarter TEXT,
    order_year INTEGER,
    customer_city TEXT,
    customer_state TEXT,
    seller_city TEXT,
    seller_state TEXT,
    product_category_name_english TEXT,
    price NUMERIC(12, 2),
    freight_value NUMERIC(12, 2),
    revenue NUMERIC(12, 2),
    estimated_profit NUMERIC(12, 2),
    payment_type TEXT,
    payment_installments INTEGER,
    review_score NUMERIC(4, 2),
    delivery_days INTEGER,
    shipping_delay INTEGER,
    late_delivery_flag INTEGER,
    repeat_customer_flag INTEGER,
    customer_lifetime_value NUMERIC(12, 2),
    seller_performance_score NUMERIC(8, 2)
);

CREATE VIEW vw_order_kpis AS
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS active_customers,
    SUM(revenue) AS total_revenue,
    SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0) AS average_order_value,
    AVG(review_score) AS average_review_score,
    1.0 - AVG(late_delivery_flag) AS on_time_delivery_rate
FROM olist_analytical_dataset;
