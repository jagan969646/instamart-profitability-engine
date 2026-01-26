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
    .data-box {
        background-color: #000000;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .data-text {
        color: #2ECC71; 
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
        st.error(f"🚨 File not found: {DATA_PATH}")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    
    # CRITICAL FIX: Clean column names (removes spaces and makes lowercase)
    df.columns = df.columns.str.strip().str.lower()
    
    # Handle time if column exists
    if 'order_time' in df.columns:
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
# We use .get() or check columns to prevent crashes
f_df = df.copy()

# Ensure required columns exist, or create them with 0 if missing to avoid KeyError
cols_needed = ['order_value', 'delivery_fee', 'discount', 'delivery_cost']
for col in cols_needed:
    if col not in f_df.columns:
        st.error(f"❌ Missing column in CSV: '{col}'. Please check your file.")
        st.stop()

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
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['opex'])
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
st.markdown(f"""
<div class="data-box">
    <div class="data-text">
        <span class="data-label">>> SIMULATION ACTIVE: {scenario.upper()}</span><br>
        [REVENUE] Avg Comm: ₹{f_df['commission'].mean():.2f} | Ad Rev: ₹{f_df['ad_revenue'].mean():.2f} | Del. Fee: ₹{f_df['delivery_fee'].mean():.2f}<br>
        [COSTS] Del. Cost: ₹{f_df['delivery_cost'].mean():.2f} | Disc: ₹{f_df['discount'].mean():.2f} | OPEX: ₹12.00<br>
        [FINAL] NET PROFIT PER ORDER: ₹{f_df['net_profit'].mean():.2f}
    </div>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
t1, t2 = st.tabs(["📊 Financial Waterfall", "📖 Case Study Analysis"])

with t1:
    metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -12]
    
    fig = go.Figure(go.Waterfall(
        orientation="v", x=metrics + ['Net Profit'], y=vals + [0],
        measure=["relative"]*6 + ["total"],
        totals={"marker":{"color":"#FC8019"}},
        increasing={"marker":{"color":"#2ECC71"}},
        decreasing={"marker":{"color":"#FF4B4B"}}
    ))
    fig.update_layout(template="plotly_dark", title="Unit Economics Breakdown (CM2)", margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.header("Executive Case Study Summary")
    st.markdown("### Strategic Lever Impact")
    st.write("Current simulation shows that AOV and Delivery Fee optimization are the fastest paths to CM2 positivity.")

st.markdown("---")
st.caption("Developed by Jagadeesh N | Business Analyst Portfolio 2026")
