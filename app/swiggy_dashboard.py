import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS & ASSETS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
PDF_PATH = os.path.join(BASE_DIR, "JagadeeshN_SwiggyInstamart_Profitability_CaseStudy.pdf")
LOCAL_LOGO_PATH = os.path.join(BASE_DIR, "Logo.png")
SWIGGY_BRAND_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #121212; }
    .main-title { color: #FC8019; font-weight: 800; font-size: 2.5rem; margin-bottom: 0px; }
    
    /* KPI Boxes */
    .kpi-metric {
        background-color: #FC8019;
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: 800;
        font-size: 1.4rem;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .kpi-metric small { font-weight: 400; font-size: 0.85rem; display: block; margin-top: 5px; opacity: 0.9; }

    /* The Black Box with Green Data */
    .data-box {
        background-color: #000000;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .data-text {
        color: #2ECC71; /* Green Data */
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .data-label { color: #AAAAAA; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 Data file missing.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df['order_time'] = pd.to_datetime(df['order_time'])
    return df

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists(LOCAL_LOGO_PATH):
        st.image(LOCAL_LOGO_PATH, width=180)
    else:
        st.image(SWIGGY_BRAND_URL, width=100)
    
    st.title("Control Tower")
    
    st.subheader("🛠️ Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 15)
    disc_opt = st.slider("Discount Reduction (%)", 0, 100, 25)
    aov_boost = st.slider("AOV Boost (₹)", 0, 150, 40)
    scenario = st.selectbox("Market Conditions", ["Normal Operations", "Heavy Rain", "IPL Match Night"])

# --- SIMULATION ENGINE ---
f_df = df.copy()
f_df['order_value'] += aov_boost
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.35
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.20

f_df['commission'] = f_df['order_value'] * 0.18
f_df['ad_revenue'] = f_df['order_value'] * 0.05
f_df['opex'] = 12
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + f_df['opex'])
f_df['margin_pct'] = (f_df['net_profit'] / f_df['order_value']) * 100

# --- HEADER ---
c_l, c_t = st.columns([0.1, 0.9])
with c_l: st.image(SWIGGY_BRAND_URL, width=70)
with c_t: st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)

# --- 4 KPI ROW ---
k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown(f'<div class="kpi-metric">₹{f_df["order_value"].sum()/1e6:.2f}M<small>Projected GOV</small></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="kpi-metric">₹{f_df["net_profit"].mean():.2f}<small>Avg Profit / Order</small></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="kpi-metric">{f_df["margin_pct"].mean():.1f}%<small>Contribution Margin %</small></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="kpi-metric">{len(f_df):,}<small>Total Order Vol</small></div>', unsafe_allow_html=True)

# --- BLACK BOX (GREEN DATA) ---
st.markdown("""
<div class="data-box">
    <div class="data-text">
        <span class="data-label">>> RUNNING SIMULATION...</span><br>
        [REVENUE] Avg Comm: ₹{comm:.2f} | Ad Rev: ₹{ad:.2f} | Del. Fee: ₹{fee:.2f}<br>
        [COSTS] Del. Cost: ₹{cost:.2f} | Disc: ₹{disc:.2f} | OPEX: ₹{opex:.2f}<br>
        [FINAL] NET PROFIT PER ORDER: ₹{profit:.2f}
    </div>
</div>
""".format(
    comm=f_df['commission'].mean(),
    ad=f_df['ad_revenue'].mean(),
    fee=f_df['delivery_fee'].mean(),
    cost=f_df['delivery_cost'].mean(),
    disc=f_df['discount'].mean(),
    opex=f_df['opex'].mean(),
    profit=f_df['net_profit'].mean()
), unsafe_allow_html=True)

# --- TABS ---
t1, t2 = st.tabs(["📊 Financial Waterfall", "📖 Case Study Analysis"])

with t1:
    metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]
    fig = go.Figure(go.Waterfall(
        orientation="v", x=metrics + ['Net Profit'], y=vals + [0],
        measure=["relative"]*6 + ["total"],
        totals={"marker":{"color":"#FC8019"}},
        increasing={"marker":{"color":"#2ECC71"}},
        decreasing={"marker":{"color":"#FF4B4B"}}
    ))
    fig.update_layout(template="plotly_dark", title="Unit Economics Breakdown")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.header("Executive Case Study Summary")
    st.info("**Strategy:** Optimization focuses on increasing AOV and reducing high-burn discounting.")
    st.write("Full case study details are available via the PDF download in the sidebar.")

st.markdown("---")
st.caption("Developed by Jagadeesh N | Business Analyst Portfolio 2026")
