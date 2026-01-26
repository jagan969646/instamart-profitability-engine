import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOCAL_LOGO_PATH = os.path.join(BASE_DIR, "Logo.png")
SWIGGY_BRAND_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- CUSTOM STYLING (The Orange & Black Aesthetic) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    
    /* Orange KPI Card Styling */
    .kpi-metric {
        background-color: #FC8019 !important;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(252, 128, 25, 0.3);
        text-align: center;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #ffffff !important;
        opacity: 0.9;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* The Black Box with Green Terminal Data */
    .data-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .data-text {
        color: #2ECC71; 
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 CSV file not found.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 0.0
    return df

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image(LOCAL_LOGO_PATH if os.path.exists(LOCAL_LOGO_PATH) else SWIGGY_BRAND_URL, width=180)
    st.title("Control Tower")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 60, 20)
    disc_opt = st.slider("Discount Reduction (%)", 0, 100, 30)
    aov_boost = st.slider("AOV Boost Strategy (₹)", 0, 200, 50)
    scenario = st.selectbox("Market Scenario", ["Normal Operations", "Heavy Rain", "IPL Match Night"])

# --- SIMULATION ENGINE ---
f_df = df.copy()
f_df['order_value'] += aov_boost
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

if scenario == "Heavy Rain": f_df['delivery_cost'] *= 1.40
elif scenario == "IPL Match Night": f_df['order_value'] *= 1.25

f_df['commission'] = f_df['order_value'] * 0.18
f_df['ad_revenue'] = f_df['order_value'] * 0.04
f_df['opex'] = 15.0
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + f_df['opex'])

# --- KPI CALCULATIONS ---
total_gov = f_df['order_value'].sum() / 1e6
avg_profit = f_df['net_profit'].mean()
prof_rate = (f_df['net_profit'] > 0).mean() * 100
burn_rate = (f_df['discount'].sum() / f_df['order_value'].sum()) * 100

# --- UI HEADER ---
st.markdown(f"<h1 style='color: #FC8019;'>Instamart Strategy Engine <span style='font-size:15px; color:#555;'>v2.0</span></h1>", unsafe_allow_html=True)

# --- 4 ORANGE KPI CARDS ---
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("Total GOV", f"₹{total_gov:.2f}M"),
    ("Net Profit/Order", f"₹{avg_profit:.2f}"),
    ("Order Profitability", f"{prof_rate:.1f}%"),
    ("Burn Rate", f"{burn_rate:.1f}%")
]

for col, (label, value) in zip([m1, m2, m3, m4], metrics):
    col.markdown(f"""
        <div class="kpi-metric">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- THE BLACK BOX (GREEN DATA) ---
st.markdown(f"""
<div class="data-box">
    <div class="data-text">
        [SYSTEM_LOG] SIMULATION_RUN: {scenario.upper()}<br>
        [REVENUE] Avg_Comm: ₹{f_df['commission'].mean():.2f} | Ad_Rev: ₹{f_df['ad_revenue'].mean():.2f} | Del_Fee: ₹{f_df['delivery_fee'].mean():.2f}<br>
        [EXPENSE] Delivery: ₹{f_df['delivery_cost'].mean():.2f} | Discount: ₹{f_df['discount'].mean():.2f} | OPEX: ₹15.00<br>
        [SUCCESS] TARGET_METRIC_DELTA: ₹{avg_profit - df['contribution_margin'].mean() if 'contribution_margin' in df.columns else 0:.2f}
    </div>
</div>
""", unsafe_allow_html=True)

# --- WATERFALL CHART ---
st.subheader("Unit Economics Breakdown")
metrics_list = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
        -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0]

fig = go.Figure(go.Waterfall(
    orientation="v", x=metrics_list + ['Net Profit'], y=vals + [0],
    measure=["relative"]*6 + ["total"],
    totals={"marker":{"color":"#FC8019"}},
    increasing={"marker":{"color":"#2ECC71"}},
    decreasing={"marker":{"color":"#FF4B4B"}}
))
fig.update_layout(template="plotly_dark", height=450, margin=dict(t=20, b=20, l=10, r=10))
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Developed by Jagadeesh N | Business Analyst Portfolio 2026")
