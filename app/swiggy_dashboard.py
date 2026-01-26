import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime, timedelta

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Singularity v9.0", page_icon="🧡", layout="wide")

# --- ASSET PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_URL = "https://raw.githubusercontent.com/jagan969646/instamart-profitability-engine/main/app/Logo.png"

# --- ELITE UI STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 128, 25, 0.5);
        padding: 25px; border-radius: 20px;
        text-align: center; transition: 0.3s;
    }
    .metric-card:hover { border-color: #FC8019; background: rgba(252, 128, 25, 0.05); }
    .metric-value { font-size: 2.5rem; font-weight: 900; color: #FC8019; }
    .metric-label { font-size: 0.8rem; letter-spacing: 2px; color: #888; text-transform: uppercase; margin-bottom: 10px; }
    .case-study-box {
        background: #111; border-left: 5px solid #FC8019;
        padding: 20px; border-radius: 0 15px 15px 0; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- NEURAL DATA ENGINE ---
@st.cache_data
def load_and_engineer():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        # Emergency Simulation if CSV fails
        df = pd.DataFrame({
            'order_time': [datetime.now() - timedelta(minutes=x*5) for x in range(1000)],
            'order_value': np.random.uniform(300, 1200, 1000),
            'delivery_cost': np.random.uniform(50, 90, 1000),
            'discount': np.random.uniform(0, 50, 1000),
            'zone': np.random.choice(['Indiranagar', 'Koramangala', 'HSR', 'Whitefield'], 1000),
            'delivery_time_mins': np.random.randint(15, 40, 1000),
            'customer_rating': np.random.uniform(3.5, 5.0, 1000)
        })

    df.columns = df.columns.str.strip().str.lower()
    df['order_time'] = pd.to_datetime(df['order_time'])
    
    # Unit Economics Logic [cite: 10, 42]
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 29.0
    df['commission'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    return df

df = load_and_engineer()

# --- SIDEBAR: OPERATIONS CONTROL ---
with st.sidebar:
    st.image(LOGO_URL, width=150)
    st.markdown("### 🛰️ LIVE SIMULATOR")
    situation = st.selectbox("Market Scenario", ["Standard Day", "IPL Match Night", "Monsoon Surge"])
    
    st.divider()
    st.markdown("### 🛠️ STRATEGIC LEVERS")
    # AOV is the strongest lever 
    aov_expansion = st.slider("AOV Expansion (Strategy 1)", 0, 150, 50)
    # Reducing cost via batching is 2x more sustainable [cite: 14, 46]
    batching_eff = st.slider("Batching Efficiency (Strategy 2)", 0, 30, 10)
    # Dynamic discounting [cite: 20, 52]
    disc_reduction = st.slider("Discount Optimization (Strategy 3)", 0, 100, 20)

# --- PREDICTIVE MATH ---
f_df = df.copy()
sit_mult = {"Standard Day": 1.0, "IPL Match Night": 1.8, "Monsoon Surge": 1.5}

f_df['order_value'] = (f_df['order_value'] * sit_mult[situation]) + aov_expansion
f_df['delivery_cost'] = (f_df['delivery_cost'] * sit_mult[situation]) - batching_eff
f_df['discount'] *= (1 - disc_reduction/100)
f_df['commission'] = f_df['order_value'] * 0.18

# CM2 calculation [cite: 6, 38]
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# Sanitize for viz
f_df['viz_size'] = f_df['order_value'].clip(lower=1)

# --- INTERFACE ---
st.markdown("<h1 style='color: #FC8019;'>INSTAMART <span style='color:#FFF; font-weight:100;'>SINGULARITY v9.0</span></h1>", unsafe_allow_html=True)
st.caption("Advanced Profitability Engine | CM2 Strategy Framework 2026")

c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("Projected GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M"),
    ("CM2 per Order", f"₹{f_df['net_profit'].mean():.2f}"),
    ("Margin %", f"{(f_df['net_profit'].sum()/f_df['order_value'].sum()*100):.1f}%"),
    ("Health Score", "ELITE" if f_df['net_profit'].mean() > 40 else "CRITICAL")
]

for col, (l, v) in zip([c1, c2, c3, c4], metrics):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)

# --- TABBED INTELLIGENCE ---
t1, t2, t3 = st.tabs(["📊 Financial DNA", "🎯 Strategic Recommendations", "📖 Full Case Study"])

with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write("### Unit Economics Waterfall")
        wf_vals = [f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0]
        fig_wf = go.Figure(go.Waterfall(
            x = ['Commission', 'Ads', 'Fees', 'Delivery', 'Discounts', 'Fixed Store'],
            y = wf_vals, totals = {"marker":{"color":"#FC8019"}}
        ))
        fig_wf.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_wf, use_container_width=True)
    with col_b:
        st.write("### Satisfaction vs. Margin")
        fig_scat = px.scatter(f_df, x="delivery_time_mins", y="customer_rating", color="net_profit", size="viz_size", color_continuous_scale="RdYlGn", template="plotly_dark")
        st.plotly_chart(fig_scat, use_container_width=True)

with t2:
    st.markdown("### 🚀 Execution Roadmap based on Analysis")
    st.info("**Strategy 1: Incentivize High-AOV Baskets**\nUsing tiered delivery for orders >₹500 and AI-driven bundling[cite: 18, 50].")
    st.success("**Strategy 2: Optimize Delivery Densities**\nPrioritizing demand clustering and batching during peaks like IPL nights to dilute costs[cite: 19, 51].")
    st.warning("**Strategy 3: Dynamic Discounting**\nShifting to margin-aware discounting for high-margin categories[cite: 20, 52].")

with t3:
    st.markdown(f"## {df.columns.str.title()[0]} Profitability Analysis [cite: 1, 33]")
    st.markdown(f"**Author:** Jagadeesh N | BBA, SRM IST (2026) [cite: 2, 34]")
    
    st.markdown("### 1. Problem Statement")
    st.write("Q-commerce operates on thin margins due to last-mile costs and discount-heavy growth[cite: 5, 37]. Achieving CM2 positivity is the primary challenge[cite: 6, 38].")
    
    st.markdown("### 3. Key Strategic Insights")
    st.markdown(f"""
    <div class="case-study-box">
    <b>AOV is the Strongest Lever:</b> A ₹50-₹70 increase in AOV has a higher impact than 20% volume growth.<br><br>
    <b>The Scale Paradox:</b> High volume without a healthy contribution margin accelerates "burn"[cite: 15, 47].
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("CONFIDENTIAL | STRATEGY ENGINE | JAGADEESH N 2026")
