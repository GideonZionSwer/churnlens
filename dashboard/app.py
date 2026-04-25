import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import warnings
warnings.filterwarnings("ignore")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="ChurnLens",
    page_icon="CL",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS — Theme 2: Warm Coral Analytics ───────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #FAFAF9;
    color: #1C1917;
}

/* Sidebar */
div[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E7E5E4 !important;
}
div[data-testid="stSidebar"] * { color: #57534E !important; }
div[data-testid="stSidebar"] .stRadio label {
    font-size: 0.85rem !important;
    color: #57534E !important;
}

/* Main content */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Page header */
.page-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #F5F5F4;
}
.page-header .breadcrumb {
    font-size: 0.72rem;
    color: #A8A29E;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}
.page-header h1 {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1C1917 !important;
    margin: 0;
    letter-spacing: -0.02em;
    line-height: 1.3;
}
.page-header .subtitle {
    font-size: 0.85rem;
    color: #78716C;
    margin-top: 4px;
}

/* KPI cards */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E7E5E4;
    border-radius: 10px;
    padding: 1rem 1rem;
    border-top: 3px solid #EA580C;
    height: 110px;
    min-height: 110px;
    max-height: 110px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-card .kpi-label {
    font-size: 0.68rem;
    color: #A8A29E;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 6px;
    font-weight: 500;
}
.kpi-card .kpi-value {
    font-size: 1.7rem;
    font-weight: 700;
    color: #1C1917;
    line-height: 1;
    letter-spacing: -0.02em;
}
.kpi-card .kpi-delta {
    font-size: 0.75rem;
    color: #78716C;
    margin-top: 6px;
}
.kpi-card.danger { border-top-color: #DC2626; }
.kpi-card.danger .kpi-delta { color: #DC2626; }
.kpi-card.success { border-top-color: #16A34A; }
.kpi-card.success .kpi-delta { color: #16A34A; }
.kpi-card.warning { border-top-color: #D97706; }
.kpi-card.warning .kpi-delta { color: #D97706; }

/* Risk badges */
.badge-high {
    display: inline-block;
    background: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-medium {
    display: inline-block;
    background: #FFF7ED;
    color: #EA580C;
    border: 1px solid #FED7AA;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-low {
    display: inline-block;
    background: #F0FDF4;
    color: #16A34A;
    border: 1px solid #BBF7D0;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}

/* Section header */
.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    color: #78716C;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #E7E5E4;
}

/* Customer table rows */
.customer-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #F5F5F4;
    font-size: 0.85rem;
}
.customer-row:last-child { border-bottom: none; }

/* Insight cards */
.insight-card {
    background: #FFF7ED;
    border: 1px solid #FED7AA;
    border-left: 4px solid #EA580C;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
}
.insight-card .insight-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #9A3412;
    margin-bottom: 3px;
}
.insight-card .insight-body {
    font-size: 0.8rem;
    color: #78716C;
    line-height: 1.5;
}

/* Streamlit overrides */
.stSelectbox label, .stCheckbox label, .stRadio label {
    font-size: 0.82rem !important;
    color: #57534E !important;
}
.stButton > button {
    background: #EA580C !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 1.2rem !important;
}
.stButton > button:hover { background: #C2410C !important; }
.stTabs [data-baseweb="tab"] {
    font-size: 0.82rem !important;
    color: #78716C !important;
}
.stTabs [aria-selected="true"] {
    color: #EA580C !important;
    border-bottom-color: #EA580C !important;
}
.stMetric label { color: #78716C !important; font-size: 0.78rem !important; }
div[data-testid="stMetricValue"] { color: #1C1917 !important; font-size: 1.6rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ─────────────────────────────────────────────
@st.cache_data
def load_predictions():
    try:
        from models.churn_model import predict_all_customers, load_model, get_feature_importance
        df = predict_all_customers()
        model, feature_cols = load_model()
        importance = get_feature_importance(model, feature_cols)
        return df, importance
    except Exception as e:
        st.error(f"Model error: {e}")
        return None, None

@st.cache_data
def load_trend():
    try:
        return pd.read_csv("data/raw/churn_trend.csv")
    except:
        return None

@st.cache_data
def load_raw():
    try:
        return pd.read_csv("data/raw/customers.csv")
    except:
        return None

# ── Chart theme ───────────────────────────────────────────────
CHART = dict(
    template="plotly_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="Inter",
    font_color="#57534E",
    margin=dict(t=20, b=20, l=0, r=0),
)
CORAL   = "#EA580C"
CORAL2  = "#FED7AA"
RED     = "#DC2626"
GREEN   = "#16A34A"
AMBER   = "#D97706"
STONE   = "#78716C"

def risk_badge(risk):
    cls = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(risk, "badge-low")
    return f'<span class="{cls}">{risk}</span>'

def page_header(breadcrumb, title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <div class="breadcrumb">{breadcrumb}</div>
        <h1>{title}</h1>
        <div class="subtitle">{subtitle}</div>
    </div>""", unsafe_allow_html=True)

def kpi(label, value, delta="", kind="default"):
    cls = {"danger": "danger", "success": "success", "warning": "warning"}.get(kind, "")
    st.markdown(
        f'<div class="kpi-card {cls}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-delta">{delta}&nbsp;</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.2rem;">
        <div style="font-size:1.2rem;font-weight:700;color:#1C1917;letter-spacing:-0.03em;">
            Churn<span style="color:#EA580C;">Lens</span>
        </div>
        <div style="font-size:0.72rem;color:#A8A29E;margin-top:2px;">
            E-Commerce Churn Intelligence
        </div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    page = st.radio("Navigation", [
        "Overview",
        "Churn Predictions",
        "Feature Analysis",
        "Intervention Simulator",
        "Model Performance",
        "About ChurnLens",
    ])

    st.divider()

    # Filter
    st.markdown('<div style="font-size:0.75rem;font-weight:600;color:#57534E;margin-bottom:6px;">FILTERS</div>', unsafe_allow_html=True)
    df_raw = load_raw()
    cat_options = ["All Categories"] + sorted(df_raw["preferred_category"].dropna().unique().tolist()) if df_raw is not None else ["All Categories"]
    sel_cat = st.selectbox("Category", cat_options)
    sel_risk = st.multiselect("Risk Level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
    st.divider()
    st.markdown('<div style="font-size:0.7rem;color:#A8A29E;">ChurnLens v1.0 · April 2026</div>', unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────
df, importance = load_predictions()
trend = load_trend()

if df is not None:
    # Apply filters properly
    df_filtered = df.copy()
    if sel_cat != "All Categories":
        df_filtered = df_filtered[df_filtered["preferred_category"] == sel_cat]
    if sel_risk:
        df_filtered = df_filtered[df_filtered["churn_risk"].isin(sel_risk)]
else:
    df_filtered = None
    sel_cat = "All Categories"
    sel_risk = ["High", "Medium", "Low"]


# ════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "Overview":
    page_header("ChurnLens", "Customer Churn Overview", "Monitor churn risk across your entire customer base in real time")

    if df is None:
        st.error("Could not load model. Please run: python models/churn_model.py")
        st.stop()

    dv      = df_filtered  # use filtered data throughout overview
    total   = len(dv)
    high    = (dv["churn_risk"] == "High").sum()
    medium  = (dv["churn_risk"] == "Medium").sum()
    churn_r = dv["churned"].mean()
    rev_risk= dv["revenue_at_risk"].sum()

    filter_label = f" — {sel_cat}" if sel_cat != "All Categories" else ""

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Customers Shown", f"{total:,}", f"Filtered base{filter_label}")
    with c2: kpi("High Risk", f"{high:,}", f"{high/max(total,1):.1%} of filtered", "danger")
    with c3: kpi("Medium Risk", f"{medium:,}", f"{medium/max(total,1):.1%} of filtered", "warning")
    with c4: kpi("Churn Rate", f"{churn_r:.1%}", "Historical average")
    with c5: kpi("Revenue at Risk", f"₹{rev_risk/100000:.1f}L", "From at-risk customers", "danger")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        section_title("Churn Rate Trend — Last 18 Months")
        if trend is not None:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trend["month"], y=(trend["churn_rate"] * 100).round(1),
                mode="lines+markers",
                line=dict(color=CORAL, width=2.5),
                marker=dict(size=5, color=CORAL),
                fill="tozeroy",
                fillcolor="rgba(234,88,12,0.08)",
                name="Churn Rate %"
            ))
            fig.update_layout(**CHART, height=240,
                yaxis_title="Churn Rate (%)",
                xaxis_tickangle=-45,
                showlegend=False)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor="#F5F5F4")
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        section_title("Risk Distribution")
        risk_counts = dv["churn_risk"].value_counts().reset_index()
        risk_counts.columns = ["Risk", "Count"]
        risk_counts["Risk"] = pd.Categorical(risk_counts["Risk"], ["High","Medium","Low"])
        risk_counts = risk_counts.sort_values("Risk")
        fig2 = px.pie(risk_counts, names="Risk", values="Count", hole=0.55,
                      color="Risk",
                      color_discrete_map={"High": RED, "Medium": CORAL, "Low": "#86EFAC"})
        fig2.update_layout(**CHART, height=240, showlegend=True,
                           legend=dict(font_size=11, font_color=STONE))
        fig2.update_traces(textfont_size=11, textfont_color="white")
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        section_title("Churn by Product Category")
        cat_churn = dv.groupby("preferred_category")["churned"].mean().reset_index()
        cat_churn.columns = ["Category", "Churn Rate"]
        cat_churn = cat_churn.sort_values("Churn Rate", ascending=True)
        cat_churn["Churn Rate %"] = (cat_churn["Churn Rate"] * 100).round(1)
        fig3 = px.bar(cat_churn, x="Churn Rate %", y="Category", orientation="h",
                      color="Churn Rate %",
                      color_continuous_scale=[[0,"#FEF2F2"],[0.5,CORAL],[1,RED]])
        fig3.update_layout(**CHART, height=250, showlegend=False,
                           coloraxis_showscale=False)
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        section_title("Top 8 At-Risk Customers")
        top_risk = dv[dv["churn_risk"] == "High"].nlargest(8, "churn_probability")[
            ["customer_id","churn_probability","revenue_at_risk","preferred_category"]
        ]
        for _, row in top_risk.iterrows():
            st.markdown(f"""
            <div class="customer-row">
                <div>
                    <div style="font-weight:500;font-size:0.85rem;color:#1C1917;">{row['customer_id']}</div>
                    <div style="font-size:0.75rem;color:#A8A29E;">{row['preferred_category']}</div>
                </div>
                <div style="text-align:right;">
                    <div>{risk_badge("High")}</div>
                    <div style="font-size:0.75rem;color:#57534E;margin-top:3px;">
                        {row['churn_probability']:.0%} · ₹{row['revenue_at_risk']:,.0f}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 2: CHURN PREDICTIONS
# ════════════════════════════════════════════════════════════
elif page == "Churn Predictions":
    page_header("ChurnLens", "Churn Predictions", "Browse every customer's churn probability with risk scores and key drivers")

    if df is None:
        st.error("Model not loaded.")
        st.stop()

    col1, col2, col3 = st.columns(3)
    risk_filter   = col1.selectbox("Risk Level", ["All", "High", "Medium", "Low"])
    cat_filter    = col2.selectbox("Category", ["All"] + sorted(df["preferred_category"].dropna().unique().tolist()))
    sort_by       = col3.selectbox("Sort By", ["churn_probability", "revenue_at_risk", "total_orders"])

    view = df.copy()
    if risk_filter != "All":  view = view[view["churn_risk"] == risk_filter]
    if cat_filter  != "All":  view = view[view["preferred_category"] == cat_filter]
    view = view.sort_values(sort_by, ascending=False)

    st.markdown(f'<div style="font-size:0.8rem;color:#78716C;margin-bottom:12px;">{len(view):,} customers found</div>', unsafe_allow_html=True)

    # Summary cards
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Showing", f"{len(view):,}", "customers")
    with c2: kpi("Avg Churn Prob", f"{view['churn_probability'].mean():.1%}", "")
    with c3: kpi("Revenue at Risk", f"₹{view['revenue_at_risk'].sum()/100000:.1f}L", "")
    with c4: kpi("High Risk", f"{(view['churn_risk']=='High').sum():,}", "in this view", "danger")

    st.markdown("<br>", unsafe_allow_html=True)

    # Scatter plot
    section_title("Churn Probability vs Revenue at Risk")
    fig = px.scatter(
        view.head(2000),
        x="churn_probability", y="revenue_at_risk",
        color="churn_risk",
        color_discrete_map={"High": RED, "Medium": CORAL, "Low": "#86EFAC"},
        hover_data=["customer_id", "preferred_category", "total_orders"],
        opacity=0.7, size_max=6,
    )
    fig.update_layout(**CHART, height=300,
                      xaxis_title="Churn Probability",
                      yaxis_title="Revenue at Risk (₹)",
                      legend=dict(font_size=11))
    fig.update_traces(marker_size=5)
    st.plotly_chart(fig, use_container_width=True)

    # Table
    section_title("Customer Churn Table")
    display_cols = ["customer_id", "preferred_category", "city_tier",
                    "total_orders", "days_since_last_order",
                    "churn_probability", "churn_risk", "revenue_at_risk"]
    display_df = view[display_cols].head(500).copy()
    display_df["churn_probability"] = display_df["churn_probability"].apply(lambda x: f"{x:.1%}")
    display_df["revenue_at_risk"]   = display_df["revenue_at_risk"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(display_df, use_container_width=True, height=380)

    csv = view[display_cols].to_csv(index=False)
    st.download_button("Export as CSV", csv, "churnlens_predictions.csv", "text/csv")


# ════════════════════════════════════════════════════════════
# PAGE 3: FEATURE ANALYSIS
# ════════════════════════════════════════════════════════════
elif page == "Feature Analysis":
    page_header("ChurnLens", "Feature Analysis", "Understand what drives churn — feature importance and behavioral patterns")

    if df is None or importance is None:
        st.error("Model not loaded.")
        st.stop()

    dfa = df_filtered.copy()
    filter_note = f" — {sel_cat}" if sel_cat != "All Categories" else ""
    st.markdown(
        f'<div style="font-size:0.78rem;color:#A8A29E;margin-bottom:12px;">'
        f'Showing <b style="color:#1C1917;">{len(dfa):,}</b> customers{filter_note}</div>',
        unsafe_allow_html=True
    )

    # ── Row 1: Avg churn prob per feature bucket (responds to filter) ──
    section_title("Churn Rate by Key Behavioral Features")

    num_features = ["days_since_last_order","total_orders","return_rate",
                    "email_open_rate","app_sessions_month","support_tickets",
                    "discount_usage_rate","rating_avg","avg_order_value","tenure_days"]
    avail = [c for c in num_features if c in dfa.columns]
    feature_churn = []
    for feat in avail:
        avg_churn_high = dfa[dfa[feat] >= dfa[feat].median()]["churned"].mean()
        avg_churn_low  = dfa[dfa[feat] <  dfa[feat].median()]["churned"].mean()
        feature_churn.append({"Feature": feat,
                               "Above Median": round(avg_churn_high * 100, 1),
                               "Below Median": round(avg_churn_low  * 100, 1),
                               "Difference":   round((avg_churn_high - avg_churn_low) * 100, 1)})
    feat_df = pd.DataFrame(feature_churn).sort_values("Difference", ascending=True)
    fig = px.bar(feat_df, x="Difference", y="Feature", orientation="h",
                 color="Difference",
                 color_continuous_scale=[[0,"#86EFAC"],[0.4,CORAL2],[1,RED]],
                 hover_data=["Above Median","Below Median"])
    fig.update_layout(**CHART, height=380,
                      xaxis_title="Churn Rate Difference: Above vs Below Median (%)",
                      coloraxis_showscale=False)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Distribution + City tier side by side ──
    col_a, col_b = st.columns(2)

    with col_a:
        section_title("Churn Probability Distribution")
        churned_dfa     = dfa[dfa["churned"] == 1]["churn_probability"]
        not_churned_dfa = dfa[dfa["churned"] == 0]["churn_probability"]
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(x=not_churned_dfa, name="Retained",
                                    marker_color="#86EFAC", opacity=0.7,
                                    nbinsx=40))
        fig2.add_trace(go.Histogram(x=churned_dfa, name="Churned",
                                    marker_color=CORAL, opacity=0.7,
                                    nbinsx=40))
        fig2.update_layout(**CHART, height=280, barmode="overlay",
                           legend=dict(font_size=11),
                           xaxis_title="Churn Probability",
                           yaxis_title="Count")
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        section_title("Avg Churn Probability by City Tier")
        tier_churn = dfa.groupby("city_tier")["churn_probability"].mean().reset_index()
        tier_churn.columns = ["City Tier", "Avg Churn Prob"]
        tier_churn["City Tier"] = tier_churn["City Tier"].map({1:"Tier 1 (Metro)", 2:"Tier 2", 3:"Tier 3 (Small)"})
        fig3 = px.bar(tier_churn, x="City Tier", y="Avg Churn Prob",
                      color="Avg Churn Prob",
                      color_continuous_scale=[[0,CORAL2],[1,RED]],
                      text=tier_churn["Avg Churn Prob"].apply(lambda x: f"{x:.1%}"))
        fig3.update_layout(**CHART, height=280, coloraxis_showscale=False)
        fig3.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 3: Correlation (full width) ──
    section_title("Feature Correlation with Churn")
    num_cols = ["days_since_last_order","total_orders","avg_order_value",
                "return_rate","email_open_rate","app_sessions_month",
                "support_tickets","rating_avg","discount_usage_rate","churned"]
    corr = dfa[num_cols].corr()["churned"].drop("churned").sort_values()
    fig4 = go.Figure(go.Bar(
        x=corr.values, y=corr.index,
        orientation="h",
        marker_color=[RED if v > 0 else "#86EFAC" for v in corr.values],
        marker_line_width=0,
    ))
    fig4.update_layout(**CHART, height=300,
                       xaxis_title="Correlation with Churn",
                       yaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 4: INTERVENTION SIMULATOR
# ════════════════════════════════════════════════════════════
elif page == "Intervention Simulator":
    page_header("ChurnLens", "Intervention Simulator", "Simulate the revenue impact of retention campaigns before spending a rupee")

    if df is None:
        st.error("Model not loaded.")
        st.stop()

    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">How this works</div>
        <div class="insight-body">
            Select a target customer segment, choose an intervention type, set your budget,
            and the simulator estimates how many customers you can retain and the expected
            revenue recovered. Based on churn probability uplift estimates.
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        segment = st.selectbox("Target Segment", [
            "All High Risk",
            "High Risk — Electronics",
            "High Risk — Fashion",
            "High Risk — Tier 3 Cities",
            "Medium Risk — High Value",
        ])
        intervention = st.selectbox("Intervention Type", [
            "Discount Offer (10%)",
            "Discount Offer (20%)",
            "Loyalty Points (500 pts)",
            "Free Shipping (3 months)",
            "Personalized Email Campaign",
        ])

    with col2:
        budget = st.slider("Campaign Budget (₹)", 10000, 500000, 100000, 10000)
        effectiveness = st.slider("Estimated Effectiveness (%)", 10, 60, 30, 5)

    # Compute segment — respect sidebar filter
    base = df_filtered.copy()
    target = base[base["churn_risk"] == "High"].copy()
    if "Electronics" in segment:   target = target[target["preferred_category"] == "Electronics"]
    elif "Fashion"   in segment:   target = target[target["preferred_category"] == "Fashion"]
    elif "Tier 3"    in segment:   target = target[target["city_tier"] == 3]
    elif "High Value" in segment:  target = base[(base["churn_risk"] == "Medium") & (base["avg_order_value"] > base["avg_order_value"].median())]

    cost_map = {"Discount Offer (10%)": 200, "Discount Offer (20%)": 400,
                "Loyalty Points (500 pts)": 150, "Free Shipping (3 months)": 250,
                "Personalized Email Campaign": 50}
    cost_per = cost_map.get(intervention, 200)
    customers_reachable = min(len(target), budget // cost_per)
    customers_retained  = int(customers_reachable * effectiveness / 100)
    revenue_recovered   = target.nlargest(customers_retained, "revenue_at_risk")["revenue_at_risk"].sum()
    roi = ((revenue_recovered - budget) / budget * 100) if budget > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Simulation Results")

    r1, r2, r3, r4 = st.columns(4)
    with r1: kpi("Customers in Segment", f"{len(target):,}", "eligible for campaign")
    with r2: kpi("Customers Reachable", f"{customers_reachable:,}", f"within ₹{budget:,} budget")
    with r3: kpi("Expected Retained", f"{customers_retained:,}", f"at {effectiveness}% effectiveness", "success")
    with r4:
        kind = "success" if roi > 0 else "danger"
        kpi("Expected ROI", f"{roi:.0f}%", f"₹{revenue_recovered:,.0f} recovered", kind)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        section_title("Budget Allocation Breakdown")
        fig = go.Figure(go.Waterfall(
            name="Budget", orientation="v",
            measure=["absolute","relative","relative","total"],
            x=["Campaign Budget","Intervention Cost","Admin & Creative","Net Investment"],
            y=[budget, -int(budget*0.75), -int(budget*0.15), 0],
            connector={"line": {"color": STONE}},
            decreasing={"marker": {"color": CORAL}},
            increasing={"marker": {"color": "#86EFAC"}},
            totals={"marker": {"color": "#1C1917"}},
        ))
        fig.update_layout(**CHART, height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        section_title("Effectiveness Sensitivity Analysis")
        eff_range  = list(range(10, 65, 5))
        ret_range  = [int(customers_reachable * e / 100) for e in eff_range]
        rev_range  = [target.nlargest(r, "revenue_at_risk")["revenue_at_risk"].sum() / 100000 for r in ret_range]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=eff_range, y=rev_range,
                                  mode="lines+markers",
                                  line=dict(color=CORAL, width=2.5),
                                  marker=dict(size=6, color=CORAL),
                                  name="Revenue Recovered (L)"))
        fig2.add_vline(x=effectiveness, line_dash="dot", line_color=STONE, annotation_text=f"Current: {effectiveness}%")
        fig2.update_layout(**CHART, height=280,
                           xaxis_title="Effectiveness (%)",
                           yaxis_title="Revenue Recovered (₹L)",
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 5: MODEL PERFORMANCE
# ════════════════════════════════════════════════════════════
elif page == "Model Performance":
    page_header("ChurnLens", "Model Performance", "Evaluate the churn prediction model — accuracy, precision, recall, and validation")
    st.markdown('<div style="font-size:0.78rem;color:#A8A29E;margin-bottom:8px;">Model metrics are computed on the full test set — category filter does not apply here.</div>', unsafe_allow_html=True)

    if df is None or importance is None:
        st.error("Model not loaded.")
        st.stop()

    from models.churn_model import load_data, engineer_features, get_all_features, load_model
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix

    raw_df = load_data()
    feat_df = engineer_features(raw_df)
    model, feature_cols = load_model()
    X = feat_df[[c for c in feature_cols if c in feat_df.columns]]
    y = feat_df["churned"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    y_prob = model.predict_proba(X_te)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)
    auc = roc_auc_score(y_te, y_prob)

    m1, m2, m3, m4 = st.columns(4)
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    with m1: kpi("AUC-ROC", f"{auc:.4f}", "Area under curve", "success" if auc > 0.75 else "warning")
    with m2: kpi("Accuracy", f"{accuracy_score(y_te, y_pred):.1%}", "Overall correct")
    with m3: kpi("Precision", f"{precision_score(y_te, y_pred):.1%}", "Of predicted churners")
    with m4: kpi("Recall", f"{recall_score(y_te, y_pred):.1%}", "Of actual churners")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        section_title("ROC Curve")
        fpr, tpr, _ = roc_curve(y_te, y_prob)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines",
                                  line=dict(color=CORAL, width=2.5),
                                  name=f"AUC = {auc:.3f}"))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
                                  line=dict(color=STONE, dash="dash", width=1),
                                  name="Random"))
        fig.update_layout(**CHART, height=300,
                          xaxis_title="False Positive Rate",
                          yaxis_title="True Positive Rate",
                          legend=dict(font_size=11))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        section_title("Confusion Matrix")
        cm = confusion_matrix(y_te, y_pred)
        fig2 = px.imshow(cm, labels=dict(x="Predicted", y="Actual"),
                         x=["Retained","Churned"], y=["Retained","Churned"],
                         color_continuous_scale=[[0,"#FFF7ED"],[0.5,CORAL2],[1,CORAL]],
                         text_auto=True)
        fig2.update_layout(**CHART, height=300, coloraxis_showscale=False)
        fig2.update_traces(textfont_size=16)
        st.plotly_chart(fig2, use_container_width=True)

    section_title("Precision-Recall Curve")
    prec, rec, thr = precision_recall_curve(y_te, y_prob)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=rec, y=prec, mode="lines",
                              line=dict(color=CORAL, width=2.5),
                              fill="tozeroy", fillcolor="rgba(234,88,12,0.08)"))
    fig3.update_layout(**CHART, height=250,
                       xaxis_title="Recall", yaxis_title="Precision",
                       showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 6: ABOUT
# ════════════════════════════════════════════════════════════
elif page == "About ChurnLens":
    page_header("ChurnLens", "About This Project", "E-commerce churn prediction with causal inference — built by Gideon Zion Swer")

    col_l, col_r = st.columns([1, 2])

    with col_l:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E7E5E4;border-radius:12px;padding:1.5rem;text-align:center;">
            <div style="width:64px;height:64px;border-radius:50%;background:#FFF7ED;border:2px solid #FED7AA;
                        display:flex;align-items:center;justify-content:center;margin:0 auto 12px;
                        font-size:1.3rem;font-weight:700;color:#EA580C;">GZ</div>
            <div style="font-size:1rem;font-weight:700;color:#1C1917;">Gideon Zion Swer</div>
            <div style="font-size:0.78rem;color:#78716C;margin-top:2px;">Data Analyst</div>
            <div style="font-size:0.72rem;color:#A8A29E;margin-top:2px;">Meghalaya, Northeast India</div>
            <div style="border-top:1px solid #F5F5F4;margin:1rem 0;padding-top:1rem;text-align:left;">
                <div style="font-size:0.7rem;font-weight:600;color:#A8A29E;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">Stack</div>
                <div style="display:flex;flex-wrap:wrap;gap:5px;">
                    <span style="background:#FFF7ED;color:#9A3412;font-size:0.7rem;padding:2px 8px;border-radius:20px;border:1px solid #FED7AA;">Python</span>
                    <span style="background:#FFF7ED;color:#9A3412;font-size:0.7rem;padding:2px 8px;border-radius:20px;border:1px solid #FED7AA;">XGBoost</span>
                    <span style="background:#FFF7ED;color:#9A3412;font-size:0.7rem;padding:2px 8px;border-radius:20px;border:1px solid #FED7AA;">Streamlit</span>
                    <span style="background:#FFF7ED;color:#9A3412;font-size:0.7rem;padding:2px 8px;border-radius:20px;border:1px solid #FED7AA;">Plotly</span>
                    <span style="background:#FFF7ED;color:#9A3412;font-size:0.7rem;padding:2px 8px;border-radius:20px;border:1px solid #FED7AA;">SHAP</span>
                </div>
            </div>
            <a href="https://www.linkedin.com/in/gideon-zion-swer-89a84a292" target="_blank"
               style="display:block;background:#EA580C;color:white;text-align:center;
                      padding:8px;border-radius:8px;text-decoration:none;
                      font-size:0.8rem;font-weight:600;margin-top:8px;">
                LinkedIn Profile
            </a>
        </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-title">What ChurnLens Does</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#57534E;font-size:0.9rem;line-height:1.8;margin-bottom:1rem;">
        <b style="color:#1C1917;">ChurnLens</b> is a churn prediction and retention intelligence platform for
        e-commerce businesses. It goes beyond standard churn models by not just predicting
        <i>who</i> will leave, but identifying <i>why</i> they leave and <i>what interventions</i>
        would retain them — with expected revenue impact.
        </p>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:1rem;">Key Capabilities</div>', unsafe_allow_html=True)
        caps = [
            ("Churn Prediction", "XGBoost model with 27 behavioral features — AUC 0.76+"),
            ("Risk Segmentation", "Every customer scored and segmented into High / Medium / Low risk"),
            ("Revenue Quantification", "Revenue at risk calculated per customer for business prioritization"),
            ("Feature Analysis", "Full feature importance and correlation analysis to understand drivers"),
            ("Intervention Simulator", "Budget-aware ROI simulator for retention campaign planning"),
        ]
        for title, desc in caps:
            st.markdown(f"""
            <div style="background:#FAFAF9;border:1px solid #E7E5E4;border-radius:8px;
                        padding:0.8rem 1rem;margin-bottom:0.5rem;border-left:3px solid #EA580C;">
                <div style="font-size:0.85rem;font-weight:600;color:#1C1917;">{title}</div>
                <div style="font-size:0.78rem;color:#78716C;margin-top:2px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;color:#A8A29E;font-size:0.78rem;padding:1rem;border-top:1px solid #F5F5F4;">
        ChurnLens v1.0 · Built with Python, Streamlit, XGBoost, Plotly · Gideon Zion Swer · April 2026
    </div>""", unsafe_allow_html=True)
