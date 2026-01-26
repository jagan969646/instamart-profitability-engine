import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- ADVANCED ENGINE CONFIG ---
st.set_page_config(page_title="Instamart Strategy v3.5", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png") 
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- ELITE EXECUTIVE CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0D1117; }
    
    /* Neumorphic Orange KPI Cards */
    .kpi-box {
        background: linear-gradient(145deg, #FC8019, #e67316);
        color: white !important;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 5px 5px 15px #06080a;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    .kpi-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.9; margin-bottom: 8px; color: white; }
    .kpi-value { font-size: 2.2rem; font-weight: 900; color: white; }
    .kpi-sub { font-size: 0.85rem; margin-top: 10px; background: rgba(0,0,0,0.2); border-radius: 20px; padding: 4px 12px; display: inline-block; color: white; }

    /* The 'Green Screen' Command Center */
    .terminal-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 20px;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(46, 204, 113, 0.1);
    }
    .terminal-line { color: #2ECC71; font-size: 1rem; line-height: 1.6; }
    .status-pulse { color: #2ECC71; animation: blinker 1.5s linear infinite; font-weight: bold; }
    @keyframes blinker { 50% { opacity: 0; } }

    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
</style>
""", unsafe_allow_html=True)

# --- DATA INTELLIGENCE ENGINE ---
@st.cache_data
def load_and_engineer():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 DATABASE_OFFLINE: swiggy_simulated_data.csv not found.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Auto-Schema Alignment
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 12.0
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    
    # Unit Economics Logic
    df['base_comm'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    df['base_opex'] = 14.0
    return df

# Fixed function call
df = load_and_engineer()

# --- SIDEBAR: STRATEGY WAR ROOM ---
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
    else:
        st.image(SWIGGY_URL, width=120)
        
    st.markdown("### 🏹 Strategic Levers")
    aov_target = st.select_slider("Basket Size Expansion (AOV)", options=[0, 20, 50, 100, 150], value=50)
    fee_optimization = st.slider("Dynamic Fee Premium (₹)", 0, 80, 25)
    discount_rationalization = st.slider("Subsidy Reduction (%)", 0, 100, 30)
    
    st.divider()
    st.markdown("### 🌏 Environment Controls")
    volatility = st.radio("Market Flux", ["Low", "High"], index=0)
    market_scenario = st.selectbox("Market Event", ["Neutral", "Monsoon Peak", "IPL Final Night"])

# --- SIMULATION ENGINE ---
f_df = df.copy()
noise_level = 0.02 if volatility == "Low" else 0.12
noise = np.random.normal(1, noise_level, len(f_df))

if market_scenario == "Monsoon Peak":
    f_df['delivery_cost'] *= (1.45 * noise)
    f_df['order_value'] *= 0.95
elif market_scenario == "IPL Final Night":
    f_df['order_value'] *= (1.25 * noise)
    f_df['delivery_cost'] *= 1.15

f_df['order_value'] += aov_target
f_df['delivery_fee'] += fee_optimization
f_df['discount'] *= (1 - discount_rationalization/100)

# Final CM2 Calculation
f_df['net_profit'] = (f_df['base_comm'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['base_opex'])

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='color: #FC8019; margin-bottom:0;'>Instamart Strategic War Room</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #666; margin-top:0;'>Executive Decision Support System v3.5</p>", unsafe_allow_html=True)

# --- 4 ORANGE KPI CARDS ---
k1, k2, k3, k4 = st.columns(4)
gov_total = (f_df['order_value'].sum() / 1e6)
avg_profit = f_df['net_profit'].mean()
cm_percent = (f_df['net_profit'].sum() / f_df['order_value'].sum()) * 100
alpha_score = (avg_profit / 14.5) * 100 

metrics = [
    ("Projected GOV", f"₹{gov_total:.2f}M", "↑ 18.4% vs Base"),
    ("CM2 / Order", f"₹{avg_profit:.2f}", f"Δ ₹{avg_profit-12:.1f} vs PY"),
    ("CM % Margin", f"{cm_percent:.1f}%", "Status: Healthy"),
    ("System Alpha", f"{alpha_score:.1f}pts", "Target: 120pts")
]

for col, (label, val, sub) in zip([k1, k2, k3, k4], metrics):
    col.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value if (value:=val) else 'N/A'}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
    """, unsafe_allow_html=True)

# --- COMMAND CENTER TERMINAL ---
st.markdown(f"""
<div class="terminal-box">
    <div class="terminal-line">
        <span class="status-pulse">●</span> LIVE_SIMULATION_ACTIVE...<br>
        > STRATEGY_LEVERS: AOV_BOOST(+₹{aov_target}) | FEE_OPT(+₹{fee_optimization}) | DISC_RED({discount_rationalization}%)<br>
        > ENVIRONMENTAL_CONTEXT: {market_scenario.upper()} | VOLATILITY: {volatility.upper()}<br>
        > <span style="color:#FFF">OUTCOME: Expected CM2 Positivity at ₹{avg_profit:.2f} per order.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- ANALYTICS TABS ---
t1, t2, t3 = st.tabs(["📊 Financial Waterfall", "📍 Zonal Analysis", "📈 Risk Profile"])

with t1:
    
    comps = ['Comm', 'Ads', 'Fees', 'Logistics', 'Discounts', 'OPEX']
    vals = [f_df['base_comm'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), 
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -14.0]
    
    fig_water = go.Figure(go.Waterfall(
        orientation="v", measure=["relative"]*6 + ["total"],
        x=comps + ['Final CM2'], y=vals + [0],
        totals={"marker":{"color":"#FC8019"}},
        decreasing={"marker":{"color":"#FF4B4B"}},
        increasing={"marker":{"color":"#2ECC71"}}
    ))
    fig_water.update_layout(template="plotly_dark", height=450, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_water, use_container_width=True)

with t2:
    z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
    fig_heat = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
    fig_heat.update_layout(template="plotly_dark", title="Hourly Profitability Matrix by Zone")
    st.plotly_chart(fig_heat, use_container_width=True)

with t3:
    fig_risk = px.histogram(f_df, x='net_profit', nbins=50, color_discrete_sequence=['#FC8019'],
                           title="Profitability Distribution (Monte Carlo Sample)")
    fig_risk.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_risk, use_container_width=True)

st.markdown("---")
st.caption("Developed by Jagadeesh N | Business Analyst & Portfolio Case Study 2026")
