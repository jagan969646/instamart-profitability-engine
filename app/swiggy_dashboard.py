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

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .main-title { color: #FC8019; font-weight: 800; font-size: 2.5rem; margin-bottom: 0px; }
    
    /* 4 KPI Cards */
    .kpi-metric {
        background-color: #FC8019;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: 800;
        font-size: 1.5rem;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-metric small { font-weight: 400; font-size: 0.85rem; display: block; margin-top: 5px; opacity: 0.9; }

    /* The Black Box with Green Data */
    .data-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .data-text {
        color: #2ECC71; 
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .data-label { color: #555; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 Data file not found.")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # FIX: If delivery_fee is missing, initialize it at 0 so the slider can add to it
    if 'delivery_fee' not in df.columns:
        df['delivery_fee'] = 0.0
        
    return df

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists(LOCAL_LOGO_PATH):
        st.image(LOCAL_LOGO_PATH, width=180)
    else:
        st.image(SWIGGY_BRAND_URL, width=100)
    
    st.title("Control Tower")
    st.divider()
    
    st.subheader("🛠️ Strategy Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 60, 20)
    disc_opt = st.slider("Discount Reduction (%)", 0, 100, 30)
    aov_boost = st.slider("AOV Boost Strategy (₹)", 0, 200, 50)
    scenario = st.selectbox("Market Scenario", ["Normal Operations", "Heavy Rain", "IPL Match Night"])

# --- SIMULATION ENGINE ---
f_df = df.copy()

# Apply User Levers
f_df['order_value'] += aov_boost
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

# Apply Scenario Logic
if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.40
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.25

# Standard Financial Ratios
f_df['commission'] = f_df['order_value'] * 0.18
f_df['ad_revenue'] = f_df['order_value'] * 0.04
f_df['opex_fixed'] = 15.00 # Dark Store processing costs

# CM2 Calculation
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['opex_fixed'])

f_df['margin_pct'] = (f_df['net_profit'] / f_df['order_value']) * 100

# --- HEADER ---
c1, c2 = st.columns([0.1, 0.9])
with c1: st.image(SWIGGY_BRAND_URL, width=70)
with c2: st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
st.divider()

# --- 4 KPI ROW ---
k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown(f'<div class="kpi-metric">₹{f_df["order_value"].sum()/1e6:.2f}M<small>Total GOV</small></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="kpi-metric">₹{f_df["net_profit"].mean():.2f}<small>Avg Profit/Order</small></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="kpi-metric">{f_df["margin_pct"].mean():.1f}%<small>Contribution Margin</small></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="kpi-metric">{len(f_df):,}<small>Orders Analyzed</small></div>', unsafe_allow_html=True)

# --- THE BLACK BOX (GREEN DATA) ---
st.markdown(f"""
<div class="data-box">
    <div class="data-text">
        <span style="color:#555"># EXECUTION_LOG: SCENARIO_{scenario.replace(" ","_").upper()}</span><br>
        [REVENUE] Commission: ₹{f_df['commission'].mean():.2f} | Ad_Rev: ₹{f_df['ad_revenue'].mean():.2f} | Del_Fee: ₹{f_df['delivery_fee'].mean():.2f}<br>
        [EXPENSE] Del_Cost: ₹{f_df['delivery_cost'].mean():.2f} | Discount: ₹{f_df['discount'].mean():.2f} | OPEX: ₹15.00<br>
        [SUMMARY] CM2_PROFIT: <span style="font-weight:bold">₹{f_df['net_profit'].mean():.2f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- VISUALS ---
t1, t2 = st.tabs(["📊 Financial Waterfall", "📖 Case Study"])

with t1:
    metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.00]
    
    fig = go.Figure(go.Waterfall(
        orientation="v",
        x=metrics + ['Net Profit'],
        y=vals + [0],
        measure=["relative"]*6 + ["total"],
        totals={"marker":{"color":"#FC8019"}},
        increasing={"marker":{"color":"#2ECC71"}},
        decreasing={"marker":{"color":"#FF4B4B"}}
    ))
    
    fig.update_layout(template="plotly_dark", title="Unit Economics: Contribution Margin 2 Breakdown", height=500)
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.subheader("Profitability Analysis Summary")
    st.markdown("""
    * **Observation:** Increasing AOV (Basket Size) is the most efficient way to dilute fixed delivery costs.
    * **Action:** Shift from generic discounting to tiered loyalty rewards for orders >₹500.
    """)

st.markdown("---")
st.caption("Strategic Analyst Portfolio | Jagadeesh N")
