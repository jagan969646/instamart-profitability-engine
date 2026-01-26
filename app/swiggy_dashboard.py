import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS & ASSETS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
PDF_PATH = os.path.join(BASE_DIR, "JagadeeshN_SwiggyInstamart_Profitability_CaseStudy.pdf")

# Direct GitHub link to your Logo to ensure it always loads
LOGO_URL = "https://raw.githubusercontent.com/jagan969646/instamart-profitability-engine/main/app/Logo.png"
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
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 Missing {DATA_PATH}")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    
    # List of required columns for the simulation logic
    required_cols = {
        'delivery_fee': 15, 
        'delivery_cost': 40, 
        'discount': 20,
        'order_value': 450, 
        'category': 'FMCG', 
        'freshness_hrs_left': 24,
        'zone': 'Cluster A'
    }

    # If the column is missing from your CSV, this adds it with a default value
    for col, default_val in required_cols.items():
        if col not in df.columns:
            df[col] = default_val

    # Ensure order_time is in datetime format
    if 'order_time' in df.columns:
        df['order_time'] = pd.to_datetime(df['order_time'])
    else:
        # Create a dummy date column if it doesn't exist
        df['order_time'] = pd.Timestamp.now()

    # Pre-calculate baseline metrics for the simulation
    df['commission'] = df['order_value'] * 0.18
    df['ad_revenue'] = df['order_value'] * 0.05
    df['opex'] = 12
    
    return df
df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    # Try loading your custom logo first, fallback to brand logo
    st.image(LOGO_URL, width=150, caption="Instamart Engine", use_container_width=False)
    st.title("Control Tower")

    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            st.download_button(label="📄 Download Case Study PDF", data=f, file_name="JagadeeshN_Analysis.pdf")

    st.divider()
    st.subheader("🛠️ Profitability Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 5)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 20)
    aov_boost = st.slider("AOV Expansion Strategy (₹)", 0, 100, 0)
    scenario = st.selectbox("Conditions", ["Normal Operations", "Heavy Rain", "IPL Match Night"])

# --- SIMULATION ENGINE ---
f_df = df.copy()
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)
f_df['order_value'] += aov_boost

if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.3
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.15

f_df['commission'] = f_df['order_value'] * 0.18
f_df['ad_revenue'] = f_df['order_value'] * 0.05
f_df['opex'] = 12
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + f_df['opex'])

# --- HEADER ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image(SWIGGY_BRAND_URL, width=80)
with col_text:
    st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
st.divider()

# --- KPI ROW ---
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f'<div class="kpi-metric">₹{f_df["order_value"].sum()/1e6:.2f}M<br><small>Total GOV</small></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-metric">₹{f_df["net_profit"].mean():.2f}<br><small>Avg Profit/Order (CM2)</small></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-metric">{len(f_df):,}<br><small>Orders Analyzed</small></div>', unsafe_allow_html=True)

# --- TABS ---
t1, t2, t3 = st.tabs(["📊 Financials", "📈 Scenarios", "📖 Case Study"])

with t1:
    st.subheader("Unit Economics Waterfall")
    metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]
    fig = go.Figure(go.Waterfall(orientation="v", x=metrics + ['Net Profit'], y=vals + [0], totals={"marker":{"color":"#FC8019"}}))
    st.plotly_chart(fig, use_container_width=True)

with t3:
    st.header("Executive Case Study: Improving Instamart Profitability [cite: 1]")
    st.caption("By Jagadeesh N | BBA, SRM IST (2026) [cite: 2]")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 Problem Statement [cite: 4]")
        st.write("Quick-commerce businesses operate on thin margins due to high last-mile costs and discount-heavy growth[cite: 5]. Achieving Contribution Margin (CM2) positivity is the primary challenge[cite: 6].")
        
        st.subheader("💡 Key Strategic Insights [cite: 12]")
        st.success("**AOV is the Strongest Lever:** A ₹50-₹70 increase in AOV (via cross-selling) has a higher impact on profitability than a 20% volume growth.")
        st.info("**Cost Efficiency:** Reducing delivery costs by ₹10 via batching is 2x more sustainable than increasing fees[cite: 14].")
        st.error("**Scale Paradox:** High volume without healthy margins actually accelerates 'burn'[cite: 15].")

    with c2:
        st.subheader("🚀 Strategic Recommendations [cite: 17]")
        st.markdown("""
        * **Incentivize High-AOV Baskets:** Use tiered delivery pricing for orders above ₹500[cite: 18].
        * **Optimize Delivery Densities:** Prioritize 'Demand Clustering' and multi-order batching[cite: 19].
        * **Dynamic Discounting:** Transition to 'Margin-Aware' discounting for high-margin categories[cite: 20].
        """)
        
        st.subheader("🛠️ Technical Execution [cite: 21]")
        st.write("Developed using Python (Pandas) for financial modeling and Streamlit for the executive UI.")

st.markdown("---")
st.caption("Business Analyst Portfolio | Jagadeesh N [cite: 28]")

