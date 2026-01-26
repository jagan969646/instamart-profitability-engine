import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import itertools

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS & ASSETS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
PDF_PATH = os.path.join(BASE_DIR, "JagadeeshN_SwiggyInstamart_Profitability_CaseStudy.pdf")

# Logos
GITHUB_LOGO_URL = "https://raw.githubusercontent.com/jagan969646/instamart-profitability-engine/main/app/Logo.png"
SWIGGY_BRAND_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #262730; }
    .main-title { color: #FC8019; font-weight: 800; font-size: 2.2rem; }
    .kpi-metric {
        background-color: #FC8019;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .kpi-label { font-size: 0.85rem; color: #ffffff; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 Data file not found.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df['order_time'] = pd.to_datetime(df['order_time'])
    # Ensure required columns
    for col, val in {'delivery_fee':15,'delivery_cost':40,'discount':20,'order_value':450,'category':'FMCG','freshness_hrs_left':24}.items():
        if col not in df.columns:
            df[col] = val
    df['commission'] = df['order_value']*0.18
    df['ad_revenue'] = df['order_value']*0.05
    df['opex'] = 12
    df['gross_margin'] = (df['commission']+df['ad_revenue']+df['delivery_fee'])-(df['delivery_cost']+df['discount']+df['opex'])
    return df

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    # Sidebar Logo
    try:
        st.image(GITHUB_LOGO_URL, width=150, caption="Instamart Engine", use_container_width=False)
    except:
        st.image(SWIGGY_BRAND_URL, width=150)

    st.title("Control Tower")

    # Case Study Download
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            st.download_button(label="📄 Download Case Study PDF", data=f, file_name="JagadeeshN_Analysis.pdf")

    st.divider()
    st.subheader("🛠️ Profitability Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 5)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 20)
    aov_boost = st.slider("AOV Expansion Strategy (₹)", 0, 100, 0)
    scenario = st.selectbox("Conditions", ["Normal Operations", "Heavy Rain", "IPL Match Night"])
    marketing_spend = st.slider("Marketing Spend (₹)", 0, 50000, 0)

    # Reset
    if st.button("🔄 Reset Levers"):
        st.experimental_rerun()

# --- SIMULATION ENGINE ---
f_df = df.copy()
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)
f_df['order_value'] += aov_boost + marketing_spend/1000

if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.3
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.15

f_df['commission'] = f_df['order_value']*0.18
f_df['ad_revenue'] = f_df['order_value']*0.05
f_df['opex'] = 12
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (
    f_df['delivery_cost'] + f_df['discount'] + f_df['opex']
)

# --- HEADER ---
col_logo, col_text = st.columns([1,5])
with col_logo:
    try:
        st.image(GITHUB_LOGO_URL, width=80)
    except:
        st.image(SWIGGY_BRAND_URL, width=80)
with col_text:
    st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
st.divider()

# --- KPI ROW ---
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f'<div class="kpi-metric">₹{f_df["order_value"].sum()/1e6:.2f}M<br><span class="kpi-label">Total GOV</span></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-metric">₹{f_df["net_profit"].mean():.2f}<br><span class="kpi-label">Avg Profit/Order (CM2)</span></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-metric">{len(f_df):,}<br><span class="kpi-label">Orders Analyzed</span></div>', unsafe_allow_html=True)

# --- TABS ---
t1, t2, t3 = st.tabs(["📊 Financials", "📈 Scenarios", "📖 Case Study"])

# --- Financials Tab ---
with t1:
    st.subheader("Unit Economics Waterfall")
    metrics = ['Commission','Ad Revenue','Delivery Fee','Delivery Cost','Discount','OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(),
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]
    fig = go.Figure(go.Waterfall(orientation="v", x=metrics+['Net Profit'], y=vals+[0], totals={"marker":{"color":"#FC8019"}}))
    st.plotly_chart(fig, use_container_width=True)

# --- Scenario Comparison Tab ---
with t2:
    st.subheader("Scenario Comparison (Net Profit)")
    scenario_comp = pd.DataFrame({
        "Scenario":["Normal","Heavy Rain","IPL Night"],
        "Net Profit":[]
    })
    net_profits=[]
    for scen in ["Normal","Heavy Rain","IPL Night"]:
        temp = df.copy()
        if scen=="Heavy Rain": temp['delivery_cost']*=1.3
        if scen=="IPL Night": temp['order_value']*=1.15
        temp['commission'] = temp['order_value']*0.18
        temp['ad_revenue'] = temp['order_value']*0.05
        temp['opex'] = 12
        temp['net_profit'] = (temp['commission'] + temp['ad_revenue'] + temp['delivery_fee']) - (temp['delivery_cost'] + temp['discount'] + temp['opex'])
        net_profits.append(temp['net_profit'].mean())
    scenario_comp['Net Profit'] = net_profits
    st.bar_chart(scenario_comp.set_index('Scenario'))

# --- Case Study Tab ---
with t3:
    st.header("Executive Case Study: Improving Instamart Profitability")
    st.caption("By Jagadeesh N | BBA, SRM IST (2026)")
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Problem Statement")
        st.write("Quick-commerce businesses operate on thin margins due to high last-mile costs and discount-heavy growth. Achieving Contribution Margin (CM2) positivity is the primary challenge.")
        st.subheader("Key Strategic Insights")
        st.success("AOV is the strongest lever: ₹50-₹70 increase impacts profit more than 20% volume growth.")
        st.info("Cost Efficiency: Reducing delivery costs by ₹10 via batching is more sustainable than raising fees.")
        st.error("Scale Paradox: High volume without healthy margins accelerates 'burn'.")
    with c2:
        st.subheader("Strategic Recommendations")
        st.markdown("""
        * Incentivize High-AOV Baskets via tiered delivery pricing
        * Optimize Delivery Densities with Demand Clustering & batching
        * Dynamic Discounting: Margin-Aware for high-margin categories
        """)
        st.subheader("Technical Execution")
        st.write("Python (Pandas) for modeling, Streamlit for dashboard UI.")

st.markdown("---")
st.caption("Business Analyst Portfolio | Jagadeesh N")
