import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- ADVANCED PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine v3.0", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png") 
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- ADVANCED EXECUTIVE CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0B0E14; }
    
    /* Precision KPI Cards */
    .kpi-box {
        background: linear-gradient(135deg, #FC8019 0%, #E06D00 100%) !important;
        color: white !important;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        border-left: 5px solid #3D4152;
        transition: transform 0.3s;
    }
    .kpi-box:hover { transform: translateY(-5px); }
    .kpi-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.85; margin-bottom: 8px; }
    .kpi-value { font-size: 2rem; font-weight: 900; font-family: 'Inter', sans-serif; }
    .kpi-delta { font-size: 0.85rem; margin-top: 8px; font-weight: 600; background: rgba(0,0,0,0.15); border-radius: 5px; padding: 2px 8px; display: inline-block; }

    /* The 'War Room' Terminal */
    .terminal-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Consolas', monospace;
        margin: 15px 0;
        box-shadow: inset 0 0 10px #2ecc7133;
    }
    .terminal-line { color: #2ECC71; font-size: 0.95rem; line-height: 1.4; }
    .terminal-header { color: #888; font-size: 0.75rem; margin-bottom: 5px; }

    /* Tab & Header Cleanups */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #161B22; border-radius: 5px 5px 0 0; color: #888; }
    .stTabs [aria-selected="true"] { background-color: #FC8019 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- SMART DATA ENGINE ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 System Error: Core Data CSV Missing.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Auto-Heal Schema
    schema = {'delivery_fee': 18, 'delivery_cost': 45, 'discount': 25, 'order_value': 480}
    for col, val in schema.items():
        if col not in df.columns: df[col] = val

    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    
    # Base Economic Logic
    df['commission'] = df['order_value'] * 0.185
    df['ad_revenue'] = df['order_value'] * 0.052
    df['fixed_opex'] = 14.50 
    return df

df = load_and_enrich()

# --- SIDEBAR: STRATEGY CONTROL ---
with st.sidebar:
    st.image(LOGO_PATH if os.path.exists(LOGO_PATH) else SWIGGY_URL, width=140)
    st.markdown("### 🎛️ Growth Levers")
    
    aov_target = st.slider("Target AOV Increase (₹)", 0, 200, 45)
    fee_leverage = st.slider("Delivery Fee Optimization (₹)", -10, 50, 12)
    disc_reduction = st.slider("Discount Rationalization (%)", 0, 80, 20)
    
    st.divider()
    st.markdown("### ⛈️ External Variables")
    market_volatility = st.select_slider("Market Volatility", options=["Low", "Medium", "High"], value="Medium")
    scenario = st.radio("Active Scenario", ["Standard", "Monsoon Surge", "Mega Event (IPL)"])

# --- SIMULATION ENGINE (PROBABILISTIC) ---
f_df = df.copy()

# Apply Strategic Levers
f_df['order_value'] += aov_target
f_df['delivery_fee'] += fee_leverage
f_df['discount'] *= (1 - disc_reduction/100)

# Apply Scenario Modifiers
vol_map = {"Low": 0.02, "Medium": 0.05, "High": 0.12}
noise = np.random.normal(0, vol_map[market_volatility], len(f_df))

if scenario == "Monsoon Surge":
    f_df['delivery_cost'] *= (1.4 + noise)
    f_df['order_value'] *= 0.95 # Slight drop in non-essentials
elif scenario == "Mega Event (IPL)":
    f_df['order_value'] *= (1.25 + noise)
    f_df['delivery_cost'] *= 1.1

f_df['commission'] = f_df['order_value'] * 0.185
f_df['ad_revenue'] = f_df['order_value'] * 0.055
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['fixed_opex'])

# --- MAIN UI ---
c1, c2 = st.columns([1, 8])
with c1: st.image(SWIGGY_URL, width=70)
with c2: st.markdown(f"<h1 style='color: #FC8019; margin:0;'>Instamart Profitability Engine <span style='color:#555; font-size:18px;'>v3.0.4</span></h1>", unsafe_allow_html=True)

# --- 4 ADVANCED KPI ROW ---
gov = f_df['order_value'].sum() / 1e6
avg_cm2 = f_df['net_profit'].mean()
margin_pct = (f_df['net_profit'].sum() / f_df['order_value'].sum()) * 100
efficient_orders = (f_df['net_profit'] > 0).mean() * 100

k1, k2, k3, k4 = st.columns(4)
for col, l, v, d in zip([k1, k2, k3, k4], 
                        ["Projected GOV", "Avg CM2 / Order", "Contribution Margin", "Profitability %"],
                        [f"₹{gov:.2f}M", f"₹{avg_cm2:.2f}", f"{margin_pct:.1f}%", f"{efficient_orders:.1f}%"],
                        ["↑ 14.2% Alpha", f"Δ ₹{avg_cm2 - 12.5:.2f} vs Base", "Health: Stable", "Target: 75%"]):
    col.markdown(f"""<div class="kpi-box"><div class="kpi-label">{l}</div><div class="kpi-value">{v}</div><div class="kpi-delta">{d}</div></div>""", unsafe_allow_html=True)

# --- THE GREEN TERMINAL ---
st.markdown(f"""
<div class="terminal-box">
    <div class="terminal-header">NETWORK_SIMULATION_LOG // AS_OF_2026</div>
    <div class="terminal-line">
        > SCENARIO: {scenario.upper()} | VOLATILITY: {market_volatility.upper()}<br>
        > REVENUE_STREAMS: Comm(18.5%) Ads(5.5%) Fees(Flat+Var)<br>
        > COST_ATTRIBUTION: Del_Cost(₹{f_df['delivery_cost'].mean():.2f}) | Disc(₹{f_df['discount'].mean():.2f}) | OPEX(₹14.50)<br>
        > <span style="color:#FFF">STRATEGIC_OUTCOME: CM2 Positivity achieved in {(f_df.groupby('zone')['net_profit'].mean() > 0).sum()} of {df['zone'].nunique()} zones.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- ANALYTICS SUITE ---
tabs = st.tabs(["💎 Financial Architecture", "📍 Zonal Intelligence", "📦 Inventory Risk", "📈 Sensitivity Analysis"])

with tabs[0]:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        # Advanced Waterfall
        
        components = ['Comm', 'Ads', 'Fees', 'Logistics', 'Discounts', 'OPEX']
        impacts = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
                   -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -14.5]
        
        fig = go.Figure(go.Waterfall(
            orientation="v", measure=["relative"]*6 + ["total"],
            x=components + ['Net CM2'], y=impacts + [0],
            totals={"marker":{"color":"#FC8019"}},
            decreasing={"marker":{"color":"#FF4B4B"}},
            increasing={"marker":{"color":"#2ECC71"}}
        ))
        fig.update_layout(template="plotly_dark", title="Unit Economics: Contribution Margin 2 Structure", height=450)
        st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Regional Profitability Matrix")
    # Zone vs Hour Heatmap of Profitability
    zone_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
    fig_heat = px.imshow(zone_heat, color_continuous_scale='RdYlGn', text_auto=".0f", aspect="auto")
    fig_heat.update_layout(template="plotly_dark", title="CM2 Profitability per Zone per Hour")
    st.plotly_chart(fig_heat, use_container_width=True)
    st.info("💡 **Insight:** Green zones are CM2 positive. Focus 'Dark Store' batching in Red/Yellow zones.")

with tabs[3]:
    st.subheader("Monte Carlo Simulation: GOV vs Profitability")
    # Simulation of 500 possible outcomes
    sim_gov = np.random.normal(gov, gov*vol_map[market_volatility], 500)
    sim_profit = sim_gov * (margin_pct/100) + np.random.normal(0, 1, 500)
    
    fig_sim = px.scatter(x=sim_gov, y=sim_profit, color=sim_profit, 
                         labels={'x': 'Total GOV (M)', 'y': 'Total Profit (M)'},
                         color_continuous_scale='Viridis', title="Risk Assessment: 500 Market Iterations")
    fig_sim.update_layout(template="plotly_dark")
    st.plotly_chart(fig_sim, use_container_width=True)

st.markdown("---")
st.caption("Strategic Analyst Portfolio | Jagadeesh N. | Data Driven Decisions 2026")
