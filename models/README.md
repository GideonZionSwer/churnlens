ChurnLens — E-Commerce Churn Intelligence
> Predict who will churn. Understand why. Simulate what stops them.
Live Demo: churnlens.streamlit.app
---
What is ChurnLens?
ChurnLens is a churn prediction and retention intelligence dashboard built for e-commerce businesses. It goes beyond standard churn models by not just predicting who will leave, but identifying why they leave and what interventions would retain them — with expected revenue impact.
Most churn tools answer one question: Who will leave?
ChurnLens answers three:
Who will leave? — XGBoost churn classifier
Why are they leaving? — Behavioral feature analysis
What should we do? — Intervention simulator with ROI estimates
---
Dashboard Pages
Page	What it shows
Overview	Churn KPIs, trend chart, risk distribution, top at-risk customers
Churn Predictions	Every customer's churn probability, risk score, revenue at risk
Feature Analysis	What drives churn — behavioral patterns by category and city tier
Intervention Simulator	Budget-aware ROI simulator for retention campaigns
Model Performance	ROC curve, AUC, confusion matrix, precision-recall
About	Project documentation and methodology
---
Dataset
About the Data
The dataset used in ChurnLens is synthetically generated using Python — no real customer data is used. It was built from scratch using `NumPy` and `Pandas` to simulate realistic e-commerce customer behavior with statistically plausible churn patterns.
The synthetic generator (`data/generate_data.py`) creates 10,000 customers with the following features:
Feature	Description
`customer_id`	Unique customer identifier
`tenure_days`	Days since account creation
`total_orders`	Total number of orders placed
`avg_order_value`	Average spend per order (INR)
`days_since_last_order`	Recency — key churn signal
`return_rate`	Proportion of orders returned
`discount_usage_rate`	How often discounts are used
`email_open_rate`	Email engagement rate
`app_sessions_month`	App activity in last 30 days
`support_tickets`	Number of complaints raised
`rating_avg`	Average product rating given
`city_tier`	1 = Metro, 2 = Tier-2, 3 = Small city
`preferred_category`	Electronics, Fashion, Grocery, Beauty, Sports, Home
`churned`	Target variable — 0 = retained, 1 = churned
The churn label is assigned using a causal scoring formula that weights recency, frequency, returns, engagement, and satisfaction — making the patterns realistic and learnable.
Churn rate in generated dataset: ~14%
---
Generate the Dataset Yourself
```bash
python data/generate_data.py
```
This creates two files:
`data/raw/customers.csv` — 10,000 customer records
`data/raw/churn_trend.csv` — 18-month churn trend data
---
Real Datasets You Can Use Instead
If you want to replace the synthetic data with real e-commerce or churn datasets, here are the best publicly available options:
Dataset	Source	Description	Link
Telco Customer Churn	Kaggle	IBM dataset — 7,043 telecom customers with churn labels	Download
E-Commerce Churn Dataset	Kaggle	5,630 e-commerce customers with behavioral features	Download
Online Retail II	UCI ML Repository	Real transactional data from a UK online retailer	Download
Brazilian E-Commerce (Olist)	Kaggle	100k real orders from Brazilian marketplace	Download
E-Commerce Behavior Data	Kaggle	Multi-category store — 285M rows of user behavior	Download
> **Note:** To use any of the above datasets, place the CSV in `data/raw/`, update the column names in `models/churn_model.py` to match, and re-run `python models/churn_model.py`.
---
Tech Stack
Layer	Technology
Language	Python 3.11+
Dashboard	Streamlit
ML Model	XGBoost (AUC 0.75+)
Data Processing	Pandas, NumPy
Visualization	Plotly Express
Model Explainability	SHAP
Dataset	Synthetic e-commerce (10,000 customers)
---
Project Structure
```
churnlens/
├── data/
│   ├── raw/                    # Generated CSV files
│   └── generate_data.py        # Synthetic dataset generator
├── models/
│   ├── saved/                  # Trained model files (.pkl)
│   └── churn_model.py          # XGBoost training and prediction
├── dashboard/
│   └── app.py                  # Main Streamlit dashboard
├── requirements.txt
└── README.md
```
---
Run Locally
1. Clone the repo
```bash
git clone https://github.com/GideonZionSwer/churnlens.git
cd churnlens
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Generate the dataset
```bash
python data/generate_data.py
```
4. Train the model
```bash
python models/churn_model.py
```
5. Run the dashboard
```bash
streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501`
---
Key Results
AUC-ROC: 0.75+ on held-out test set
10,000 synthetic e-commerce customers
1,314 high-risk customers identified
₹59L+ revenue at risk quantified
6 interactive pages with real-time filtering
---
Built By
Gideon Zion Swer — Data Analyst, Meghalaya, Northeast India
---
ChurnLens v1.0 · April 2026