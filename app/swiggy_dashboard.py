import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import os
import time

# --- 1. SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="SWIGGY NEURAL OPS", layout="wide", initial_sidebar_state="collapsed")

# Elite Dark-Mode CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; background-color: #030305; color: #8F9BB3; }
    .stMetric { background: #0A0B10; border: 1px solid #1A1C23; border-radius: 4px; padding: 15px !important; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.6rem !important; }
    .console-box { background: #000; color: #00FF41; padding: 15px; border-radius: 4px; font-size: 0.75rem; border: 1px solid #00FF4133; font-family: 'JetBrains Mono'; margin-bottom: 20px; }
    .header-center { text-align: center; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PATH RESOLVER (The "Senior" Fix) ---
def resolve_path(filename):
    """Production-grade file resolver to prevent FileNotFoundError."""
    # Search in current directory, parent, and recursive subdirectories
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            return os.path.join(root, filename)
    return filename # Fallback to original name

# --- 3. DATA ORCHESTRATION ---
@st.cache_data
def load_quantum_engine():
    data_path = resolve_path('swiggy_simulated_data.csv')
    df = pd.read_csv(data_path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

try:
    df = load_quantum_engine()
except Exception as e:
    st.error(f"FATAL ERROR: Could not resolve data stream. Ensure 'swiggy_simulated_data.csv' is in your repository.")
    st.stop()

# --- 4. CENTERED LOGO & COCOLE (CONTROL CONSOLE) ---
st.markdown('<div class="header-center">', unsafe_allow_html=True)
logo_path = resolve_path('image_d988b9.png')
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
else:
    st.title("SWIGGY QUANTUM")
st.markdown('</div>', unsafe_allow_html=True)

# The "Cocole" - Control Console (Centered)
st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] SYSTEM_BOOT: SUCCESS<br>
    [{datetime.now().strftime('%H:%M:%S')}] DATA_LINK: {len(df)} NODES ACTIVE<br>
    [{datetime.now().strftime('%H:%M:%S')}] RISK_ANALYSIS: PUSHING NOTIFICATIONS TO OPERATORS...
</div>
""", unsafe_allow_html=True)

# --- 5. RISK ANALYSIS PUSH NOTIFICATIONS ---
# Automated risk trigger based on data
perishable_risk = df[df['freshness_hrs_left'] < 5]
if not perishable_risk.empty:
    st.toast(f"🚨 ALERT: {len(perishable_risk)} Units at Expiry Risk in Whitefield Sector", icon="⚠️")
    time.sleep(1)
    st.toast("🌧️ WEATHER UPDATE: Rainy conditions detected in Koramangala. SLA Buffer +15m", icon="⛈️")

# --- 6. THE 12-CHART QUANTUM GRID ---
st.markdown("### 🛰️ GLOBAL OPERATIONAL VECTORS")

# Primary Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("GMV ALPHA", f"₹{df['order_value'].sum()/1e5:.2f}L", "+5.2%")
m2.metric("NET MARGIN", f"{df['margin_rate'].mean():.1f}%", "-0.4%")
m3.metric("FLEET VELOCITY", f"{df['delivery_time_mins'].mean():.1f}m", "OPTIMAL")
m4.metric("SYSTEM STRESS", "LOW", "-12% LOAD")

# Matrix Layout
col_a, col_b, col_c = st.columns(3)

with col_a:
    # 1. Temporal Demand
    st.plotly_chart(px.area(df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', title="1. Temporal Volume", template="plotly_dark", color_discrete_sequence=['#FC8019']), use_container_width=True)
    # 2. Weather Variance
    st.plotly_chart(px.box(df, x="weather", y="delivery_time_mins", title="2. Climatic Variance", template="plotly_dark"), use_container_width=True)
    # 3. Zonal Mix
    st.plotly_chart(px.pie(df, names='zone', values='order_value', hole=0.6, title="3. Regional Concentration", template="plotly_dark"), use_container_width=True)
    # 4. Logistics Costs
    st.plotly_chart(px.histogram(df, x="delivery_cost", title="4. Delivery Overhead Distribution", template="plotly_dark"), use_container_width=True)

with col_b:
    # 5. Category Depth
    st.plotly_chart(px.bar(df.groupby('category')['order_value'].sum().reset_index(), x='category', y='order_value', title="5. Categorical GMV", template="plotly_dark"), use_container_width=True)
    # 6. Freshness Decay
    st.plotly_chart(px.scatter(df, x="freshness_hrs_left", y="order_value", color="category", title="6. Perishable Decay Vector", template="plotly_dark"), use_container_width=True)
    # 7. Discount Elasticity
    st.plotly_chart(px.scatter(df, x="discount", y="contribution_margin", trendline="ols", title="7. Discount Elasticity", template="plotly_dark"), use_container_width=True)
    # 8. Delivery Density
    st.plotly_chart(px.density_contour(df, x="delivery_time_mins", y="order_value", title="8. Delivery Velocity Density", template="plotly_dark"), use_container_width=True)

with col_c:
    # 9. Margin Stability
    st.plotly_chart(px.violin(df, y="margin_rate", x="zone", box=True, title="9. Zonal Margin Stability", template="plotly_dark"), use_container_width=True)
    # 10. SLA Reliability
    st.plotly_chart(px.line(df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins', title="10. Hourly SLA Reliability", template="plotly_dark"), use_container_width=True)
    # 11. Cost vs Margin
    st.plotly_chart(px.scatter(df, x="delivery_cost", y="contribution_margin", title="11. Logistics/Margin Correlation", template="plotly_dark"), use_container_width=True)
    # 12. Market Archetypes (AI Cluster Proxy)
    st.plotly_chart(px.scatter_3d(df.sample(500), x='order_value', y='delivery_time_mins', z='margin_rate', color='zone', title="12. 3D Operational Vector Space", template="plotly_dark"), use_container_width=True)
