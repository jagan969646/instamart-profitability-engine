import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- ADVANCED ENGINE CONFIG ---
st.set_page_config(page_title="Instamart Strategy v4.0", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png") 
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- ELITE EXECUTIVE CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0A0C10; }
    
    /* Neumorphic Orange KPI Cards */
    .kpi-box {
        background: linear-gradient(135deg, #FC8019 0%, #D86910 100%);
        color: white !important;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 8px 8px 20px #040506, -2px -2px 10px #1a1f28;
        border: 1px solid rgba(255,255,255,0.05);
        transition: 0.3s ease;
    }
    .kpi-box:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(252, 128, 25, 0.4); }
    .kpi-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.9; margin-bottom: 8px; font-weight: 600; }
    .kpi-value { font-size: 2.2rem; font-weight: 900; }
    .kpi-sub { font-size: 0.8rem; margin-top: 10px; background: rgba(0,0,0,0.25); border-radius: 20px; padding: 4px 12px; display: inline-block; }

    /* The 'Green Screen' Command Center */
    .terminal-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 20px;
        border-radius: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        margin-bottom: 25px;
        box-shadow: inset 0 0 15px rgba(46, 204, 113, 0.2);
    }
    .terminal-line { color: #2ECC71; font-size: 0.95rem; line-height: 1.6; }
    .status-pulse { color: #2ECC71; animation: blinker 2s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }

    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
</style>
""", unsafe_allow_html=True)

# --- DATA INTELLIGENCE ENGINE ---
@st.cache_data
def load_and_engineer():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 DATABASE_OFFLINE: Ensure swiggy_simulated_data.csv is in the directory.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Auto-Schema Alignment & Heuristics
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 15.0
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    
    # Financial Base Engineering
    df['base_comm'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    df['fixed_opex'] = 14.0
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGY CONTROL TOWER ---
with st.sidebar:
    st.image(LOGO_PATH if os.path.exists(LOGO_PATH) else SWIGGY_URL, width=150)
    st.markdown("### 🏹 Profitability Levers")
    
    aov_expansion = st.select_slider("Basket Size Strategy (AOV)", options=[0, 25, 50, 75, 100, 150], value=50)
    fee_leverage = st.slider("Dynamic Surge Premium (₹)", 0, 100, 30)
    disc_rationalization = st.slider("Subsidy Optimization (%)", 0, 100, 20)
    
    st.divider()
    st.markdown("### 🌏 Risk Environment")
    market_flux = st.select_slider("Market Volatility", options=["Stable", "Moderate", "Extreme"], value="Moderate")
    scenario = st.selectbox("Active Market Scenario", ["Neutral", "Monsoon Peak", "Flash Sale Event"])

# --- PROBABILISTIC SIMULATION ENGINE ---
f_df = df.copy()

# Market Volatility Mapping
vol_map = {"Stable": 0.02, "Moderate": 0.06, "Extreme": 0.15}
noise = np.random.normal(1, vol_map[market_flux], len(f_df))

# Apply Scenario Modifiers
if scenario == "Monsoon Peak":
    f_df['delivery_cost'] *= (1.45 * noise)
    f_df['order_value'] *= 0.95
elif scenario == "Flash Sale Event":
    f_df['order_value'] *= (1.30 * noise)
    f_df['delivery_cost'] *= 1.20

# Apply Strategic Levers
f_df['order_value'] += aov_expansion
f_df['delivery_fee'] += fee_leverage
f_df['discount'] *= (1 - disc_rationalization/100)

# Final CM2 Architecture
f_df['net_profit'] = (f_df['base_comm'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['fixed_opex'])

# --- MAIN DASHBOARD INTERFACE ---
st.markdown("<h1 style='color: #FC8019; margin-bottom:0;'>Instamart Strategic War Room <span style='font-size: 14px; color:#555;'>SYSTEM_v4.0.1</span></h1>", unsafe_allow_html=True)

# --- 4 ORANGE KPI CARDS ---
k1, k2, k3, k4 = st.columns(4)
gov_total = (f_df['order_value'].sum() / 1e6)
avg_profit = f_df['net_profit'].mean()
cm_margin = (f_df['net_profit'].sum() / f_df['order_value'].sum()) * 100
system_alpha = (avg_profit / 15.0) * 100 # Performance against internal benchmark

metrics = [
    ("Projected GOV", f"₹{gov_total:.2f}M", "↑ 14.5% vs LW"),
    ("CM2 / Order", f"₹{avg_profit:.2f}", f"Δ ₹{avg_profit-12.5:.1f} vs Baseline"),
    ("CM % Margin", f"{cm_margin:.1f}%", "Health: Optimal"),
    ("System Alpha", f"{system_alpha:.1f} pts", "Target: 110 pts")
]

for col, (label, val, sub) in zip([k1, k2, k3, k4], metrics):
    col.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
    """, unsafe_allow_html=True)

# --- THE GREEN COMMAND TERMINAL ---
st.markdown(f"""
<div class="terminal-box">
    <div class="terminal-line">
        <span class="status-pulse">●</span> SIMULATION_LOG: {scenario.upper()} // VOLATILITY_{market_flux.upper()}<br>
        > LEVERS: AOV(+₹{aov_expansion}) | FEE(+₹{fee_leverage}) | DISC_RED({disc_rationalization}%)<br>
        > REVENUE_VECTOR: Comm(₹{f_df['base_comm'].mean():.2f}) | Ads(₹{f_df['ad_rev'].mean():.2f}) | Fee(₹{f_df['delivery_fee'].mean():.2f})<br>
        > <span style="color:#FFF">OUTCOME_ANALYSIS: CM2 POSITIVITY ACHIEVED AT ₹{avg_profit:.2f} AVG PER VECTOR.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- ANALYTICS SUITE ---
tabs = st.tabs(["💎 Financial Architecture", "📍 Regional Intelligence", "📈 Monte Carlo Risk"])

with tabs[0]:
    st.subheader("Unit Economics: CM2 Waterfall Structure")
    
    comps = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discounts', 'OPEX']
    vals = [f_df['base_comm'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), 
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -14.0]
    
    fig_water = go.Figure(go.Waterfall(
        orientation="v", measure=["relative"]*6 + ["total"],
        x=comps + ['Final CM2'], y=vals + [0],
        totals={"marker":{"color":"#FC8019"}},
        decreasing={"marker":{"color":"#FF4B4B"}},
        increasing={"marker":{"color":"#2ECC71"}}
    ))
    fig_water.update_layout(template="plotly_dark", height=450, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_water, use_container_width=True)

with tabs[1]:
    st.subheader("Hourly Zonal Profitability Heatmap")
    z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
    fig_heat = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
    fig_heat.update_layout(template="plotly_dark", title="CM2 Net per Region/Time Window")
    st.plotly_chart(fig_heat, use_container_width=True)
    st.info("💡 **Strategy Hint:** Deep Red cells indicate 'Burn Zones'. Consider implementing batch-delivery rules for these windows.")

with tabs[2]:
    st.subheader("Monte Carlo Simulation: Profit Variance Distribution")
    
    fig_risk = px.histogram(f_df, x='net_profit', nbins=100, color_discrete_sequence=['#FC8019'],
                           marginal="box", title="Monte Carlo Vector Outcomes")
    fig_risk.update_layout(template="plotly_dark")
    st.plotly_chart(fig_risk, use_container_width=True)

st.markdown("---")
st.caption("Strategic Analyst Portfolio | Jagadeesh N. | Data Driven Decisions 2026")
