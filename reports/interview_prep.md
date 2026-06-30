# Interview Preparation

## Project Explanation

I built an end-to-end e-commerce analytics project using the Brazilian Olist marketplace dataset. The work covers data cleaning, feature engineering, SQL analysis, RFM segmentation, cohort retention, dashboard design, and executive business recommendations. The final model converts nine raw marketplace tables into a BI-ready analytical dataset at the order-item grain while preserving customer, seller, product, payment, review, and delivery context.

## 60 SQL Interview Questions

1. Explain the difference between `INNER JOIN` and `LEFT JOIN`.
2. When would you use a `FULL JOIN` in data reconciliation?
3. How do you find duplicate orders in SQL?
4. How do you calculate monthly revenue?
5. How do you calculate AOV?
6. How do `WHERE` and `HAVING` differ?
7. How does `COUNT(*)` differ from `COUNT(column)`?
8. How do you rank sellers by revenue?
9. Explain `ROW_NUMBER`, `RANK`, and `DENSE_RANK`.
10. How do you calculate month-over-month growth?
11. What is a CTE and why use one?
12. How do window functions differ from aggregate queries?
13. How do you calculate repeat purchase rate?
14. How do you identify at-risk customers?
15. How do you detect missing foreign keys?
16. How do you handle nulls in revenue calculations?
17. How do you calculate percent contribution by category?
18. How would you create a cohort table in SQL?
19. What is `PARTITION BY`?
20. Explain `LEAD` and `LAG`.
21. How do you find top N products per category?
22. How do you optimize slow analytical queries?
23. What indexes would help this project?
24. What is a view?
25. What is a materialized view?
26. How do you validate row counts after joins?
27. What causes fanout in joins?
28. How do you prevent double-counting revenue?
29. How do you calculate delivery delay?
30. How do you bucket delivery days?
31. How do you calculate late delivery rate?
32. How do you compare seller performance?
33. How do you find customers above average CLV?
34. How do you calculate rolling revenue?
35. How do you calculate cumulative revenue share?
36. How do you identify revenue concentration risk?
37. How do you reconcile raw and cleaned tables?
38. How do you remove duplicate records?
39. How do you use `CASE` for segmentation?
40. What are correlated subqueries?
41. How do you choose between joins and subqueries?
42. What is query execution order?
43. What are primary and foreign keys?
44. How do you handle slowly changing dimensions?
45. What is grain in a fact table?
46. How do you document SQL assumptions?
47. How do you test a KPI query?
48. How do you handle time zones?
49. How do you calculate retention?
50. How do you identify churn risk?
51. What is a star schema?
52. How do you design a sales fact table?
53. How do you use `NTILE`?
54. How do you find outliers in SQL?
55. How do you calculate median if supported?
56. How do you debug incorrect totals?
57. How do you build an executive KPI view?
58. How do you compare category performance across states?
59. How do you handle unsupported `FULL JOIN` dialects?
60. How would you explain a complex SQL project to a non-technical stakeholder?

## Python Interview Questions

- How did you structure the data cleaning pipeline?
- Why use functions and modules instead of one notebook?
- How do you handle invalid dates in pandas?
- How do you avoid chained assignment issues?
- How do you validate expected input files?
- How do you prevent duplicate rows after merges?
- What is the difference between `merge`, `join`, and `concat`?
- How do you profile missing values?
- How do you save reproducible analytical outputs?
- How would you productionize this project further?

## Power BI Interview Questions

- What pages did you design and why?
- Which DAX measures are required for executive KPIs?
- How would you set up slicers and drill-through?
- How do you avoid overloading an executive dashboard?
- How would you model RFM segments in Power BI?
- How would you optimize dashboard performance?
- How do bookmarks and tooltip pages improve usability?

## Statistics Questions

- How would you test whether delivery speed affects review scores?
- What is correlation and what are its limitations?
- How would you identify outliers in freight cost?
- What is cohort retention?
- What is selection bias?
- How would you compare review scores across seller groups?

## Business Case Questions

- Revenue is growing but reviews are declining. What do you investigate?
- A top category has high cancellations. What actions do you recommend?
- Delivery delays are concentrated in one region. How do you respond?
- Repeat purchase rate is low. What lifecycle strategy would you propose?
- Freight costs are increasing faster than revenue. What should leadership do?

## HR Questions

- Tell me about yourself.
- Why are you interested in data analyst roles?
- Why this company?
- Tell me about a time you handled ambiguous data.
- Tell me about a time you influenced a stakeholder.
- Tell me about a time you found an unexpected insight.
- Describe a time you had to meet a tight deadline.
- What is your biggest strength as an analyst?
- What is one area you are improving?
- Why should we hire you?

## STAR Answers

**Situation:** The raw marketplace data was split across customers, orders, products, sellers, payments, reviews, and geolocation files.

**Task:** Build a BI-ready analytics project that identifies revenue drivers and customer experience risks.

**Action:** I created a modular Python pipeline, cleaned each table, engineered delivery and customer lifecycle features, wrote SQL KPI queries, built RFM and cohort models, and designed a Power BI dashboard blueprint.

**Result:** The project produces reusable cleaned datasets, executive KPIs, customer segments, retention outputs, and business recommendations suitable for stakeholder review and analyst interviews.
