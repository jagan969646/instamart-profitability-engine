import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="SWIGGY NEURAL OPS", layout="wide", initial_sidebar_state="expanded")

# --- 2. ELITE CSS FOR CHART VISIBILITY ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
    
    /* Force Background and Text Colors */
    .stApp { background-color: #050505; color: #8F9BB3; font-family: 'JetBrains Mono', monospace; }
    
    /* Center Logo & Layout */
    .header-box { text-align: center; padding: 10px 0; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #0A0A0C !important; border-right: 1px solid #1A1C23; }
    
    /* Metric & Console Boxes */
    .stMetric { background: #0F0F12 !important; border: 1px solid #1A1C23 !important; border-radius: 8px; padding: 15px !important; }
    [data-testid="stMetricValue"] { color: #FC8019 !important; font-size: 1.8rem !important; }
    .console-box { 
        background: #000; color: #00FF41; padding: 12px; border-radius: 4px; 
        font-size: 0.75rem; border: 1px solid #00FF4133; margin-bottom: 25px; 
        font-family: 'JetBrains Mono'; line-height: 1.4;
    }
    
    /* Ensure Chart Containers have height */
    .js-plotly-plot { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA RESOLVER ---
def resolve_path(filename):
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files: return os.path.join(root, filename)
    return filename

@st.cache_data
def load_quantum_engine():
    # Direct access for speed, resolver for safety
    path = resolve_path('swiggy_simulated_data.csv')
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

try:
    df = load_quantum_engine()
except Exception as e:
    st.error(f"DATA_LINK_FAILURE: {e}")
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color: #FC8019; font-size: 1.2rem;'>COMMAND_NAV</h2>", unsafe_allow_html=True)
    page = st.radio("SELECT_MODULE", 
                    ["GROWTH_VECTORS", "LOGISTICS_NEURAL", "FINANCIAL_QUANT", "RISK_ANALYSIS"],
                    index=0)
    st.markdown("---")
    st.caption("SYSTEM_STATUS: PRO_ACTIVE")
    st.caption(f"KERNEL_REF: {hex(id(df))}")

# --- 5. MAIN STAGE: LOGO & COCOLE ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
logo = resolve_path('image_d988b9.png')
if os.path.exists(logo): 
    st.image(logo, width=150)
else:
    st.title("SWIGGY NEURAL")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] MODULE_LOADED: {page}<br>
    [{datetime.now().strftime('%H:%M:%S')}] PACKETS_RESOLVED: {len(df)} | RENDER_ENGINE: PLOTLY_DARK
</div>
""", unsafe_allow_html=True)

# Risk Alert Push
if df['freshness_hrs_left'].min() < 5:
    st.toast("🚨 ALERT: CRITICAL PERISHABLE RISK DETECTED", icon="⚠️")

# --- 6. CHART UTILITY (Forces Visibility) ---
def render_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=350  # Fixed height ensures they are visible
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 7. MODULAR PAGES ---

if page == 'GROWTH_VECTORS':
    st.markdown("#### 🛰️ GROWTH_MATRICES")
    c1, c2, c3 = st.columns(3)
    with c1: render_chart(px.area(df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', title="Temporal Volume Flow"))
    with c2: render_chart(px.pie(df, names='zone', values='order_value', hole=0.5, title="Zonal Distribution"))
    with c3: render_chart(px.bar(df.groupby('category')['order_value'].sum().reset_index(), x='category', y='order_value', title="Categorical GMV"))

elif page == 'LOGISTICS_NEURAL':
    st.markdown("#### 🧠 LOGISTICS_NEURAL")
    c1, c2, c3 = st.columns(3)
    with c1: render_chart(px.box(df, x="weather", y="delivery_time_mins", color="weather", title="SLA Weather Variance"))
    with c2: render_chart(px.line(df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins', title="Hourly Velocity Delta"))
    with c3: render_chart(px.density_heatmap(df, x="delivery_time_mins", y="order_value", title="Logistics Density"))

elif page == 'FINANCIAL_QUANT':
    st.markdown("#### 💎 FINANCIAL_QUANT")
    c1, c2, c3 = st.columns(3)
    with c1: render_chart(px.scatter(df, x="discount", y="contribution_margin", trendline="ols", title="Discount Elasticity"))
    with c2: render_chart(px.violin(df, y="margin_rate", x="zone", box=True, title="Margin Stability"))
    with c3: render_chart(px.scatter(df, x="delivery_cost", y="contribution_margin", color="category", title="Cost-Profit Correlation"))

elif page == 'RISK_ANALYSIS':
    st.markdown("#### 🚨 RISK_ANALYSIS")
    c1, c2, c3 = st.columns(3)
    with c1: render_chart(px.histogram(df, x="delivery_cost", nbins=30, title="Logistics Overhead Risk"))
    with c2: render_chart(px.scatter(df, x="freshness_hrs_left", y="order_value", color="category", title="Inventory Decay Vector"))
    with c3: render_chart(px.scatter_3d(df.sample(400), x='order_value', y='delivery_time_mins', z='margin_rate', color='zone', title="3D Operational Space"))

# --- 8. FOOTER METRICS ---
st.markdown("---")
f1, f2, f3, f4 = st.columns(4)
f1.metric("GLOBAL_GMV", f"₹{df['order_value'].sum()/1e5:.2f}L")
f2.metric("MEAN_MARGIN", f"{df['margin_rate'].mean():.1f}%")
f3.metric("SYSTEM_SLA", f"{df['delivery_time_mins'].mean():.1f}m")
f4.metric("STATUS", "ALPHA_ACTIVE")
