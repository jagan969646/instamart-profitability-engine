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

# Elite Dark UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; background-color: #030305; color: #8F9BB3; }
    
    /* Center Logo & Layout */
    .header-box { text-align: center; padding: 20px 0; }
    .stSidebar { background-color: #05070A !important; border-right: 1px solid #1A1C23; }
    
    /* Console & Metrics */
    .console-box { background: #000; color: #00FF41; padding: 12px; border-radius: 4px; font-size: 0.75rem; border: 1px solid #00FF4133; margin: 0 auto 25px auto; width: 100%; }
    .stMetric { background: #0A0B10; border: 1px solid #1A1C23; border-radius: 4px; padding: 15px !important; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.6rem !important; }
    
    /* Sidebar Navigation Styling */
    .stRadio [data-testid="stWidgetLabel"] { display: none; }
    div[role="radiogroup"] { gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA RESOLVER (Unbreakable Pathing) ---
def resolve_path(filename):
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files: return os.path.join(root, filename)
    return filename

@st.cache_data
def load_quantum_engine():
    df = pd.read_csv(resolve_path('swiggy_simulated_data.csv'))
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_quantum_engine()

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h3 style='color: #FC8019; letter-spacing: 2px;'>CORE MODULES</h3>", unsafe_allow_html=True)
    page = st.radio("Navigation", 
                    ["GROWTH VECTORS", "LOGISTICS NEURAL", "FINANCIAL QUANT", "RISK ANALYSIS"])
    
    st.markdown("---")
    st.caption("SYSTEM STATUS: ONLINE")
    st.caption(f"KERNEL: V3.13-PRO")

# --- 4. MAIN BODY: LOGO & CONSOLE ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
logo = resolve_path('image_d988b9.png')
if os.path.exists(logo): 
    st.image(logo, width=160)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] ACCESSING_MODULE: {page}<br>
    [{datetime.now().strftime('%H:%M:%S')}] NODES_RESOLVED: {len(df)} | ENCRYPTION: ACTIVE
</div>
""", unsafe_allow_html=True)

# Automated Risk Toast
if df['freshness_hrs_left'].min() < 5:
    st.toast("🚨 SYSTEM ALERT: Perishable Decay Detected", icon="⚠️")

# --- 5. MODULAR GRID LOGIC ---

# PAGE: GROWTH VECTORS
if page == 'GROWTH_VECTORS':
    st.markdown("### 🛰️ Growth & Temporal Matrices")
    c1, c2, c3 = st.columns(3)
    with c1: st.plotly_chart(px.area(df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', title="1. Temporal Volume", template="plotly_dark", color_discrete_sequence=['#FC8019']), use_container_width=True)
    with c2: st.plotly_chart(px.pie(df, names='zone', values='order_value', hole=0.6, title="2. Regional Concentration", template="plotly_dark"), use_container_width=True)
    with c3: st.plotly_chart(px.bar(df.groupby('category')['order_value'].sum().reset_index(), x='category', y='order_value', title="3. Categorical Alpha", template="plotly_dark"), use_container_width=True)

# PAGE: LOGISTICS NEURAL
elif page == 'LOGISTICS_NEURAL':
    st.markdown("### 🧠 Fleet Dynamics & Velocity")
    c1, c2, c3 = st.columns(3)
    with c1: st.plotly_chart(px.box(df, x="weather", y="delivery_time_mins", title="4. Climatic SLA Variance", template="plotly_dark"), use_container_width=True)
    with c2: st.plotly_chart(px.line(df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins', title="5. Hourly SLA Reliability", template="plotly_dark"), use_container_width=True)
    with c3: st.plotly_chart(px.density_contour(df, x="delivery_time_mins", y="order_value", title="6. Velocity Density", template="plotly_dark"), use_container_width=True)

# PAGE: FINANCIAL QUANT
elif page == 'FINANCIAL_QUANT':
    st.markdown("### 💎 Unit Economics & Alpha")
    c1, c2, c3 = st.columns(3)
    with c1: st.plotly_chart(px.scatter(df, x="discount", y="contribution_margin", trendline="ols", title="7. Discount Elasticity", template="plotly_dark"), use_container_width=True)
    with c2: st.plotly_chart(px.violin(df, y="margin_rate", x="zone", box=True, title="8. Zonal Margin Stability", template="plotly_dark"), use_container_width=True)
    with c3: st.plotly_chart(px.scatter(df, x="delivery_cost", y="contribution_margin", title="9. Cost/Margin Correlation", template="plotly_dark"), use_container_width=True)

# PAGE: RISK ANALYSIS
elif page == 'RISK_ANALYSIS':
    st.markdown("### 🚨 Forensic Risk & 3D Vectors")
    c1, c2, c3 = st.columns(3)
    with c1: st.plotly_chart(px.histogram(df, x="delivery_cost", title="10. Logistics Overhead Risk", template="plotly_dark"), use_container_width=True)
    with c2: st.plotly_chart(px.scatter(df, x="freshness_hrs_left", y="order_value", color="category", title="11. Perishable Decay Risk", template="plotly_dark"), use_container_width=True)
    with c3: st.plotly_chart(px.scatter_3d(df.sample(500), x='order_value', y='delivery_time_mins', z='margin_rate', color='zone', title="12. 3D Operational Space", template="plotly_dark"), use_container_width=True)

# Global Metrics Footer
st.markdown("---")
f1, f2, f3, f4 = st.columns(4)
f1.metric("TOTAL GMV", f"₹{df['order_value'].sum()/1e5:.1f}L")
f2.metric("AVG MARGIN", f"{df['margin_rate'].mean():.1f}%")
f3.metric("SYSTEM SLA", f"{df['delivery_time_mins'].mean():.1f}m")
f4.metric("ALPHA STATUS", "ACTIVE")
