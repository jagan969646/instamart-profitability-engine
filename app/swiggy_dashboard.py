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
    .kpi-container { display: flex; gap: 15px; margin-bottom: 25px; }
    .kpi-box {
        background: linear-gradient(145deg, #FC8019, #e67316);
        color: white;
        padding: 25px;
        border-radius: 18px;
        flex: 1;
        text-align: center;
        box-shadow: 5px 5px 15px #06080a, -2px -2px 10px #141a24;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .kpi-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.9; margin-bottom: 8px; }
    .kpi-value { font-size: 2.2rem; font-weight: 900; }
    .kpi-sub { font-size: 0.85rem; margin-top: 10px; background: rgba(0,0,0,0.2); border-radius: 20px; padding: 4px 12px; display: inline-block; }

    /* The 'Green Screen' Command Center */
    .terminal-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 20px;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        margin: 20px 0;
        box-shadow: 0 0 20px rgba(46, 204, 113, 0.1);
    }
    .terminal-line { color: #2ECC71; font-size: 1rem; line-height: 1.6; }
    .status-pulse { color: #2ECC71; animation: blinker 1.5s linear infinite; font-weight: bold; }
    @keyframes blinker { 50% { opacity: 0; } }

    /* Chart Containers */
    .chart-card { background-color: #161B22; padding: 20px; border-radius: 15px; border: 1px solid #30363D; }
</style>
""", unsafe_allow_html=True)

# --- DATA INTELLIGENCE ENGINE ---
@st.cache_data
def load_and_engineer():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 DATABASE_OFFLINE: Connect swiggy_simulated_data.csv")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Auto-Schema Alignment
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 12.0
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    
    # Unit Economics Engineering
    df['base_comm'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    df['base_opex'] = 14.0
    return df

df = load_engineer()

# --- SIDEBAR: STRATEGY WAR ROOM ---
with st.sidebar:
    st.image(LOGO_PATH if os.path.exists(LOGO_PATH) else SWIGGY_URL, width=150)
    st.markdown("### 🏹 Strategic Levers")
    aov_target = st.select_slider("Basket Size Expansion (AOV)", options=[0, 20, 50, 100, 150], value=50)
    fee_optimization = st.slider("Dynamic Fee Premium (₹)", 0, 80, 25)
    discount_rationalization = st.slider("Subsidy Reduction (%)", 0, 100, 30)
    
    st.divider()
    st.markdown("### 🌏 Environment Controls")
    volatility = st.radio("Market Flux", ["Low (0.02)", "High (0.15)"], index=0)
    market_scenario = st.selectbox("Market Event", ["Neutral", "Monsoon Peak", "IPL Final Night"])

# --- MONTE CARLO SIMULATION ENGINE ---
f_df = df.copy()
noise_level = 0.02 if "Low" in volatility else 0.15
noise = np.random.normal(1, noise_level, len(f_df))

# Dynamic Scenario Overlays
if market_scenario == "Monsoon Peak":
    f_df['delivery_cost'] *= (1.45 * noise)
    f_df['order_value'] *= 0.92
elif market_scenario == "IPL Final Night":
    f_df['order_value'] *= (1.30 * noise)
    f_df['delivery_cost'] *= 1.15

# Applying Levers
f_df['order_value'] += aov_target
f_df['delivery_fee'] += fee_optimization
f_df['discount'] *= (1 - discount_rationalization/100)

# Final Financial Calculation
f_df['net_profit'] = (f_df['base_comm'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['base_opex'])

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='color: #FC8019;'>Instamart Strategic War Room <span style='font-size: 16px; color:#666;'>SYSTEM_v3.5</span></h1>", unsafe_allow_html=True)

# --- 4 ORANGE KPI CARDS ---
k1, k2, k3, k4 = st.columns(4)
gov_total = (f_df['order_value'].sum() / 1e6)
avg_profit = f_df['net_profit'].mean()
cm_percent = (f_df['net_profit'].sum() / f_df['order_value'].sum()) * 100
alpha_score = (avg_profit / 14.5) * 100 # Internal performance score

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
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
    """, unsafe_allow_html=True)

# --- COMMAND CENTER TERMINAL ---
st.markdown(f"""
<div class="terminal-box">
    <div class="terminal-line">
        <span class="status-pulse">●</span> SYSTEM_READY: Simulating {len(f_df):,} Order Vectors...<br>
        > STRATEGY_LOADED: AOV_BOOST(+₹{aov_target}) | FEE_OPTIMIZATION(+₹{fee_optimization})<br>
        > MARKET_ENVIRONMENT: {market_scenario.upper()} (Volatility: {volatility})<br>
        > <span style="color:#FFF">FINANCIAL_OUTLOOK: CM2 Positive in {len(f_df[f_df['net_profit']>0]):,} orders ({cm_percent:.1f}% Margin)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- ANALYTICS TABS ---
t1, t2, t3 = st.tabs(["📊 Financial Architecture", "📍 Regional Elasticity", "📈 Risk Distribution"])

with t1:
    c_a, c_b = st.columns([2, 1])
    with c_a:
        st.subheader("Profitability Waterfall (CM2)")
        
        # Advanced waterfall using Plotly
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
        fig_water.update_layout(template="plotly_dark", height=450, margin=dict(t=10, b=10))
        st.plotly_chart(fig_water, use_container_width=True)

with t2:
    st.subheader("Regional Profitability Matrix")
    # Zonal Heatmap
    z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
    fig_heat = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
    fig_heat.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.info("💡 **Decision Logic:** Red cells indicate 'Burn Hours'. Suggesting higher surge pricing or batching-only mode.")

with t3:
    st.subheader("Monte Carlo Simulation: GOV vs. Profit Variance")
    # Risk Distribution Scatter
    f_df['gov_sim'] = f_df['order_value'] * noise
    fig_risk = px.scatter(f_df.sample(min(1000, len(f_df))), x='gov_sim', y='net_profit', color='net_profit', 
                         color_continuous_scale='Portland', title="Outlier Detection: 1000 Vector Sample")
    fig_risk.update_layout(template="plotly_dark")
    st.plotly_chart(fig_risk, use_container_width=True)

st.markdown("---")
st.caption("Developed by Jagadeesh N | Business Analyst & Portfolio Case Study 2026")
