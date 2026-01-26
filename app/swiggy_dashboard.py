import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime, timedelta

# --- CORE SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Singularity v8.0", page_icon="🧡", layout="wide")

# --- PATH & ASSET RECOVERY ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- ELITE WAR-ROOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 128, 25, 0.4);
        padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .metric-value { font-size: 2.2rem; font-weight: 900; color: #FC8019; }
    .metric-label { font-size: 0.75rem; letter-spacing: 2px; color: #888; text-transform: uppercase; }
    .terminal {
        background: #000; border-left: 5px solid #2ECC71;
        padding: 15px; font-family: 'Courier New', monospace; color: #2ECC71;
        font-size: 0.85rem; margin-bottom: 20px; border-radius: 0 10px 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- NEURAL DATA ENGINE ---
@st.cache_data
def load_and_engineer():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        # Fallback Generator
        zones = ['Koramangala', 'Indiranagar', 'HSR Layout', 'Whitefield', 'Jayanagar']
        categories = ['Perishables', 'FMCG', 'Munchies', 'Beverages', 'Personal Care']
        data = {
            'order_time': [datetime.now() - timedelta(minutes=x*10) for x in range(1000)],
            'order_value': np.random.uniform(200, 1500, 1000),
            'delivery_cost': np.random.uniform(40, 110, 1000),
            'discount': np.random.uniform(0, 120, 1000),
            'zone': np.random.choice(zones, 1000),
            'category': np.random.choice(categories, 1000),
            'freshness_hrs_left': np.random.randint(1, 48, 1000),
            'delivery_time_mins': np.random.randint(12, 45, 1000),
            'customer_rating': np.random.uniform(3.5, 5.0, 1000)
        }
        df = pd.DataFrame(data)

    # Hardening Column Names
    df.columns = df.columns.str.strip().str.lower()
    
    # Critical Fix: Ensure 'delivery_fee' exists to prevent KeyError
    if 'delivery_fee' not in df.columns:
        df['delivery_fee'] = 25.0
    
    # Ensure numeric types for calculation columns
    numeric_cols = ['order_value', 'delivery_cost', 'discount', 'delivery_fee']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    
    # Baseline Unit Economics
    df['commission'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGIC CONTROL TOWER ---
with st.sidebar:
    st.image(SWIGGY_URL, width=120)
    st.header("🛰️ Operations")
    situation = st.selectbox("Market Situation", ["Standard Ops", "IPL Final Night", "Heavy Rain Surge", "Weekend Peak"])
    weather = st.select_slider("Weather Friction", options=["Clear", "Cloudy", "Heavy Rain", "Extreme Storm"])
    st.divider()
    aov_adj = st.slider("AOV Expansion (₹)", 0, 200, 30)
    surge_adj = st.slider("Dynamic Surge Alpha (₹)", 0, 100, 20)
    disc_cut = st.slider("Subsidy Optimization (%)", 0, 100, 15)

# --- PREDICTIVE PHYSICS ---
# --- PREDICTIVE PHYSICS ---
f_df = df.copy()
sit_map = {"Standard Ops": 1.0, "IPL Final Night": 2.2, "Heavy Rain Surge": 1.7, "Weekend Peak": 1.4}
weather_map = {"Clear": 1.0, "Cloudy": 1.2, "Heavy Rain": 1.8, "Extreme Storm": 2.5}
cost_mult = sit_map[situation] * weather_map[weather]

# Simulation Math
f_df['delivery_cost'] *= cost_mult
f_df['order_value'] *= sit_map[situation]
f_df['order_value'] += aov_adj
f_df['delivery_fee'] += surge_adj
f_df['discount'] *= (1 - disc_cut/100)

# Net Profit calculation
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# --- CRITICAL FIX FOR VALUEERROR ---
# 1. Ensure order_value is never 0 or negative for the 'size' parameter
f_df['viz_size'] = f_df['order_value'].apply(lambda x: x if x > 0 else 1)

# 2. Drop any remaining NaNs in visualization columns to prevent Plotly errors
f_df = f_df.dropna(subset=['delivery_time_mins', 'customer_rating', 'net_profit', 'viz_size'])

# Simulation Math
f_df['delivery_cost'] *= cost_mult
f_df['order_value'] *= sit_map[situation]
f_df['order_value'] += aov_adj
f_df['delivery_fee'] += surge_adj
f_df['discount'] *= (1 - disc_cut/100)

# Net Profit calculation (including fixed store OPEX of 15.0)
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# Cleaning for Viz
f_df['viz_size'] = f_df['order_value'].clip(lower=1)

# --- MAIN INTERFACE ---
st.markdown("<h1 style='color: #FC8019;'>INSTAMART <span style='color:#FFF; font-weight:100;'>SINGULARITY v8.0</span></h1>", unsafe_allow_html=True)

# KPI Row
c1, c2, c3, c4 = st.columns(4)
gov = f_df['order_value'].sum()
cm2 = f_df['net_profit'].mean()
margin = (f_df['net_profit'].sum() / gov * 100) if gov != 0 else 0
success_rate = (f_df['net_profit'] > 0).mean() * 100

metrics = [
    ("Projected GOV", f"₹{gov/1e6:.2f}M"),
    ("CM2 / Order", f"₹{cm2:.2f}"),
    ("Net Margin", f"{margin:.1f}%"),
    ("Profitable Orders", f"{success_rate:.1f}%")
]

for col, (l, v) in zip([c1, c2, c3, c4], metrics):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)

st.write("")
st.markdown(f"""<div class="terminal">> [LOG]: {situation.upper()} ACTIVE | WEATHER: {weather.upper()} ({weather_map[weather]}x Friction)<br>> [STATUS]: Engine online. Parameters synced.</div>""", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["💰 Financials", "📍 Zonal Analytics", "🥬 Inventory", "👥 Customer Experience"])

with t1:
    st.subheader("Unit Economics (Waterfall)")
    # Averaging metrics for the Waterfall
    wf_metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    wf_values = [
        f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(),
        -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0
    ]
    fig_wf = go.Figure(go.Waterfall(
        orientation = "v", x = wf_metrics + ['Net Profit'], y = wf_values + [0],
        totals = {"marker":{"color":"#FC8019"}},
        decreasing = {"marker":{"color":"#EF4444"}},
        increasing = {"marker":{"color":"#60B246"}}
    ))
    fig_wf.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig_wf, use_container_width=True)

with t4:
    col10, col11, col12 = st.columns(3)
    with col10:
        st.write("### Delivery Efficiency")
        fig10 = px.violin(f_df, y="delivery_time_mins", x="zone", box=True, color="zone", template="plotly_dark")
        st.plotly_chart(fig10, use_container_width=True)
    with col11:
        st.write("### Satisfaction vs. Profit")
        fig11 = px.scatter(f_df, x="delivery_time_mins", y="customer_rating", 
                          color="net_profit", size="viz_size", 
                          color_continuous_scale="RdYlGn", template="plotly_dark")
        st.plotly_chart(fig11, use_container_width=True)
    with col12:
        st.write("### Rating Distribution")
        fig12 = px.histogram(f_df[f_df['customer_rating'] > 0], x="customer_rating", 
                            nbins=10, color_discrete_sequence=['#FC8019'], template="plotly_dark")
    st.plotly_chart(fig12, use_container_width=True)

st.markdown("---")
st.caption(f"PROPRIETARY STRATEGY ENGINE | JAGADEESH N | 2026")

