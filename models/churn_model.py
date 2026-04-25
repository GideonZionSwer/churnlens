import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (roc_auc_score, classification_report,
                             confusion_matrix, precision_recall_curve)
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")

MODEL_PATH = "models/saved/churn_model.pkl"
FEATURES_PATH = "models/saved/feature_cols.pkl"
SCALER_PATH = "models/saved/scaler.pkl"

FEATURE_COLS = [
    "tenure_days", "total_orders", "avg_order_value",
    "days_since_last_order", "return_rate", "discount_usage_rate",
    "email_open_rate", "app_sessions_month", "support_tickets",
    "rating_avg", "category_diversity", "city_tier",
    "received_discount_offer", "received_loyalty_points",
    "received_free_shipping",
]

CAT_COLS = ["age_group", "gender", "device_type", "preferred_category"]


def load_data():
    df = pd.read_csv("data/raw/customers.csv")
    return df


def engineer_features(df):
    df = df.copy()

    # RFM composite
    df["rfm_score"] = (
        (1 - df["days_since_last_order"] / 365) * 0.4
        + (df["total_orders"] / df["total_orders"].max()) * 0.3
        + (df["avg_order_value"] / df["avg_order_value"].max()) * 0.3
    )

    # Engagement score
    df["engagement_score"] = (
        df["email_open_rate"] * 0.4
        + (df["app_sessions_month"] / df["app_sessions_month"].max()) * 0.4
        + df["discount_usage_rate"] * 0.2
    )

    # Risk signals
    df["high_return_flag"] = (df["return_rate"] > 0.3).astype(int)
    df["low_activity_flag"] = (df["days_since_last_order"] > 90).astype(int)
    df["complaints_flag"] = (df["support_tickets"] >= 3).astype(int)
    df["low_rating_flag"] = (df["rating_avg"] <= 2).astype(int)
    df["order_value_log"] = np.log1p(df["avg_order_value"])
    df["tenure_months"] = df["tenure_days"] / 30

    # Encode categoricals
    le = LabelEncoder()
    for col in CAT_COLS:
        if col in df.columns:
            df[col + "_enc"] = le.fit_transform(df[col].astype(str))

    return df


def get_all_features(df):
    base = FEATURE_COLS.copy()
    extra = [
        "rfm_score", "engagement_score",
        "high_return_flag", "low_activity_flag",
        "complaints_flag", "low_rating_flag",
        "order_value_log", "tenure_months",
    ]
    cat_enc = [c + "_enc" for c in CAT_COLS if c + "_enc" in df.columns]
    return [f for f in base + extra + cat_enc if f in df.columns]


def train_model(df=None, save=True):
    if df is None:
        df = load_data()

    df = engineer_features(df)
    feature_cols = get_all_features(df)

    X = df[feature_cols]
    y = df["churned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scale_pos = (y_train == 0).sum() / (y_train == 1).sum()

    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=scale_pos,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="auc",
        verbosity=0,
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)
    auc    = roc_auc_score(y_test, y_prob)

    print(f"\nModel trained successfully!")
    print(f"AUC-ROC Score: {auc:.4f}")
    print(f"Features used: {len(feature_cols)}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Retained","Churned"]))

    if save:
        os.makedirs("models/saved", exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)
        with open(FEATURES_PATH, "wb") as f:
            pickle.dump(feature_cols, f)
        print(f"Model saved to {MODEL_PATH}")

    return model, feature_cols, auc, (X_test, y_test, y_prob)


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Training now...")
        train_model()

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(FEATURES_PATH, "rb") as f:
        feature_cols = pickle.load(f)
    return model, feature_cols


def predict_all_customers(df=None):
    model, feature_cols = load_model()

    if df is None:
        df = load_data()

    df = engineer_features(df)
    X  = df[[c for c in feature_cols if c in df.columns]]

    probs = model.predict_proba(X)[:, 1]
    df = df.copy()
    df["churn_probability"] = probs.round(4)
    df["churn_risk"] = pd.cut(
        probs,
        bins=[0, 0.35, 0.65, 1.0],
        labels=["Low", "Medium", "High"]
    )
    df["revenue_at_risk"] = (df["avg_order_value"] * df["churn_probability"]).round(2)

    return df


def get_feature_importance(model=None, feature_cols=None):
    if model is None:
        model, feature_cols = load_model()
    importance = pd.DataFrame({
        "feature":    feature_cols,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False).reset_index(drop=True)
    return importance


def get_model_metrics(X_test, y_test, y_prob):
    auc = roc_auc_score(y_test, y_prob)
    y_pred = (y_prob >= 0.5).astype(int)
    cm = confusion_matrix(y_test, y_pred)
    precision, recall, thresholds = precision_recall_curve(y_test, y_prob)
    report = classification_report(
        y_test, y_pred,
        target_names=["Retained","Churned"],
        output_dict=True
    )
    return {
        "auc":        round(auc, 4),
        "confusion_matrix": cm,
        "precision":  precision,
        "recall":     recall,
        "thresholds": thresholds,
        "report":     report,
    }


if __name__ == "__main__":
    print("Training ChurnLens churn prediction model...")
    model, feature_cols, auc, test_data = train_model()
    X_test, y_test, y_prob = test_data
    metrics = get_model_metrics(X_test, y_test, y_prob)
    print(f"\nFinal AUC: {metrics['auc']}")
    print("\nPredicting churn for all customers...")
    predictions = predict_all_customers()
    print(predictions[["customer_id","churn_probability","churn_risk","revenue_at_risk"]].head(10))
    print(f"\nHigh risk customers: {(predictions['churn_risk']=='High').sum():,}")
    print(f"Medium risk:         {(predictions['churn_risk']=='Medium').sum():,}")
    print(f"Low risk:            {(predictions['churn_risk']=='Low').sum():,}")
