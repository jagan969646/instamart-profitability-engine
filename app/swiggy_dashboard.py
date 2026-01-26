import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime, timedelta

# --- EXECUTIVE SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Singularity v12.0", page_icon="🧡", layout="wide")

# --- ASSET & PATH RECOVERY ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_URL = "https://raw.githubusercontent.com/jagan969646/instamart-profitability-engine/main/app/Logo.png"

# --- PRO-LEVEL CSS CUSTOMIZATION ---
st.markdown("""
<style>
    .stApp { background-color: #020202; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    .executive-card {
        background: linear-gradient(145deg, #111, #050505);
        border: 1px solid rgba(252, 128, 25, 0.3);
        padding: 30px; border-radius: 12px;
        text-align: left; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .metric-value { font-size: 2.8rem; font-weight: 800; color: #FC8019; line-height: 1; }
    .metric-label { font-size: 0.85rem; color: #888; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px; }
    .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- ADVANCED DATA & FEATURE ENGINEERING ---
@st.cache_data
def load_and_enrich():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        # High-fidelity synthetic generator for demonstration
        np.random.seed(42)
        df = pd.DataFrame({
            'order_id': [f"ORD-{1000+i}" for i in range(2000)],
            'order_value': np.random.normal(550, 150, 2000).clip(200, 2500),
            'delivery_cost': np.random.normal(75, 15, 2000).clip(45, 120),
            'discount': np.random.exponential(40, 2000).clip(0, 150),
            'zone': np.random.choice(['Indiranagar', 'Koramangala', 'HSR', 'Whitefield', 'CBD'], 2000),
            'category': np.random.choice(['Fresh', 'FMCG', 'Munchies', 'Pharma'], 2000),
            'delivery_time': np.random.randint(12, 48, 2000),
            'rating': np.random.uniform(3.2, 5.0, 2000)
        })
    
    df.columns = df.columns.str.strip().str.lower()
    df['commission'] = df['order_value'] * 0.18 # Platform fee logic 
    df['ad_rev'] = df['order_value'] * 0.05
    df['delivery_fee'] = 35.0
    return df

df = load_and_enrich()

# --- SIDEBAR: SENIOR LEADERSHIP CONTROLS ---
with st.sidebar:
    st.image(LOGO_URL, width=160)
    st.markdown("## 🕹️ Strategy Simulation")
    scenario = st.select_slider("Select Market Dynamics", options=["Deep Off-Peak", "Standard", "Match Night", "Surge Extreme"])
    
    st.divider()
    st.subheader("💡 Portfolio Levers")
    # Derived from Strategy: AOV is the strongest lever [cite: 13]
    aov_expansion = st.slider("Target AOV Delta (Smart Bundling)", 0, 250, 80)
    # Strategy: Batching reduces last-mile cost [cite: 14]
    cost_efficiency = st.slider("Logistics Efficiency Alpha", 0, 40, 15)
    # Strategy: Margin-aware discounting [cite: 20]
    disc_reduction = st.slider("Subsidy Optimization (%)", 0, 100, 30)

# --- PRESCRIPTIVE SIMULATION MATH ---
f_df = df.copy()
sit_multipliers = {"Deep Off-Peak": 0.8, "Standard": 1.0, "Match Night": 1.7, "Surge Extreme": 2.1}
m = sit_multipliers[scenario]

f_df['order_value'] = (f_df['order_value'] * m) + aov_expansion
f_df['delivery_cost'] = (f_df['delivery_cost'] * m) - cost_efficiency
f_df['discount'] *= (1 - disc_reduction/100)
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + 18.0)

# Cleaning for high-end visualization
f_df['viz_size'] = f_df['order_value'].clip(lower=1)
f_df = f_df.dropna(subset=['net_profit', 'order_value'])

# --- MAIN EXECUTIVE DASHBOARD ---
st.markdown("<h1 style='color: #FC8019;'>INSTAMART <span style='color:#FFF; font-weight:100;'>SINGULARITY v12.0</span></h1>", unsafe_allow_html=True)
st.markdown("> **Strategic Mission:** Achieving CM2 Positivity through Volume-Margin Synthesis. ")

# High-Level Metric Row
m1, m2, m3, m4 = st.columns(4)
gov = f_df['order_value'].sum()
avg_profit = f_df['net_profit'].mean()
margin_pct = (f_df['net_profit'].sum() / gov) * 100

with m1:
    st.markdown(f'<div class="executive-card"><div class="metric-label">Projected GOV</div><div class="metric-value">₹{gov/1e6:.2f}M</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="executive-card"><div class="metric-label">Avg CM2 / Order</div><div class="metric-value">₹{avg_profit:.2f}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="executive-card"><div class="metric-label">Portfolio Margin</div><div class="metric-value">{margin_pct:.1f}%</div></div>', unsafe_allow_html=True)
with m4:
    status = "OPTIMIZED" if avg_profit > 45 else "RE-STRATEGIZE"
    st.markdown(f'<div class="executive-card"><div class="metric-label">Operation Health</div><div class="metric-value">{status}</div></div>', unsafe_allow_html=True)

# --- ANALYTICAL WORKSPACES ---
t1, t2, t3, t4 = st.tabs(["💎 Financial DNA", "🗺️ Market Density", "📝 Strategic Framework", "🛡️ Risk Matrix"])

with t1:
    st.subheader("Unit Economics Waterfall (Standardized per Order)")
    wf_metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount Burn', 'Dark Store OPEX']
    wf_vals = [f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -18.0]
    fig_wf = go.Figure(go.Waterfall(x=wf_metrics + ['Net Profit'], y=wf_vals + [0], totals={"marker":{"color":"#FC8019"}}))
    fig_wf.update_layout(template="plotly_dark", height=450, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_wf, use_container_width=True)
    

with t2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### Zonal CM2 Distribution")
        fig_box = px.box(f_df, x="zone", y="net_profit", color="zone", template="plotly_dark")
        st.plotly_chart(fig_box, use_container_width=True)
    with col_b:
        st.write("### Category Margin Heatmap")
        fig_sun = px.sunburst(f_df, path=['category', 'zone'], values='order_value', color='net_profit', template="plotly_dark")
        st.plotly_chart(fig_sun, use_container_width=True)

with t3:
    st.header("Executive Case Study: CM2 Optimization Framework")
    st.markdown(f"**Principal Analyst:** Jagadeesh N [cite: 2]")
    
    st.info("**Strategy 1: Incentivize High-AOV Baskets**\nImplementation of tiered delivery pricing for orders above ₹500 to dilute fixed costs. [cite: 18]")
    st.success("**Strategy 2: Batching & Density**\nPrioritizing multi-order batching during peak hours (e.g., IPL nights) to optimize last-mile economics. [cite: 19]")
    st.warning("**Strategy 3: The Scale Paradox**\nAvoid volume growth without margin health, as it accelerates 'burn' rather than profit. [cite: 15]")

with t4:
    st.subheader("Sensitivity Matrix: Profitability Thresholds")
    # Simulation of break-even points 
    costs = np.linspace(40, 100, 10)
    aovs = np.linspace(300, 1000, 10)
    z = [[(a*0.23 + 25) - (c + 15 + 10) for c in costs] for a in aovs]
    fig_heat = px.imshow(z, x=costs, y=aovs, labels=dict(x="Delivery Cost (₹)", y="AOV (₹)", color="Profit"), color_continuous_scale="RdYlGn", template="plotly_dark")
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
st.caption("SINGULARITY V12.0 | JAGADEESH N 2026 | CONFIDENTIAL")
