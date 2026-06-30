# Power BI Dashboard Blueprint

## Theme

Use a dark executive retail theme:

- Background: `#101418`
- Visual surface: `#1B2229`
- Primary accent: `#2FBF71`
- Secondary accent: `#F5A623`
- Alert: `#E15554`
- Text: `#F4F7F9`

## Data Model

Import these cleaned outputs:

- `olist_analytical_dataset.csv`
- `rfm_segments.csv`
- `monthly_cohort_retention.csv`
- `executive_kpis.csv`

Recommended relationships:

- `olist_analytical_dataset[customer_unique_id]` to `rfm_segments[customer_unique_id]`
- Date table to `olist_analytical_dataset[order_purchase_timestamp]`

## Core DAX Measures

```DAX
Total Revenue = SUM(olist_analytical_dataset[revenue])
Total Orders = DISTINCTCOUNT(olist_analytical_dataset[order_id])
Active Customers = DISTINCTCOUNT(olist_analytical_dataset[customer_unique_id])
AOV = DIVIDE([Total Revenue], [Total Orders])
Average Review Score = AVERAGE(olist_analytical_dataset[review_score])
On-Time Delivery % = 1 - AVERAGE(olist_analytical_dataset[late_delivery_flag])
Repeat Customer % = AVERAGE(olist_analytical_dataset[repeat_customer_flag])
Estimated Profit = SUM(olist_analytical_dataset[estimated_profit])
```

## Pages

1. Executive Overview
   - KPI cards: revenue, orders, AOV, retention, on-time delivery, review score
   - Monthly revenue trend
   - Revenue by state map
   - Top category and seller tables

2. Sales Dashboard
   - Revenue by month, quarter, state, city, category
   - Average basket size and order value
   - Payment and installment analysis

3. Customer Dashboard
   - Customer growth
   - Repeat customer rate
   - CLV distribution
   - Top customers

4. Seller Dashboard
   - Seller performance score
   - Late delivery rate
   - Review score by seller
   - Revenue concentration

5. Product Dashboard
   - Top and bottom products
   - Category margin proxy
   - Freight burden
   - Review by category

6. Delivery Dashboard
   - Delivery days distribution
   - State-wise delivery performance
   - Shipping delay heatmap
   - Slow seller lanes

7. RFM Dashboard
   - Segment count and revenue
   - Champions and at-risk customers
   - Segment recommendations
   - Cohort retention heatmap

## Interactions

- Global slicers: date, state, category, seller, payment type
- Drill-through: seller detail and customer segment detail
- Tooltip pages: category detail and delivery lane detail
- Bookmarks: revenue view, profit view, logistics view
- Dynamic titles driven by selected date and category
