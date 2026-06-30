-- 60 interview-level SQL queries for the Olist portfolio project.
-- SQL dialect: PostgreSQL-style. Adjust date functions for BigQuery, MySQL, or SQL Server.

-- 01. Total revenue, orders, customers, and AOV.
SELECT COUNT(DISTINCT order_id) AS orders, COUNT(DISTINCT customer_unique_id) AS customers, SUM(revenue) AS revenue, SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0) AS aov FROM olist_analytical_dataset;

-- 02. Monthly revenue trend.
SELECT order_month, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY order_month ORDER BY order_month;

-- 03. Revenue by year and quarter.
SELECT order_year, order_quarter, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY order_year, order_quarter ORDER BY order_year, order_quarter;

-- 04. Top 10 product categories by revenue.
SELECT product_category_name_english, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY product_category_name_english ORDER BY revenue DESC LIMIT 10;

-- 05. Bottom 10 product categories with meaningful volume.
SELECT product_category_name_english, COUNT(DISTINCT order_id) AS orders, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY product_category_name_english HAVING COUNT(DISTINCT order_id) >= 50 ORDER BY revenue ASC LIMIT 10;

-- 06. Revenue by customer state.
SELECT customer_state, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY customer_state ORDER BY revenue DESC;

-- 07. Revenue by city within top states.
SELECT customer_state, customer_city, SUM(revenue) AS revenue, RANK() OVER (PARTITION BY customer_state ORDER BY SUM(revenue) DESC) AS city_rank FROM olist_analytical_dataset GROUP BY customer_state, customer_city;

-- 08. Top sellers by revenue.
SELECT seller_id, seller_state, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY seller_id, seller_state ORDER BY revenue DESC LIMIT 20;

-- 09. Seller performance score ranking.
SELECT seller_id, AVG(seller_performance_score) AS score, RANK() OVER (ORDER BY AVG(seller_performance_score) DESC) AS seller_rank FROM olist_analytical_dataset GROUP BY seller_id LIMIT 25;

-- 10. Average delivery days by state.
SELECT customer_state, AVG(delivery_days) AS avg_delivery_days FROM olist_analytical_dataset GROUP BY customer_state ORDER BY avg_delivery_days DESC;

-- 11. Late delivery rate by state.
SELECT customer_state, AVG(late_delivery_flag) AS late_delivery_rate FROM olist_analytical_dataset GROUP BY customer_state ORDER BY late_delivery_rate DESC;

-- 12. Review score distribution.
SELECT review_score, COUNT(DISTINCT order_id) AS orders FROM olist_analytical_dataset GROUP BY review_score ORDER BY review_score;

-- 13. Delivery speed impact on reviews.
SELECT CASE WHEN delivery_days <= 3 THEN '0-3 days' WHEN delivery_days <= 7 THEN '4-7 days' WHEN delivery_days <= 14 THEN '8-14 days' ELSE '15+ days' END AS delivery_bucket, AVG(review_score) AS avg_review_score, COUNT(DISTINCT order_id) AS orders FROM olist_analytical_dataset GROUP BY 1 ORDER BY MIN(delivery_days);

-- 14. Payment type mix.
SELECT payment_type, COUNT(DISTINCT order_id) AS orders, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY payment_type ORDER BY revenue DESC;

-- 15. Installment behavior.
SELECT payment_installments, COUNT(DISTINCT order_id) AS orders, AVG(revenue) AS avg_item_revenue FROM olist_analytical_dataset GROUP BY payment_installments ORDER BY payment_installments;

-- 16. Freight as percentage of revenue by category.
SELECT product_category_name_english, SUM(freight_value) / NULLIF(SUM(revenue), 0) AS freight_pct FROM olist_analytical_dataset GROUP BY product_category_name_english ORDER BY freight_pct DESC;

-- 17. Repeat customer share by month.
SELECT order_month, AVG(repeat_customer_flag) AS repeat_customer_share FROM olist_analytical_dataset GROUP BY order_month ORDER BY order_month;

-- 18. Customer lifetime value deciles.
WITH c AS (SELECT customer_unique_id, MAX(customer_lifetime_value) AS clv FROM olist_analytical_dataset GROUP BY customer_unique_id) SELECT NTILE(10) OVER (ORDER BY clv DESC) AS clv_decile, COUNT(*) AS customers, AVG(clv) AS avg_clv FROM c GROUP BY clv_decile ORDER BY clv_decile;

-- 19. Top customers by CLV.
SELECT customer_unique_id, MAX(customer_lifetime_value) AS clv, COUNT(DISTINCT order_id) AS orders FROM olist_analytical_dataset GROUP BY customer_unique_id ORDER BY clv DESC LIMIT 20;

-- 20. Daily order trend.
SELECT CAST(order_purchase_timestamp AS DATE) AS order_date, COUNT(DISTINCT order_id) AS orders FROM olist_analytical_dataset GROUP BY CAST(order_purchase_timestamp AS DATE) ORDER BY order_date;

-- 21. Weekly revenue trend.
SELECT DATE_TRUNC('week', order_purchase_timestamp) AS week_start, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY week_start ORDER BY week_start;

-- 22. Revenue moving average.
WITH m AS (SELECT order_month, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY order_month) SELECT order_month, revenue, AVG(revenue) OVER (ORDER BY order_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS revenue_3m_avg FROM m ORDER BY order_month;

-- 23. Month-over-month revenue growth.
WITH m AS (SELECT order_month, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY order_month) SELECT order_month, revenue, revenue - LAG(revenue) OVER (ORDER BY order_month) AS mom_change, (revenue / NULLIF(LAG(revenue) OVER (ORDER BY order_month), 0)) - 1 AS mom_growth FROM m ORDER BY order_month;

-- 24. Category revenue contribution.
SELECT product_category_name_english, SUM(revenue) AS revenue, SUM(revenue) / SUM(SUM(revenue)) OVER () AS revenue_share FROM olist_analytical_dataset GROUP BY product_category_name_english ORDER BY revenue DESC;

-- 25. Category rank by state.
SELECT customer_state, product_category_name_english, SUM(revenue) AS revenue, DENSE_RANK() OVER (PARTITION BY customer_state ORDER BY SUM(revenue) DESC) AS category_rank FROM olist_analytical_dataset GROUP BY customer_state, product_category_name_english;

-- 26. Products with high freight burden.
SELECT product_id, AVG(freight_value) AS avg_freight, AVG(price) AS avg_price, AVG(freight_value / NULLIF(price, 0)) AS freight_to_price FROM olist_analytical_dataset GROUP BY product_id HAVING COUNT(*) >= 10 ORDER BY freight_to_price DESC LIMIT 25;

-- 27. Canceled order revenue exposure.
SELECT order_status, COUNT(DISTINCT order_id) AS orders, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY order_status ORDER BY orders DESC;

-- 28. Sellers with poor reviews.
SELECT seller_id, COUNT(DISTINCT order_id) AS orders, AVG(review_score) AS avg_review FROM olist_analytical_dataset GROUP BY seller_id HAVING COUNT(DISTINCT order_id) >= 20 ORDER BY avg_review ASC LIMIT 20;

-- 29. Fastest sellers by delivery time.
SELECT seller_id, COUNT(DISTINCT order_id) AS orders, AVG(delivery_days) AS avg_delivery_days FROM olist_analytical_dataset GROUP BY seller_id HAVING COUNT(DISTINCT order_id) >= 20 ORDER BY avg_delivery_days ASC LIMIT 20;

-- 30. Slowest sellers by delivery time.
SELECT seller_id, COUNT(DISTINCT order_id) AS orders, AVG(delivery_days) AS avg_delivery_days FROM olist_analytical_dataset GROUP BY seller_id HAVING COUNT(DISTINCT order_id) >= 20 ORDER BY avg_delivery_days DESC LIMIT 20;

-- 31. Revenue by seller state to customer state lane.
SELECT seller_state, customer_state, COUNT(DISTINCT order_id) AS orders, SUM(revenue) AS revenue, AVG(delivery_days) AS avg_delivery_days FROM olist_analytical_dataset GROUP BY seller_state, customer_state ORDER BY revenue DESC;

-- 32. High-value delayed orders.
SELECT order_id, customer_unique_id, revenue, delivery_days, shipping_delay FROM olist_analytical_dataset WHERE late_delivery_flag = 1 ORDER BY revenue DESC LIMIT 50;

-- 33. Payment mix by category.
SELECT product_category_name_english, payment_type, COUNT(DISTINCT order_id) AS orders FROM olist_analytical_dataset GROUP BY product_category_name_english, payment_type;

-- 34. Average basket size.
SELECT AVG(items_per_order) AS avg_basket_size FROM (SELECT order_id, COUNT(*) AS items_per_order FROM olist_analytical_dataset GROUP BY order_id) x;

-- 35. Basket size by category.
SELECT product_category_name_english, AVG(items_per_order) AS avg_basket_size FROM (SELECT order_id, product_category_name_english, COUNT(*) AS items_per_order FROM olist_analytical_dataset GROUP BY order_id, product_category_name_english) x GROUP BY product_category_name_english ORDER BY avg_basket_size DESC;

-- 36. First purchase cohort size.
WITH firsts AS (SELECT customer_unique_id, MIN(order_month) AS cohort_month FROM olist_analytical_dataset GROUP BY customer_unique_id) SELECT cohort_month, COUNT(*) AS new_customers FROM firsts GROUP BY cohort_month ORDER BY cohort_month;

-- 37. Repeat purchase rate.
WITH c AS (SELECT customer_unique_id, COUNT(DISTINCT order_id) AS orders FROM olist_analytical_dataset GROUP BY customer_unique_id) SELECT AVG(CASE WHEN orders > 1 THEN 1.0 ELSE 0.0 END) AS repeat_purchase_rate FROM c;

-- 38. Customers at risk by last purchase.
WITH c AS (SELECT customer_unique_id, MAX(order_purchase_timestamp) AS last_purchase, SUM(revenue) AS clv FROM olist_analytical_dataset GROUP BY customer_unique_id) SELECT * FROM c WHERE last_purchase < (SELECT MAX(order_purchase_timestamp) - INTERVAL '180 days' FROM olist_analytical_dataset) ORDER BY clv DESC LIMIT 100;

-- 39. Revenue percentile by customer.
WITH c AS (SELECT customer_unique_id, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY customer_unique_id) SELECT customer_unique_id, revenue, PERCENT_RANK() OVER (ORDER BY revenue) AS revenue_percentile FROM c ORDER BY revenue DESC;

-- 40. Product rank within category.
SELECT product_category_name_english, product_id, SUM(revenue) AS revenue, ROW_NUMBER() OVER (PARTITION BY product_category_name_english ORDER BY SUM(revenue) DESC) AS product_rank FROM olist_analytical_dataset GROUP BY product_category_name_english, product_id;

-- 41. Products declining month over month.
WITH p AS (SELECT product_id, order_month, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY product_id, order_month) SELECT product_id, order_month, revenue, revenue - LAG(revenue) OVER (PARTITION BY product_id ORDER BY order_month) AS mom_change FROM p ORDER BY mom_change ASC NULLS LAST LIMIT 50;

-- 42. Review score trend by month.
SELECT order_month, AVG(review_score) AS avg_review_score FROM olist_analytical_dataset GROUP BY order_month ORDER BY order_month;

-- 43. Late delivery trend.
SELECT order_month, AVG(late_delivery_flag) AS late_delivery_rate FROM olist_analytical_dataset GROUP BY order_month ORDER BY order_month;

-- 44. On-time delivery by product category.
SELECT product_category_name_english, 1.0 - AVG(late_delivery_flag) AS on_time_rate FROM olist_analytical_dataset GROUP BY product_category_name_english ORDER BY on_time_rate ASC;

-- 45. Estimated profit by category.
SELECT product_category_name_english, SUM(estimated_profit) AS estimated_profit FROM olist_analytical_dataset GROUP BY product_category_name_english ORDER BY estimated_profit DESC;

-- 46. Margin proxy by category.
SELECT product_category_name_english, SUM(estimated_profit) / NULLIF(SUM(revenue), 0) AS estimated_margin FROM olist_analytical_dataset GROUP BY product_category_name_english ORDER BY estimated_margin DESC;

-- 47. Seller concentration.
WITH s AS (SELECT seller_id, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY seller_id) SELECT seller_id, revenue, SUM(revenue) OVER (ORDER BY revenue DESC) / SUM(revenue) OVER () AS cumulative_revenue_share FROM s ORDER BY revenue DESC;

-- 48. Category concentration.
WITH c AS (SELECT product_category_name_english, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY product_category_name_english) SELECT product_category_name_english, revenue, SUM(revenue) OVER (ORDER BY revenue DESC) / SUM(revenue) OVER () AS cumulative_revenue_share FROM c ORDER BY revenue DESC;

-- 49. High revenue, low review categories.
SELECT product_category_name_english, SUM(revenue) AS revenue, AVG(review_score) AS avg_review FROM olist_analytical_dataset GROUP BY product_category_name_english HAVING SUM(revenue) > 100000 AND AVG(review_score) < 4 ORDER BY revenue DESC;

-- 50. Best state-category combinations.
SELECT customer_state, product_category_name_english, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY customer_state, product_category_name_english ORDER BY revenue DESC LIMIT 50;

-- 51. LEFT JOIN example: orders missing reviews.
SELECT o.order_id FROM orders_cleaned o LEFT JOIN olist_analytical_dataset a ON o.order_id = a.order_id WHERE a.review_score IS NULL;

-- 52. INNER JOIN example: customer order revenue.
SELECT c.customer_unique_id, SUM(a.revenue) AS revenue FROM customers_cleaned c INNER JOIN olist_analytical_dataset a ON c.customer_id = a.customer_id GROUP BY c.customer_unique_id ORDER BY revenue DESC;

-- 53. RIGHT JOIN equivalent use case.
SELECT a.order_id, c.customer_unique_id FROM customers_cleaned c RIGHT JOIN olist_analytical_dataset a ON c.customer_id = a.customer_id WHERE c.customer_id IS NULL;

-- 54. FULL JOIN reconciliation.
SELECT COALESCE(o.order_id, a.order_id) AS order_id, CASE WHEN o.order_id IS NULL THEN 'missing_from_orders' WHEN a.order_id IS NULL THEN 'missing_from_analytical' ELSE 'matched' END AS status FROM orders_cleaned o FULL JOIN olist_analytical_dataset a ON o.order_id = a.order_id;

-- 55. Subquery: orders above average value.
SELECT order_id, SUM(revenue) AS order_value FROM olist_analytical_dataset GROUP BY order_id HAVING SUM(revenue) > (SELECT AVG(order_value) FROM (SELECT order_id, SUM(revenue) AS order_value FROM olist_analytical_dataset GROUP BY order_id) x);

-- 56. CTE for top category per state.
WITH ranked AS (SELECT customer_state, product_category_name_english, SUM(revenue) AS revenue, ROW_NUMBER() OVER (PARTITION BY customer_state ORDER BY SUM(revenue) DESC) AS rn FROM olist_analytical_dataset GROUP BY customer_state, product_category_name_english) SELECT * FROM ranked WHERE rn = 1;

-- 57. LEAD to compare next month revenue.
WITH m AS (SELECT order_month, SUM(revenue) AS revenue FROM olist_analytical_dataset GROUP BY order_month) SELECT order_month, revenue, LEAD(revenue) OVER (ORDER BY order_month) AS next_month_revenue FROM m ORDER BY order_month;

-- 58. LAG to detect delivery regression.
WITH m AS (SELECT order_month, AVG(delivery_days) AS avg_delivery_days FROM olist_analytical_dataset GROUP BY order_month) SELECT order_month, avg_delivery_days, avg_delivery_days - LAG(avg_delivery_days) OVER (ORDER BY order_month) AS delivery_days_change FROM m ORDER BY order_month;

-- 59. Dense rank sellers by state.
SELECT seller_state, seller_id, SUM(revenue) AS revenue, DENSE_RANK() OVER (PARTITION BY seller_state ORDER BY SUM(revenue) DESC) AS seller_state_rank FROM olist_analytical_dataset GROUP BY seller_state, seller_id;

-- 60. Create executive monthly KPI view.
CREATE VIEW vw_monthly_kpis AS SELECT order_month, COUNT(DISTINCT order_id) AS orders, COUNT(DISTINCT customer_unique_id) AS customers, SUM(revenue) AS revenue, SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0) AS aov, AVG(review_score) AS avg_review_score, 1.0 - AVG(late_delivery_flag) AS on_time_delivery_rate FROM olist_analytical_dataset GROUP BY order_month;
