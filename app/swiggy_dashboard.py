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
# Ensure your PDF filename matches exactly what is on GitHub
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
                'order_value': 450, 'category': 'FMCG', 'freshness_hrs_left': 24}
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
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)
    else:
        st.image(SWIGGY_URL, width=120)

    st.title("Control Tower")

    # PDF Download Button
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            st.download_button(
                label="📄 Download Case Study PDF",
                data=f,
                file_name="JagadeeshN_Swiggy_Instamart_Analysis.pdf",
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
    marketing_spend = st.slider("Marketing Spend (₹)", 0, 50000, 0)

# --- SIMULATION ENGINE ---
f_df = df[df['zone'].isin(zones)].copy()
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.3
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.15

f_df['order_value'] += aov_boost + (marketing_spend/1000)
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
burn_rate = (f_df['discount'].sum() / total_gov) * 100
orders = len(f_df)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f'<div class="kpi-metric">₹{total_gov/1e6:.2f}M<div class="kpi-label">Total GOV</div><div class="kpi-subbox">Scale Metric</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="kpi-metric">₹{avg_cm:.2f}<div class="kpi-label">Avg Net Profit/Order</div><div class="kpi-subbox">CM2 Target</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="kpi-metric">{burn_rate:.1f}%<div class="kpi-label">Discount Burn</div><div class="kpi-subbox">Efficiency</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="kpi-metric">{orders:,}<div class="kpi-label">Orders Modeled</div><div class="kpi-subbox">Sample Size</div></div>', unsafe_allow_html=True)

# --- ANALYTICS TABS ---
t1, t2, t3, t4, t5, t6 = st.tabs(["📊 Financials", "🏍️ Ops & Logistics", "🥬 Wastage Control", "🧠 Forecasting", "📈 Scenarios", "📖 Case Study"])

with t1:
    st.subheader("Unit Economics Breakdown")
    metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]
    fig_water = go.Figure(go.Waterfall(orientation = "v", measure = ["relative"]*6 + ["total"],
        x = metrics + ['Net Profit'], y = vals + [0],
        decreasing = {"marker":{"color":"#EF4444"}}, increasing = {"marker":{"color":"#60B246"}},
        totals = {"marker":{"color":"#FC8019"}}))
    st.plotly_chart(fig_water, use_container_width=True)

with t5:
    st.subheader("Scenario Comparison (Net Profit)")
    scenarios = ["Normal Operations", "Heavy Rain", "IPL Match Night"]
    net_profits = []
    for scen in scenarios:
        temp_df = df.copy()
        if scen == "Heavy Rain": temp_df['delivery_cost'] *= 1.3
        elif scen == "IPL Match Night": temp_df['order_value'] *= 1.15
        temp_df['commission'] = temp_df['order_value'] * 0.18
        temp_df['net_profit'] = (temp_df['commission'] + temp_df['ad_revenue'] + temp_df['delivery_fee']) - (
            temp_df['delivery_cost'] + temp_df['discount'] + temp_df['opex'])
        net_profits.append(temp_df['net_profit'].mean())
    st.bar_chart(pd.DataFrame({"Scenario": scenarios, "Net Profit": net_profits}).set_index('Scenario'))

with t6:
    st.header("Strategic Case Study: Achieving CM2 Positivity")
    st.caption("By Jagadeesh N | BBA, SRM IST (2023-26)")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 Problem Statement")
        [cite_start]st.write("Quick-commerce businesses face thin margins due to last-mile costs and discount-heavy growth[cite: 37]. [cite_start]Achieving CM2 positivity is the primary challenge[cite: 38].")
        st.subheader("💡 Key Strategic Insights")
        [cite_start]st.success("**AOV Lever:** A ₹50-₹70 increase in AOV has higher impact than 20% volume growth[cite: 45].")
        [cite_start]st.info("**Batching Efficiency:** Reducing costs by ₹10 via batching is 2x more sustainable than increasing fees[cite: 46].")
    with c2:
        st.subheader("🚀 Recommendations")
        st.markdown("""
        * [cite_start]**Incentivize High-AOV:** Tiered delivery for orders above ₹500[cite: 50].
        * [cite_start]**Optimize Density:** Prioritize batching during IPL nights[cite: 51].
        * [cite_start]**Dynamic Discounting:** Move to Margin-Aware triggers[cite: 52].
        """)
        st.subheader("🛠️ Technical Execution")
        [cite_start]st.write("Built with Python, Pandas, and Plotly to bridge technical analysis and executive strategy[cite: 54, 57].")

st.markdown("---")
st.caption("Developed by Jagadeesh.N | Business Analytics Portfolio")
