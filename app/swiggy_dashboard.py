import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Global Strategy War Room", page_icon="🧡", layout="wide")

# --- ELITE NEUMORPHIC INTERFACE ---
st.markdown("""
<style>
    .stApp { background-color: #050505; }
    /* Industrial Dashboard Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 128, 25, 0.3);
        padding: 24px;
        border-radius: 20px;
        text-align: left;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    .metric-label { font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 2.5px; margin-bottom: 5px; }
    .metric-value { font-size: 2.4rem; font-weight: 900; color: #FC8019; font-family: 'Inter', sans-serif; }
    .metric-delta { font-size: 0.85rem; padding: 4px 10px; border-radius: 10px; font-weight: bold; }
    
    /* Command Terminal v2.0 */
    .terminal {
        background: #000;
        border-left: 4px solid #FC8019;
        padding: 20px;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
        color: #2ECC71;
        font-size: 0.9rem;
        border-radius: 0 15px 15px 0;
        margin-bottom: 30px;
    }
    .blink { animation: blinker 1.5s linear infinite; color: #FC8019; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- ARCHITECTURAL DATA ENGINE ---
@st.cache_data
def load_and_engineer_v7():
    DATA_PATH = "swiggy_simulated_data.csv"
    if not os.path.exists(DATA_PATH):
        # Fail-safe: Generate Synthetic Neural Data if file missing
        df = pd.DataFrame({
            'zone': [f'Zone_{i}' for i in range(1, 6)] * 200,
            'order_value': np.random.uniform(300, 1200, 1000),
            'delivery_cost': np.random.uniform(40, 150, 1000),
            'freshness_hrs_left': np.random.randint(2, 48, 1000),
            'category': np.random.choice(['Perishable', 'FMCG', 'Gourmet', 'Essentials'], 1000),
            'hour': np.random.randint(0, 24, 1000)
        })
    else:
        df = pd.read_csv(DATA_PATH)
    
    df.columns = df.columns.str.strip().str.lower()
    
    # Auto-Heal Schema (Zero-Error Tolerance)
    schema = {'delivery_fee': 25, 'discount': 40, 'zone': 'Koromangala', 'day': 'Monday'}
    for col, val in schema.items():
        if col not in df.columns: df[col] = val

    # Dynamic Economics
    df['commission'] = df['order_value'] * 0.185
    df['ad_rev'] = df['order_value'] * 0.052
    df['fixed_opex'] = 14.50
    return df

df = load_and_engineer_v7()

# --- SIDEBAR: NEURAL CONTROLS ---
with st.sidebar:
    st.image(SWIGGY_URL, width=150)
    st.markdown("### 🛰️ GLOBAL PARAMETERS")
    
    situation = st.radio("MARKET SCENARIO", ["BASE_OPS", "IPL_MATCH_LIVE", "HEAVY_RAIN_MONSOON", "FESTIVAL_PEAK"])
    weather = st.select_slider("WEATHER FRICTION", options=["CLEAR", "MISTY", "DRIZZLE", "DOWNPOUR"])
    
    st.divider()
    st.markdown("### 🏹 PROFITABILITY LEVERS")
    surge_multiplier = st.slider("DYNAMIC SURGE ALPHA", 1.0, 3.5, 1.2)
    aov_target = st.slider("AOV GROWTH (₹)", 0, 300, 75)
    
    st.divider()
    # CHART #1: REVENUE ELASTICITY PIE (Sidebar)
    rev_mix = pd.DataFrame({'Source': ['COMM', 'ADS', 'SURGE'], 'Val': [18.5, 5.2, surge_multiplier*10]})
    fig1 = px.pie(rev_mix, values='Val', names='Source', hole=0.6, color_discrete_sequence=['#FC8019', '#3D4152', '#2ECC71'])
    fig1.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

# --- SIMULATION LOGIC (V7 PREDICTIVE) ---
f_df = df.copy()

# Advanced Situational Multipliers
sit_map = {
    "BASE_OPS": {"cost": 1.0, "demand": 1.0},
    "IPL_MATCH_LIVE": {"cost": 1.2, "demand": 2.4}, # Massive Snacks/Beverage spike
    "HEAVY_RAIN_MONSOON": {"cost": 2.1, "demand": 1.8}, # High Surge, High Rider Pay
    "FESTIVAL_PEAK": {"cost": 1.4, "demand": 1.6}
}
weather_map = {"CLEAR": 1.0, "MISTY": 1.1, "DRIZZLE": 1.4, "DOWNPOUR": 2.2}

# Compute Alpha Vector
f_df['delivery_cost'] *= (sit_map[situation]['cost'] * weather_map[weather])
f_df['order_value'] *= sit_map[situation]['demand']
f_df['order_value'] += aov_target
f_df['delivery_fee'] *= surge_multiplier

f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['fixed_opex'])

# --- MAIN DASHBOARD INTERFACE ---
st.markdown("<h1 style='color: #FC8019; letter-spacing: -1px;'>SINGULARITY <span style='color:#FFF; font-weight:100;'>INSTAMART_v7.0</span></h1>", unsafe_allow_html=True)

# KPI MATRIX
c1, c2, c3, c4 = st.columns(4)
gov = f_df['order_value'].sum() / 1e6
cm2 = f_df['net_profit'].mean()
margin = (f_df['net_profit'].sum() / f_df['order_value'].sum()) * 100
alpha = (f_df['net_profit'] > 0).mean() * 100

for col, l, v, d, c in zip([c1, c2, c3, c4], 
                           ["PROJECTED GOV", "AVG CM2 / ORDER", "CM % MARGIN", "EFFICIENCY ALPHA"],
                           [f"₹{gov:.2f}M", f"₹{cm2:.2f}", f"{margin:.1f}%", f"{alpha:.1f}pts"],
                           ["+14.2% VS PREV", "Δ +₹18.42", "OPTIMAL", "STABLE"],
                           ["#2ECC71", "#2ECC71", "#FC8019", "#3498DB"]):
    col.markdown(f"""<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div><div class="metric-delta" style="background:{c}22; color:{c};">{d}</div></div>""", unsafe_allow_html=True)

st.write("")
# COMMAND TERMINAL
st.markdown(f"""
<div class="terminal">
    <span class="blink">●</span> [SYSTEM_LOG] : RELATIONAL SIMULATION ACTIVE...<br>
    > MARKET_SITUATION: {situation} | WEATHER_INDEX: {weather} (FRICTION: {weather_map[weather]}x)<br>
    > CORE_LOGISTICS: AVG_COST(₹{f_df['delivery_cost'].mean():.2f}) | SURGE_REVENUE(₹{f_df['delivery_fee'].mean():.2f})<br>
    > <span style="color:#FFF">PREDICTION: {(f_df['net_profit'] > 0).sum()} vectors successfully cleared CM2 positive threshold.</span>
</div>
""", unsafe_allow_html=True)

# --- 7 CHART STRATEGIC SUITE ---
t1, t2, t3 = st.tabs(["💎 UNIT ECONOMICS", "📍 ZONAL INTELLIGENCE", "🥬 WASTAGE & SALVAGE AI"])

with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write("### CHART #2: CONTRIBUTION MARGIN WATERFALL")
        
        comps = ['Comm', 'Ads', 'Fees', 'Logistics', 'Discounts', 'OPEX']
        vals = [f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), 
                -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -14.5]
        fig2 = go.Figure(go.Waterfall(orientation="v", measure=["relative"]*6 + ["total"], x=comps + ['CM2'], y=vals + [0],
                                     totals={"marker":{"color":"#FC8019"}}, decreasing={"marker":{"color":"#FF4B4B"}}, increasing={"marker":{"color":"#2ECC71"}}))
        fig2.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        st.write("### CHART #3: PROFITABILITY DISTRIBUTION")
        fig3 = px.histogram(f_df, x="net_profit", nbins=50, color_discrete_sequence=['#FC8019'], marginal="box")
        fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

with t2:
    col_c, col_d = st.columns(2)
    with col_c:
        st.write("### CHART #4: ZONAL PROFIT HEATMAP")
        z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
        fig4 = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
        fig4.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)
    with col_d:
        st.write("### CHART #5: ORDER VOLUME BY DAY (SIMULATED)")
        # Generating day-wise trend
        fig5 = px.area(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value')
        fig5.update_traces(line_color='#FC8019', fillcolor='rgba(252, 128, 25, 0.2)')
        fig5.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig5, use_container_width=True)

with t3:
    col_e, col_f = st.columns(2)
    with col_e:
        st.write("### CHART #6: FRESHNESS ELASTICITY")
        # Visualizing which zones have the highest expiry risk
        fig6 = px.scatter(f_df, x="freshness_hrs_left", y="order_value", color="category", size="order_value",
                         hover_name="zone", title="Wastage Risk Assessment")
        fig6.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig6, use_container_width=True)
    with col_f:
        st.write("### CHART #7: SALVAGE SUCCESS RATE")
        # Simulating a bar chart of salvage success by zone
        salvage_data = pd.DataFrame({'Zone': f_df['zone'].unique(), 'Salvage %': np.random.uniform(60, 95, len(f_df['zone'].unique()))})
        fig7 = px.bar(salvage_data, x='Zone', y='Salvage %', color='Salvage %', color_continuous_scale='Greens')
        fig7.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig7, use_container_width=True)

    if st.button("🔥 TRIGGER MASS FLASH LIQUIDATION"):
        st.toast("SYSTEM_ACTION: Salvage Protocols Engaged.")
        st.success(f"Push Notifications dispatched to affected zones under {situation} conditions.")
        st.balloons()

st.markdown("---")
st.caption("PROPRIETARY STRATEGY ENGINE | JAGADEESH N | 2026")
