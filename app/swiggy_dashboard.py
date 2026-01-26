import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- ADVANCED ENGINE CONFIG ---
st.set_page_config(page_title="Instamart Strategy v5.0", page_icon="🧡", layout="wide")

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
        box-shadow: 8px 8px 20px #040506;
        border: 1px solid rgba(255,255,255,0.05);
        transition: 0.3s ease;
    }
    .kpi-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.9; margin-bottom: 8px; font-weight: 600; color: white; }
    .kpi-value { font-size: 2.2rem; font-weight: 900; color: white; }
    .kpi-sub { font-size: 0.8rem; margin-top: 10px; background: rgba(0,0,0,0.25); border-radius: 20px; padding: 4px 12px; display: inline-block; color: white; }

    /* Terminal Command Center */
    .terminal-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 20px;
        border-radius: 12px;
        font-family: 'Consolas', monospace;
        margin-bottom: 25px;
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
        st.error("🚨 DATABASE_OFFLINE: swiggy_simulated_data.csv not found.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Schema Alignment
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 15.0
    if 'category' not in df.columns: df['category'] = 'fmcg'
    if 'freshness_hrs_left' not in df.columns: df['freshness_hrs_left'] = 24
    
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['base_comm'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    df['fixed_opex'] = 14.0
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGY CONTROL ---
with st.sidebar:
    st.image(LOGO_PATH if os.path.exists(LOGO_PATH) else SWIGGY_URL, width=150)
    st.title("Control Tower")
    
    st.subheader("🌦️ Environmental Overlays")
    weather = st.selectbox("Current Weather", ["Clear", "Cloudy", "Rainy", "Stormy"])
    
    st.subheader("🏹 Profitability Levers")
    aov_expansion = st.slider("AOV Boost (₹)", 0, 150, 45)
    fee_leverage = st.slider("Dynamic Surge (₹)", 0, 80, 20)
    disc_reduction = st.slider("Subsidy Reduction (%)", 0, 100, 25)

# --- SIMULATION LOGIC ---
f_df = df.copy()

# Weather & Risk Logic
weather_impact = {
    "Clear": {"cost": 1.0, "demand": 1.0},
    "Cloudy": {"cost": 1.1, "demand": 1.1},
    "Rainy": {"cost": 1.45, "demand": 1.7},
    "Stormy": {"cost": 2.0, "demand": 0.4}
}

# Apply Environmental Factors
f_df['delivery_cost'] *= weather_impact[weather]['cost']
f_df['order_value'] *= weather_impact[weather]['demand']

# Apply Strategic Levers
f_df['order_value'] += aov_expansion
f_df['delivery_fee'] += fee_leverage
f_df['discount'] *= (1 - disc_reduction/100)

# Final Financial Calculation
f_df['net_profit'] = (f_df['base_comm'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['fixed_opex'])

# --- HEADER ---
st.markdown("<h1 style='color: #FC8019; margin-bottom:0;'>Instamart Strategic War Room</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #666; margin-top:0;'>Location, Weather & Wastage Control v5.0</p>", unsafe_allow_html=True)

# --- 4 ORANGE KPI ROW ---
k1, k2, k3, k4 = st.columns(4)
gov = f_df['order_value'].sum() / 1e6
avg_p = f_df['net_profit'].mean()
cm_pct = (f_df['net_profit'].sum() / f_df['order_value'].sum()) * 100
alpha = (avg_p / 15.0) * 100

for col, l, v, s in zip([k1, k2, k3, k4], 
                        ["Projected GOV", "CM2 / Order", "CM % Margin", "System Alpha"],
                        [f"₹{gov:.2f}M", f"₹{avg_p:.2f}", f"{cm_pct:.1f}%", f"{alpha:.1f}pts"],
                        ["↑ 12% vs LW", f"Δ ₹{avg_p-12:.1f} vs Base", "Health: Optimal", "Target: 110"]):
    col.markdown(f'<div class="kpi-box"><div class="kpi-label">{l}</div><div class="kpi-value">{v}</div><div class="kpi-sub">{s}</div></div>', unsafe_allow_html=True)

# --- GREEN TERMINAL ---
st.markdown(f"""
<div class="terminal-box">
    <div class="terminal-line">
        <span class="status-pulse">●</span> WEATHER_STATUS: {weather.upper()} | LOGISTICS_FRICTION: {weather_impact[weather]['cost']}x<br>
        > STRATEGY_LOADED: AOV(+₹{aov_expansion}) | SURGE(+₹{fee_leverage}) | DISC_RED({disc_reduction}%)<br>
        > <span style="color:#FFF">FINANCIAL_OUTLOOK: CM2 Positivity estimated at ₹{avg_p:.2f} per vector.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- ANALYTICS SUITE ---
tabs = st.tabs(["💎 Financials", "📍 Zonal Risk", "🥬 Wastage Salvage", "📈 Risk Distribution"])

with tabs[0]:
    st.subheader("Contribution Margin 2 Waterfall")
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
    fig_water.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig_water, use_container_width=True)

with tabs[1]:
    st.subheader("Hourly Zonal Profitability Heatmap")
    z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
    fig_heat = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
    fig_heat.update_layout(template="plotly_dark")
    st.plotly_chart(fig_heat, use_container_width=True)

with tabs[2]:
    st.subheader("Automated Inventory Salvage Engine")
    df_risk = f_df[(f_df['category'].str.lower() == 'perishable') & (f_df['freshness_hrs_left'] < 12)].copy()
    
    c_w1, c_w2 = st.columns([1, 2])
    with c_w1:
        st.error(f"⚠️ {len(df_risk)} Units at Expiry Risk")
        st.metric("Potential EBITDA Loss", f"₹{df_risk['order_value'].sum():,.0f}")
        salvage_depth = st.select_slider("Flash Sale Intensity", options=["20%", "40%", "60%", "80%"])
        if st.button("🚀 TRIGGER PUSH NOTIFICATIONS"):
            st.success(f"Sent Flash Sale to {len(df_risk)*12} customers in affected zones!")
            st.balloons()
    with c_w2:
        fig_risk = px.scatter(df_risk, x="zone", y="freshness_hrs_left", size="order_value", 
                             color="delivery_cost", title="Location-Based Wastage Risk",
                             color_continuous_scale="Reds", template="plotly_dark")
        st.plotly_chart(fig_risk, use_container_width=True)

with tabs[3]:
    st.subheader("Monte Carlo Simulation: Outcome Distribution")
    fig_dist = px.histogram(f_df, x='net_profit', nbins=100, color_discrete_sequence=['#FC8019'], marginal="rug")
    fig_dist.update_layout(template="plotly_dark")
    st.plotly_chart(fig_dist, use_container_width=True)

st.markdown("---")
st.caption("Strategic Analyst Portfolio | Jagadeesh N | 2026")
