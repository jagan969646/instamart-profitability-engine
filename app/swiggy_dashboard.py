import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime, timedelta

# --- CORE SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Singularity v10.0", page_icon="🧡", layout="wide")

# --- PATH & ASSET RECOVERY ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
# Using official Logo from your GitHub to ensure stability
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
    .case-study-quote {
        background: #111; border-left: 5px solid #FC8019;
        padding: 15px; font-style: italic; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- NEURAL DATA ENGINE ---
@st.cache_data
def load_and_engineer():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        # Emergency Generator if CSV is missing or broken
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
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 29.0
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
    # Strategy 1: Tiered delivery pricing for orders above ₹500 [cite: 50]
    aov_expansion = st.slider("AOV Boost (Strategy 1)", 0, 150, 60)
    # Strategy 2: Multi-order batching efficiency [cite: 51]
    batch_savings = st.slider("Batching Efficiency (Strategy 2)", 0, 30, 10)
    # Strategy 3: Margin-aware discounting [cite: 52]
    disc_opt = st.slider("Discount Optimization (Strategy 3)", 0, 100, 25)

# --- PREDICTIVE PHYSICS ---
f_df = df.copy()
sit_map = {"Standard Day": 1.0, "IPL Match Night": 1.8, "Monsoon Surge": 1.5}
mult = sit_map[scenario]

f_df['order_value'] = (f_df['order_value'] * mult) + aov_expansion
f_df['delivery_cost'] = (f_df['delivery_cost'] * mult) - batch_savings
f_df['discount'] *= (1 - disc_opt/100)
f_df['commission'] = f_df['order_value'] * 0.18

# Contribution Margin (CM2) Calculation [cite: 38, 42]
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# --- VALUEERROR PROTECTION ---
# Size parameter MUST be > 0. We clip to 1 to ensure markers are always visible.
f_df['viz_size'] = f_df['order_value'].clip(lower=1)
f_df = f_df.dropna(subset=['customer_rating', 'delivery_time_mins', 'net_profit'])

# --- INTERFACE ---
st.markdown("<h1 style='color: #FC8019;'>INSTAMART <span style='color:#FFF; font-weight:100;'>SINGULARITY v10.0</span></h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
stats = [
    ("Total GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M"),
    ("Avg CM2/Order", f"₹{f_df['net_profit'].mean():.2f}"),
    ("Net Margin", f"{(f_df['net_profit'].sum()/f_df['order_value'].sum()*100):.1f}%"),
    ("Profit Status", "POSITIVE" if f_df['net_profit'].mean() > 0 else "BURN")
]

for col, (l, v) in zip([c1, c2, c3, c4], stats):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["💰 Financial Architecture", "🎯 Strategic Roadmap", "📖 Case Study Analysis"])

with t1:
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.write("### Unit Economics Waterfall (CM2)")
        wf_vals = [f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), 
                   -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0]
        fig_wf = go.Figure(go.Waterfall(
            x = ['Commission', 'Ads', 'Fees', 'Delivery Cost', 'Discounts', 'Fixed Store'],
            y = wf_vals, totals = {"marker":{"color":"#FC8019"}}
        ))
        fig_wf.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_wf, use_container_width=True)
    
    with col_right:
        st.write("### Satisfaction vs. Profitability")
        # Bubble size fixed to viz_size (>0) to prevent ValueError
        fig_scat = px.scatter(f_df, x="delivery_time_mins", y="customer_rating", 
                             color="net_profit", size="viz_size", 
                             color_continuous_scale="RdYlGn", template="plotly_dark")
        st.plotly_chart(fig_scat, use_container_width=True)

with t2:
    st.subheader("🚀 Strategic Recommendations for 2026")
    st.markdown(f"""
    1. **Incentivize High-AOV Baskets:** Implement tiered delivery pricing (lower fees for orders >₹500) and AI-driven "Smart Bundling"[cite: 50].
    2. **Optimize Delivery Densities:** Prioritize "Demand Clustering" and multi-order batching during peak hours like {scenario} to dilute last-mile costs[cite: 51].
    3. **Dynamic Discounting:** Move to "Margin-Aware" discounting that triggers for high-margin categories or high-LTV customers[cite: 52].
    """)

with t3:
    st.header("Improving Instamart Profitability: Case Study")
    st.caption("By Jagadeesh N | BBA, SRM IST (2026) | Aspiring Business Analyst")
    
    st.markdown("### 1. Problem Statement")
    st.write("Quick-commerce businesses operate on thin margins due to high last-mile costs and discount-heavy growth[cite: 37]. Achieving Contribution Margin (CM2) positivity is the primary challenge[cite: 38].")
    
    st.markdown("### 3. Key Strategic Insights")
    st.info("**AOV is the Strongest Lever:** A ₹50-₹70 increase in AOV (via cross-selling) has a significantly higher impact on profitability than a 20% increase in order volume.")
    st.success("**Cost Efficiency:** Reducing delivery costs by ₹10 through batching is 2x more sustainable than increasing fees by ₹10[cite: 46].")
    st.error("**Scale Paradox:** High volume without a healthy contribution margin actually accelerates 'burn'[cite: 47].")

st.markdown("---")
st.caption("Developed by Jagadeesh.N | Business Analytics Portfolio 2026")
