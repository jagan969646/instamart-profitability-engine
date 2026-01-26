import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- ADVANCED ENGINE CONFIG ---
st.set_page_config(page_title="Instamart Strategy v6.5", page_icon="🧡", layout="wide")

# --- ELITE EXECUTIVE CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0A0C10; }
    .kpi-box {
        background: linear-gradient(135deg, #FC8019 0%, #D86910 100%);
        color: white !important;
        padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 5px 5px 15px #000; border: 1px solid rgba(255,255,255,0.1);
    }
    .kpi-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; color: white; }
    .kpi-value { font-size: 1.8rem; font-weight: 800; color: white; }
    .terminal-box {
        background-color: #000; border: 1px solid #2ECC71;
        padding: 15px; border-radius: 10px; font-family: 'Consolas', monospace;
        margin-bottom: 20px;
    }
    .terminal-line { color: #2ECC71; font-size: 0.85rem; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# --- ROBUST DATA ENGINE ---
@st.cache_data
def load_and_engineer():
    # Use your specific path or a fallback
    DATA_PATH = "swiggy_simulated_data.csv" 
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 File not found: {DATA_PATH}. Please upload it to the repository.")
        st.stop()
        
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # --- SCHEMA PROTECTOR (Fixes the KeyError) ---
    required_cols = {
        'delivery_fee': 20.0,
        'delivery_cost': 45.0,
        'order_value': 400.0,
        'discount': 30.0,
        'category': 'FMCG',
        'freshness_hrs_left': 24,
        'zone': 'Default Zone'
    }
    for col, default in required_cols.items():
        if col not in df.columns:
            df[col] = default # Create column if missing
    
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['base_comm'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGIC CONTROLS ---
with st.sidebar:
    st.markdown("### 🕹️ War Room Controls")
    
    # 1. Situation & Weather
    situation = st.selectbox("Market Situation", ["Standard", "IPL Match Night", "Heavy Rain Surge", "Weekend Peak"])
    weather = st.selectbox("Location Weather", ["Clear", "Cloudy", "Heavy Rain", "Stormy"])
    
    st.divider()
    
    # 2. Financial Levers
    aov_adj = st.slider("AOV Expansion (₹)", 0, 200, 50)
    surge_adj = st.slider("Dynamic Surge Fee (₹)", 0, 100, 25)
    disc_opt = st.slider("Discount Reduction (%)", 0, 100, 30)

    st.divider()
    
    # CHART #1: Sidebar Revenue Mix (Pie Chart)
    st.write("### Projected Revenue Mix")
    pie_data = pd.DataFrame({
        'Source': ['Commissions', 'Ad Revenue', 'Delivery Fees'],
        'Value': [18, 5, 12] # Estimated ratios
    })
    fig1 = px.pie(pie_data, values='Value', names='Source', hole=0.5, 
                 color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
    fig1.update_layout(showlegend=False, height=220, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

# --- SIMULATION ENGINE ---
f_df = df.copy()

# Advanced Situational Multipliers
sit_logic = {
    "Standard": {"c": 1.0, "d": 1.0},
    "IPL Match Night": {"c": 1.1, "d": 2.2},
    "Heavy Rain Surge": {"c": 1.8, "d": 1.7},
    "Weekend Peak": {"c": 1.2, "d": 1.4}
}
weather_logic = {"Clear": 1.0, "Cloudy": 1.1, "Heavy Rain": 1.5, "Stormy": 2.1}

# Apply Logic
m = sit_logic[situation]
w = weather_logic[weather]

f_df['delivery_cost'] *= (m['c'] * w)
f_df['order_value'] *= m['d']
f_df['order_value'] += aov_adj
f_df['delivery_fee'] += surge_adj
f_df['discount'] *= (1 - disc_opt/100)

f_df['net_profit'] = (f_df['base_comm'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# --- MAIN UI ---
st.markdown("<h1 style='color: #FC8019;'>Instamart Strategy war Room v6.5</h1>", unsafe_allow_html=True)

# 4 KPI ROW
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi-box"><div class="kpi-label">Projected GOV</div><div class="kpi-value">₹{f_df["order_value"].sum()/1e6:.2f}M</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi-box"><div class="kpi-label">CM2 / Order</div><div class="kpi-value">₹{f_df["net_profit"].mean():.2f}</div></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi-box"><div class="kpi-label">Net Margin</div><div class="kpi-value">{(f_df["net_profit"].sum()/f_df["order_value"].sum())*100:.1f}%</div></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="kpi-box"><div class="kpi-label">Efficiency</div><div class="kpi-value">{(f_df["net_profit"]>0).mean()*100:.0f}%</div></div>', unsafe_allow_html=True)

# COMMAND TERMINAL
st.markdown(f"""
<div class="terminal-box">
    <div class="terminal-line">
        [STATUS] SIMULATING: {situation.upper()} | WEATHER: {weather.upper()}<br>
        [LOGS] Cost Multiplier: {m['c']*w:.2f}x | Demand Spike: {m['d']:.2f}x<br>
        [ACTION] Surge Pricing Applied: ₹{surge_adj} | AOV Target: +₹{aov_adj}
    </div>
</div>
""", unsafe_allow_html=True)

# --- THE 7 REMAINING CHARTS ---
t1, t2, t3 = st.tabs(["📊 Financial Deep-Dive", "📍 Operational Risk", "🥬 Wastage & Salvage"])

with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write("### Chart #2: Unit Economics Waterfall")
        
        c_list = ['Comm', 'Ads', 'Fees', 'Logistics', 'Discounts', 'OPEX']
        v_list = [f_df['base_comm'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), 
                  -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0]
        fig2 = go.Figure(go.Waterfall(orientation="v", measure=["relative"]*6 + ["total"], x=c_list + ['Final CM2'], y=v_list + [0],
                                     totals={"marker":{"color":"#FC8019"}}, decreasing={"marker":{"color":"#FF4B4B"}}, increasing={"marker":{"color":"#2ECC71"}}))
        fig2.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        st.write("### Chart #3: Daily GOV Trend")
        fig3 = px.line(f_df.groupby('day')['order_value'].sum().reset_index(), x='day', y='order_value', markers=True)
        fig3.update_traces(line_color='#FC8019')
        fig3.update_layout(template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

with t2:
    col_c, col_d = st.columns(2)
    with col_c:
        st.write("### Chart #4: Zonal Profitability Heatmap")
        z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
        fig4 = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
        fig4.update_layout(template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)
    with col_d:
        st.write("### Chart #5: Profit Distribution")
        fig5 = px.histogram(f_df, x='net_profit', nbins=50, color_discrete_sequence=['#60B246'])
        fig5.update_layout(template="plotly_dark")
        st.plotly_chart(fig5, use_container_width=True)

with t3:
    col_e, col_f = st.columns(2)
    with col_e:
        st.write("### Chart #6: Freshness Risk by Category")
        fig6 = px.box(f_df, x='category', y='freshness_hrs_left', color='category')
        fig6.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)
    with col_f:
        st.write("### Chart #7: Inventory Value at Risk")
        
        fig7 = px.scatter(f_df[f_df['freshness_hrs_left']<10], x='order_value', y='delivery_cost', color='zone', size='order_value')
        fig7.update_layout(template="plotly_dark")
        st.plotly_chart(fig7, use_container_width=True)
        
    # Chart #8: Push Notification Reach
    st.write("### Chart #8: Push Notification Impact")
    reach = pd.DataFrame({'Target': ['Active Users', 'Potential Buyers', 'Salvage Reach'], 'Count': [1000, 450, 890]})
    fig8 = px.bar(reach, x='Target', y='Count', color='Target', color_discrete_sequence=['#3D4152', '#FC8019', '#60B246'])
    fig8.update_layout(template="plotly_dark", showlegend=False, height=300)
    st.plotly_chart(fig8, use_container_width=True)
    
    if st.button("🚀 TRIGGER FLASH SALVAGE PUSH"):
        st.success("Notifications Sent! Predicted Wastage Reduction: 22%")
        st.balloons()

st.markdown("---")
st.caption("Strategic Portfolio | Jagadeesh N | Built for Swiggy Case Study 2026")
