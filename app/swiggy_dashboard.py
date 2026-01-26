import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import itertools

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png")
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"
# Matches exactly: JagadeeshN_SwiggyInstamart_Profitability_CaseStudy.pdf
PDF_PATH = os.path.join(BASE_DIR, "JagadeeshN_SwiggyInstamart_Profitability_CaseStudy.pdf")

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #262730; }
    .main-title {
        color: #3D4152;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        font-size: 2.2rem;
    }
    .kpi-metric {
        background-color: #FC8019;
        color: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 6px 14px rgba(252, 128, 25, 0.35);
        text-align: center;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #ffffff;
        opacity: 0.9;
        font-weight: 500;
    }
    .kpi-subbox {
        margin-top: 8px;
        background-color: #000000;
        color: #22C55E;
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING & ENRICHMENT ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 Missing {DATA_PATH}")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    required = {'delivery_fee': 15, 'delivery_cost': 40, 'discount': 20,
                'order_value': 450, 'category': 'FMCG', 'freshness_hrs_left': 24,
                'weather': 'Clear', 'zone': 'Cluster A'}
    for col, val in required.items():
        if col not in df.columns:
            df[col] = val
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['commission'] = df['order_value'] * 0.18
    df['ad_revenue'] = df['order_value'] * 0.05
    df['opex'] = 12
    df['gross_margin'] = (df['commission'] + df['ad_revenue'] + df['delivery_fee']) - (
        df['delivery_cost'] + df['discount'] + df['opex']
    )
    return df

df = load_and_enrich()

# --- SIDEBAR ---
with st.sidebar:
    st.image(SWIGGY_URL, width=120)
    st.title("Control Tower")

    # PDF Download Button
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            st.download_button(
                label="📄 Download Case Study PDF",
                data=f,
                file_name="JagadeeshN_Instamart_Analysis.pdf",
                mime="application/pdf"
            )

    theme = st.radio("Select Theme", ["Light","Dark"])
    zones = st.multiselect("Geographic Clusters", df['zone'].unique(), df['zone'].unique())
    
    st.divider()
    st.subheader("🛠️ Profitability Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 5)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 20)
    
    st.subheader("⛈️ Contextual Scenarios")
    scenario = st.selectbox("Select Conditions", ["Normal Operations", "Heavy Rain", "IPL Match Night"])
    aov_boost = st.slider("AOV Expansion Strategy (₹)", 0, 100, 0)

# --- SIMULATION ENGINE ---
f_df = df[df['zone'].isin(zones)].copy()
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.3
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.15

f_df['order_value'] += aov_boost
f_df['commission'] = f_df['order_value'] * 0.18
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (
    f_df['delivery_cost'] + f_df['discount'] + f_df['opex']
)

# --- HEADER ---
st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
st.markdown("#### 🚀 Target: Positive Contribution Margin (CM2) by June 2026")
st.divider()

# --- KPI ROW ---
total_gov = f_df['order_value'].sum()
avg_cm = f_df['net_profit'].mean()
burn_rate = (f_df['discount'].sum() / total_gov) * 100 if total_gov != 0 else 0
orders = len(f_df)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-metric">₹{total_gov/1e6:.2f}M<div class="kpi-label">Total GOV</div><div class="kpi-subbox">Scale</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-metric">₹{avg_cm:.2f}<div class="kpi-label">Avg Net Profit/Order</div><div class="kpi-subbox">CM2 Target</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-metric">{burn_rate:.1f}%<div class="kpi-label">Discount Burn</div><div class="kpi-subbox">Efficiency</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-metric">{orders:,}<div class="kpi-label">Orders Modeled</div><div class="kpi-subbox">Sample</div></div>', unsafe_allow_html=True)

# --- ANALYTICS TABS ---
t1, t2, t3, t4, t5, t6 = st.tabs(["📊 Financials", "🏍️ Ops", "🥬 Wastage", "🧠 Forecasting", "📈 Scenarios", "📖 Case Study"])

with t1:
    st.subheader("Unit Economics Waterfall")
    metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]
    fig_water = go.Figure(go.Waterfall(orientation = "v", x = metrics + ['Net Profit'], y = vals + [0],
        decreasing = {"marker":{"color":"#EF4444"}}, increasing = {"marker":{"color":"#60B246"}}, totals = {"marker":{"color":"#FC8019"}}))
    st.plotly_chart(fig_water, use_container_width=True)

with t5:
    st.subheader("Scenario Comparison")
    scenarios = ["Normal Operations", "Heavy Rain", "IPL Match Night"]
    profits = []
    for s in scenarios:
        temp = df.copy()
        if s == "Heavy Rain": temp['delivery_cost'] *= 1.3
        elif s == "IPL Match Night": temp['order_value'] *= 1.15
        temp['commission'] = temp['order_value'] * 0.18
        temp['net_profit'] = (temp['commission'] + temp['ad_revenue'] + temp['delivery_fee']) - (temp['delivery_cost'] + temp['discount'] + temp['opex'])
        profits.append(temp['net_profit'].mean())
    st.bar_chart(pd.DataFrame({"Scenario": scenarios, "Net Profit": profits}).set_index('Scenario'))

with t6:
    st.header("Strategic Case Study: Achieving CM2 Positivity")
    st.caption("By Jagadeesh N | BBA, SRM IST (2026)")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 Problem Statement")
        st.write("Quick-commerce businesses like Swiggy Instamart operate on thin margins due to high last-mile costs and discount-heavy growth.")
        st.write("Achieving CM2 positivity is the industry's primary challenge.")
        st.subheader("💡 Key Strategic Insights")
        st.success("**AOV Lever:** A ₹50-₹70 increase in AOV has higher impact than 20% volume growth.")
        st.info("**Batching:** Reducing costs by ₹10 via batching is 2x more sustainable than increasing fees.")
    with c2:
        st.subheader("🚀 Recommendations")
        st.markdown("* **High-AOV Baskets:** Tiered delivery for orders >₹500.\n* **Density:** Prioritize multi-order batching during peak demand.\n* **Discounting:** Shift to 'Margin-Aware' triggers.")
        st.subheader("🛠️ Technical Execution")
        st.write("Developed with Python and Pandas to bridge technical analysis and executive strategy.")

st.markdown("---")
st.caption("Developed by Jagadeesh.N | Business Analytics Portfolio")

