# Business Insights

This report is generated from the cleaned Olist analytical dataset after running:

```bash
python -m src.run_pipeline
```

## Executive Narrative

The project evaluates how revenue, customer retention, product mix, sellers, reviews, payments, and delivery performance interact in a multi-seller e-commerce marketplace. The business goal is to identify where growth is concentrated, where customer experience breaks down, and which actions would improve revenue quality.

## Key Questions Answered

1. Which product categories generate the highest revenue?
2. Which products and categories underperform despite meaningful order volume?
3. Which states and cities contribute the most revenue?
4. Which sellers deliver fastest and receive strong reviews?
5. Which sellers create customer experience risk through late delivery or poor reviews?
6. Does delivery speed affect customer ratings?
7. Which customers should be retained using lifecycle marketing?
8. Which regions need logistics improvement?
9. What drives repeat purchases?
10. What actions could increase revenue?

## Recommended Actions

- Prioritize inventory, placement, and paid campaigns for high-revenue categories with strong review scores.
- Create seller quality scorecards using revenue, review score, late delivery rate, and cancellation exposure.
- Improve logistics in states with high revenue but above-average delivery delays.
- Retarget at-risk high-CLV customers with category-specific offers.
- Reduce freight burden for products where freight is a large share of the order value.
- Investigate categories with strong revenue but weak reviews before scaling demand further.

## RFM Segment Playbook

- Champions: early access, loyalty benefits, referral incentives.
- Loyal Customers: subscription-style reminders, bundles, category cross-sell.
- Potential Loyalists: second-purchase coupons and personalized recommendations.
- New Customers: onboarding sequence, trust-building delivery updates.
- At Risk: win-back campaigns based on previous category affinity.
- Lost Customers: low-cost reactivation only when historical CLV supports it.
