import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
N = 10000

def generate_churnlens_data():
    print("Generating ChurnLens e-commerce dataset...")

    # ── Customer base ─────────────────────────────────────────
    customer_ids = [f"CUST_{str(i).zfill(5)}" for i in range(1, N+1)]

    signup_dates = [
        datetime(2022, 1, 1) + timedelta(days=np.random.randint(0, 730))
        for _ in range(N)
    ]

    ages        = np.random.choice([18,25,35,45,55], N, p=[0.15,0.30,0.30,0.15,0.10])
    genders     = np.random.choice(["Male","Female","Other"], N, p=[0.48,0.48,0.04])
    city_tiers  = np.random.choice([1, 2, 3], N, p=[0.30, 0.45, 0.25])
    devices     = np.random.choice(["Mobile","Desktop","Tablet"], N, p=[0.60,0.30,0.10])
    categories  = np.random.choice(
        ["Electronics","Fashion","Grocery","Beauty","Sports","Home"],
        N, p=[0.20,0.25,0.20,0.15,0.10,0.10]
    )

    # ── Behavioural signals ───────────────────────────────────
    tenure_days          = np.array([(datetime.today() - sd).days for sd in signup_dates])
    total_orders         = np.random.negative_binomial(5, 0.4, N).clip(1, 60)
    avg_order_value      = np.random.lognormal(mean=7.5, sigma=0.8, size=N).clip(100, 15000)
    days_since_last_order= np.random.exponential(scale=40, size=N).astype(int).clip(1, 365)
    return_rate          = np.random.beta(1.5, 8, N).clip(0, 0.6)
    discount_usage_rate  = np.random.beta(2, 5, N).clip(0, 1)
    email_open_rate      = np.random.beta(2, 6, N).clip(0, 1)
    app_sessions_month   = np.random.negative_binomial(3, 0.4, N).clip(0, 50)
    support_tickets      = np.random.poisson(0.4, N).clip(0, 8)
    rating_avg           = np.random.choice([1,2,3,4,5], N, p=[0.05,0.08,0.20,0.40,0.27])
    category_diversity   = np.random.randint(1, 7, N)

    # ── Churn probability (realistic causal structure) ────────
    churn_score = (
        0.30 * (days_since_last_order / 365)
      + 0.20 * (1 - np.clip(total_orders / 20, 0, 1))
      + 0.15 * return_rate
      + 0.10 * (1 - discount_usage_rate)
      + 0.10 * (1 - email_open_rate)
      + 0.08 * (support_tickets / 8)
      + 0.07 * ((5 - rating_avg) / 4)
      - 0.05 * (app_sessions_month / 50)
      + 0.05 * (city_tiers == 3).astype(float)
      + np.random.normal(0, 0.05, N)
    ).clip(0, 1)

    churned = (churn_score > np.random.uniform(0.35, 0.65, N)).astype(int)

    # ── Intervention history (treatment variables) ────────────
    received_discount_offer  = np.random.binomial(1, 0.35, N)
    received_loyalty_points  = np.random.binomial(1, 0.25, N)
    received_free_shipping   = np.random.binomial(1, 0.20, N)

    # Discount reduces churn slightly for persuadable customers
    persuadable_mask = (churn_score > 0.4) & (churn_score < 0.75)
    churned[persuadable_mask & (received_discount_offer == 1)] = \
        np.random.binomial(1, 0.45, persuadable_mask.sum())[:int((persuadable_mask & (received_discount_offer == 1)).sum())]

    # ── Assemble customers DataFrame ─────────────────────────
    customers = pd.DataFrame({
        "customer_id":           customer_ids,
        "signup_date":           [d.strftime("%Y-%m-%d") for d in signup_dates],
        "age_group":             pd.cut(ages, bins=[0,24,34,44,54,100],
                                        labels=["18-24","25-34","35-44","45-54","55+"]),
        "gender":                genders,
        "city_tier":             city_tiers,
        "device_type":           devices,
        "preferred_category":    categories,
        "tenure_days":           tenure_days,
        "total_orders":          total_orders,
        "avg_order_value":       avg_order_value.round(2),
        "days_since_last_order": days_since_last_order,
        "return_rate":           return_rate.round(4),
        "discount_usage_rate":   discount_usage_rate.round(4),
        "email_open_rate":       email_open_rate.round(4),
        "app_sessions_month":    app_sessions_month,
        "support_tickets":       support_tickets,
        "rating_avg":            rating_avg,
        "category_diversity":    category_diversity,
        "received_discount_offer":  received_discount_offer,
        "received_loyalty_points":  received_loyalty_points,
        "received_free_shipping":   received_free_shipping,
        "churn_score":           churn_score.round(4),
        "churned":               churned,
    })

    # ── Monthly churn trend ───────────────────────────────────
    months = pd.date_range("2023-01-01", periods=18, freq="MS")
    base_churn = 0.18
    trend_data = []
    for i, month in enumerate(months):
        rate    = base_churn + i * 0.008 + np.random.normal(0, 0.012)
        total   = np.random.randint(480, 600)
        churned_n = int(total * rate)
        trend_data.append({
            "month":        month.strftime("%Y-%m"),
            "total_customers": total,
            "churned":      churned_n,
            "churn_rate":   round(churned_n / total, 4),
            "retained":     total - churned_n,
        })
    churn_trend = pd.DataFrame(trend_data)

    # ── Save ──────────────────────────────────────────────────
    os.makedirs("data/raw", exist_ok=True)
    customers.to_csv("data/raw/customers.csv", index=False)
    churn_trend.to_csv("data/raw/churn_trend.csv", index=False)

    print(f"Customers saved:   data/raw/customers.csv  ({len(customers):,} rows)")
    print(f"Churn trend saved: data/raw/churn_trend.csv ({len(churn_trend)} rows)")
    print(f"\nChurn rate in dataset: {customers['churned'].mean():.1%}")
    print(f"Total customers: {len(customers):,}")
    print("Done!")
    return customers, churn_trend

if __name__ == "__main__":
    generate_churnlens_data()