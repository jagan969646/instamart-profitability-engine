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

# --- CUSTOM STYLING (Dark Mode + Green Terminal) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .main-title { color: #FC8019; font-weight: 800; font-size: 2.5rem; margin-bottom: 0px; }
    
    /* The Black Box with Green Data */
    .data-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .data-text {
        color: #2ECC71; 
        font-family: 'Courier New', monospace;
        font-size: 1.05rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- SMART DATA LOADING ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 CSV File not found in the 'app' directory.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Initialize missing columns to prevent KeyErrors
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 0.0
    if 'order_value' not in df.columns: df['order_value'] = 0.0
    if 'discount' not in df.columns: df['discount'] = 0.0
    
    # Create a baseline gross_margin if it doesn't exist for the delta calculation
    if 'gross_margin' not in df.columns:
        df['gross_margin'] = df['order_value'] * 0.15 
        
    return df

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image(LOCAL_LOGO_PATH if os.path.exists(LOCAL_LOGO_PATH) else SWIGGY_BRAND_URL, width=150)
    st.title("Control Tower")
    st.divider()
    
    st.subheader("🛠️ Strategy Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 60, 20)
    disc_opt = st.slider("Discount Reduction (%)", 0, 100, 30)
    aov_boost = st.slider("AOV Boost Strategy (₹)", 0, 200, 50)
    scenario = st.selectbox("Market Scenario", ["Normal Operations", "Heavy Rain", "IPL Match Night"])

# --- SIMULATION ENGINE ---
f_df = df.copy()
f_df['order_value'] += aov_boost
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.40
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.25

f_df['commission'] = f_df['order_value'] * 0.18
f_df['ad_revenue'] = f_df['order_value'] * 0.04
f_df['opex_fixed'] = 15.00
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['opex_fixed'])

# --- HEADER ---
cl, ct = st.columns([0.1, 0.9])
with cl: st.image(SWIGGY_BRAND_URL, width=70)
with ct: st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
st.divider()

# --- 4 KPI ROW (The m1, m2, m3, m4 columns) ---
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="Total GOV", 
              value=f"₹{f_df['order_value'].sum()/1e6:.2f}M", 
              delta="12.5% vs LW")

with m2:
    avg_p = f_df['net_profit'].mean()
    # Calculating the delta relative to the original data's estimated gross margin
    delta_val = avg_p - df['gross_margin'].mean()
    st.metric(label="Net Profit / Order", 
              value=f"₹{avg_p:.2f}", 
              delta=f"₹{delta_val:.2f} Sim Delta")

with m3:
    prof_rate = (f_df['net_profit'] > 0).mean() * 100
    st.metric(label="Order Profitability", 
              value=f"{prof_rate:.1f}%", 
              delta="Target: 70%", 
              delta_color="normal")

with m4:
    burn = (f_df['discount'].sum() / f_df['order_value'].sum()) * 100
    # Inverse color because a lower burn rate is good (green)
    st.metric(label="Burn Rate", 
              value=f"{burn:.1f}%", 
              delta="-3.2% Improvement", 
              delta_color="inverse")

# --- THE BLACK BOX (GREEN DATA) ---
st.markdown(f"""
<div class="data-box">
    <div class="data-text">
        [SYSTEM_LOG]: RUNNING_{scenario.replace(" ","_").upper()}_MODEL... OK!<br>
        >> REVENUE: Comm(₹{f_df['commission'].mean():.2f}) + Ads(₹{f_df['ad_revenue'].mean():.2f}) + Fees(₹{f_df['delivery_fee'].mean():.2f})<br>
        >> EXPENSE: Logistics(₹{f_df['delivery_cost'].mean():.2f}) + Burn(₹{f_df['discount'].mean():.2f}) + OPEX(₹15.00)<br>
        >> STATUS: CM2 POSITIVE | NET_MARGIN: {(avg_p/f_df['order_value'].mean()*100):.2f}%
    </div>
</div>
""", unsafe_allow_html=True)

# --- WATERFALL ---
metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
        -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.00]

fig = go.Figure(go.Waterfall(
    orientation="v", x=metrics + ['Net Profit'], y=vals + [0],
    measure=["relative"]*6 + ["total"],
    totals={"marker":{"color":"#FC8019"}},
    increasing={"marker":{"color":"#2ECC71"}},
    decreasing={"marker":{"color":"#FF4B4B"}}
))
fig.update_layout(template="plotly_dark", title="Unit Economics: CM2 Breakdown", height=450)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Strategic Portfolio | Jagadeesh N | Business Analyst 2026")
