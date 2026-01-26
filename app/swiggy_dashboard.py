import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime, timedelta

# --- CORE SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Singularity v11.0", page_icon="🧡", layout="wide")

# --- ASSET RECOVERY ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_URL = "https://raw.githubusercontent.com/jagan969646/instamart-profitability-engine/main/app/Logo.png"

# --- ELITE WAR-ROOM UI ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 128, 25, 0.4);
        padding: 25px; border-radius: 15px; text-align: center;
    }
    .metric-value { font-size: 2.3rem; font-weight: 900; color: #FC8019; }
    .metric-label { font-size: 0.8rem; letter-spacing: 2px; color: #888; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# --- NEURAL DATA ENGINE ---
@st.cache_data
def load_and_engineer():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        zones = ['Koramangala', 'Indiranagar', 'HSR Layout', 'Whitefield', 'Jayanagar']
        df = pd.DataFrame({
            'order_time': [datetime.now() - timedelta(minutes=x*10) for x in range(1000)],
            'order_value': np.random.uniform(300, 1200, 1000),
            'delivery_cost': np.random.uniform(50, 95, 1000),
            'discount': np.random.uniform(0, 80, 1000),
            'zone': np.random.choice(zones, 1000),
            'delivery_time_mins': np.random.randint(15, 45, 1000),
            'customer_rating': np.random.uniform(3.5, 5.0, 1000)
        })
    
    df.columns = df.columns.str.strip().str.lower()
    # Ensure mandatory columns exist for the simulation
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 29.0
    if 'delivery_time_mins' not in df.columns: df['delivery_time_mins'] = 25
    if 'customer_rating' not in df.columns: df['customer_rating'] = 4.0
    
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['commission'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGIC CONTROL ---
with st.sidebar:
    st.image(LOGO_URL, width=150)
    st.header("🛰️ Operations Control")
    scenario = st.selectbox("Market Scenario", ["Standard Day", "IPL Match Night", "Monsoon Surge"])
    st.divider()
    st.subheader("🛠️ Strategic Levers")
    aov_boost = st.slider("AOV Expansion (Strategy 1)", 0, 150, 65)
    batch_savings = st.slider("Batching Efficiency (Strategy 2)", 0, 30, 12)
    disc_opt = st.slider("Discount Optimization (Strategy 3)", 0, 100, 25)

# --- PREDICTIVE PHYSICS ---
f_df = df.copy()
sit_map = {"Standard Day": 1.0, "IPL Match Night": 1.8, "Monsoon Surge": 1.5}
mult = sit_map[scenario]

# Simulation Math
f_df['order_value'] = (f_df['order_value'] * mult) + aov_boost
f_df['delivery_cost'] = (f_df['delivery_cost'] * mult) - batch_savings
f_df['discount'] *= (1 - disc_opt/100)
f_df['commission'] = f_df['order_value'] * 0.18
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# --- KEYERROR & VALUEERROR PROTECTION ---
f_df['viz_size'] = f_df['order_value'].clip(lower=1)
# Safe drop: only drop columns that actually exist
existing_subset = [c for c in ['customer_rating', 'delivery_time_mins', 'net_profit'] if c in f_df.columns]
f_df = f_df.dropna(subset=existing_subset)

# --- INTERFACE ---
st.markdown("<h1 style='color: #FC8019;'>INSTAMART <span style='color:#FFF; font-weight:100;'>SINGULARITY v11.0</span></h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
stats = [
    ("Total GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M"),
    ("Avg CM2/Order", f"₹{f_df['net_profit'].mean():.2f}"),
    ("Net Margin", f"{(f_df['net_profit'].sum()/f_df['order_value'].sum()*100):.1f}%"),
    ("Profit Status", "POSITIVE" if f_df['net_profit'].mean() > 0 else "BURN")
]
for col, (l, v) in zip([c1, c2, c3, c4], stats):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["💰 Economics", "🎯 Roadmap", "📖 Case Study", "🔬 Break-even Matrix"])

with t1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.write("### Unit Economics Waterfall (CM2)")
        wf_vals = [f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0]
        fig_wf = go.Figure(go.Waterfall(x=['Comm.', 'Ads', 'Fees', 'Deliv.', 'Disc.', 'Fixed'], y=wf_vals, totals={"marker":{"color":"#FC8019"}}))
        fig_wf.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_wf, use_container_width=True)
    with col_r:
        st.write("### Satisfaction vs. Profit")
        fig_scat = px.scatter(f_df, x="delivery_time_mins", y="customer_rating", color="net_profit", size="viz_size", color_continuous_scale="RdYlGn", template="plotly_dark")
        st.plotly_chart(fig_scat, use_container_width=True)

with t3:
    st.header("Executive Analysis: Improving Instamart Profitability")
    st.caption("By Jagadeesh N | BBA, SRM IST (2026)")
    st.info("**AOV is the Strongest Lever:** A ₹50-₹70 increase in AOV has a higher impact than 20% volume growth[cite: 13, 45].")
    st.success("**Batching Efficiency:** Reducing delivery costs by ₹10 via batching is 2x more sustainable for retention than increasing fees[cite: 14, 46].")
    st.error("**Scale Paradox:** High volume without a healthy contribution margin accelerates 'burn'[cite: 15, 47].")

with t4:
    st.subheader("Sensitivity Matrix: Dark Store Break-even Analysis")
    # Generating a sensitivity matrix as mentioned in Technical Execution
    aov_range = np.linspace(400, 800, 5)
    cost_range = np.linspace(40, 90, 5)
    matrix = []
    for a in aov_range:
        row = []
        for c in cost_range:
            profit = (a * 0.23 + 25) - (c + 15 + 10) # Simplified formula
            row.append(profit)
        matrix.append(row)
    
    fig_heat = px.imshow(matrix, x=cost_range, y=aov_range, labels=dict(x="Delivery Cost (₹)", y="AOV (₹)", color="Profit/Order"), color_continuous_scale="RdYlGn", template="plotly_dark")
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
st.caption("Developed by Jagadeesh.N | Business Analytics Portfolio 2026")
