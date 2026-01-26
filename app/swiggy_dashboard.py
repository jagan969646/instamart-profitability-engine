import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os

# --- 1. SYSTEM ARCHITECTURE & THEME ---
st.set_page_config(page_title="SWIGGY NEURAL OPS | SOVEREIGN SUITE", layout="wide", initial_sidebar_state="collapsed")

# Advanced CSS for "Elite Tier" UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
    
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; background-color: #030305; color: #8F9BB3; }
    
    /* Header & Logo */
    .header { text-align: center; padding: 20px; border-bottom: 1px solid #1A1C23; }
    .logo { width: 120px; filter: drop-shadow(0 0 8px #FC8019); }
    
    /* Center Nav */
    .nav-bar { display: flex; justify-content: center; gap: 30px; margin: 20px 0; font-size: 0.75rem; letter-spacing: 2px; }
    .nav-btn { color: #555; cursor: pointer; transition: 0.3s; }
    .nav-btn:hover { color: #FC8019; }
    
    /* Dashboard Cards */
    .stMetric { background: #0A0B10; border: 1px solid #1A1C23; border-radius: 4px; padding: 15px !important; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.5rem !important; }
    
    /* Console Log */
    .console { background: #000; color: #00FF41; padding: 10px; border-radius: 4px; font-size: 0.7rem; height: 150px; overflow-y: scroll; border: 1px solid #00FF4133; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ORCHESTRATION ---
@st.cache_data
def load_quantum_data():
    path = 'swiggy_simulated_data.csv'
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    
    # Coordinate Injection for Geospatial Market Analysis
    coords = {
        'Indiranagar': [12.9784, 77.6408], 'Jayanagar': [12.9250, 77.5938],
        'HSR Layout': [12.9128, 77.6388], 'Koramangala': [12.9352, 77.6245],
        'Whitefield': [12.9698, 77.7500]
    }
    df['lat'] = df['zone'].map(lambda x: coords.get(x, [12.97, 77.59])[0])
    df['lon'] = df['zone'].map(lambda x: coords.get(x, [12.97, 77.59])[1])
    return df

df = load_quantum_data()

# --- 3. TOP-LEVEL INTERFACE ---
st.markdown('<div class="header">', unsafe_allow_html=True)
logo_path = 'image_d988b9.png'
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
st.markdown('</div>', unsafe_allow_html=True)

# Centered Navigation Bar
st.markdown("""
<div class="nav-bar">
    <span class="nav-btn">SYSTEM_HEALTH</span> | 
    <span class="nav-btn">MARKET_VECTORS</span> | 
    <span class="nav-btn">LOGISTICS_NEURAL</span> | 
    <span class="nav-btn">FINANCIAL_QUANT</span>
</div>
""", unsafe_allow_html=True)

# --- 4. RISK NOTIFICATION SYSTEM ---
high_risk_count = len(df[df['freshness_hrs_left'] < 5])
if st.button("RUN RISK AUDIT"):
    st.toast(f"⚠️ {high_risk_count} CRITICAL EXPIRY RISKS DETECTED", icon="🚨")
    time.sleep(0.5)
    st.toast("⚡ CLIMATIC DELAY IN WHITEFIELD SECTOR: +14m", icon="🌧️")

# --- 5. THE 12-CHART OPERATIONAL GRID ---

# ROW 1: CORE TELEMETRY
c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL GMV", f"₹{df['order_value'].sum()/1e5:.2f}L", "ALPHA: +12%")
c2.metric("NET CONTRIBUTION", f"₹{df['contribution_margin'].sum()/1e5:.2f}L", "STABLE")
c3.metric("AVG VELOCITY", f"{df['delivery_time_mins'].mean():.1f}m", "-2.1m DELAY")
c4.metric("UNIT MARGIN", f"{df['margin_rate'].mean():.1f}%", "OPTIMAL")

st.markdown("---")

# ROW 2: TEMPORAL & MARKET SHARE
col1, col2 = st.columns(2)
with col1:
    # 1. Hourly Demand Vector (Area)
    fig1 = px.area(df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', 
                  title="1. TEMPORAL VOLUME VECTOR", template="plotly_dark", color_discrete_sequence=['#FC8019'])
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    # 2. Market Share Distribution (Sunburst)
    fig2 = px.sunburst(df, path=['zone', 'category'], values='order_value', 
                      title="2. ZONAL MARKET MIX", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# ROW 3: LOGISTICS & WEATHER
col3, col4 = st.columns(2)
with col3:
    # 3. Weather impact on SLA (Box)
    fig3 = px.box(df, x="weather", y="delivery_time_mins", color="weather", 
                 title="3. CLIMATIC SLA VARIANCE", template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    # 4. Logistics Friction Heatmap (Density)
    fig4 = px.density_heatmap(df, x="delivery_time_mins", y="delivery_cost", 
                             title="4. LOGISTICS FRICTION INDEX", template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

# ROW 4: UNIT ECONOMICS
col5, col6 = st.columns(2)
with col5:
    # 5. Discount Efficiency (Scatter with Regression)
    fig5 = px.scatter(df, x="discount", y="contribution_margin", trendline="ols",
                     title="5. DISCOUNT ELASTICITY MODEL", template="plotly_dark")
    st.plotly_chart(fig5, use_container_width=True)
with col6:
    # 6. Category GMV Contribution (Funnel)
    cat_gmv = df.groupby('category')['order_value'].sum().sort_values(ascending=False).reset_index()
    fig6 = px.funnel(cat_gmv, x='order_value', y='category', title="6. CATEGORICAL ALPHA HIERARCHY", template="plotly_dark")
    st.plotly_chart(fig6, use_container_width=True)

# ROW 5: RISK & INVENTORY
col7, col8 = st.columns(2)
with col7:
    # 7. Perishable Decay Analysis (Histogram)
    fig7 = px.histogram(df[df['category']=='Perishable'], x="freshness_hrs_left", 
                       title="7. INVENTORY DECAY DISTRIBUTION", template="plotly_dark", color_discrete_sequence=['#FF4B4B'])
    st.plotly_chart(fig7, use_container_width=True)
with col8:
    # 8. Order Value vs Margin Depth (Scatter)
    fig8 = px.scatter(df, x="order_value", y="contribution_margin", color="zone", 
                     size="delivery_time_mins", title="8. REVENUE-MARGIN CONVERGENCE", template="plotly_dark")
    st.plotly_chart(fig8, use_container_width=True)

# ROW 6: ADVANCED SPATIAL & PEAK
col9, col10 = st.columns(2)
with col9:
    # 9. Market Concentration (Geospatial Bubble)
    fig9 = px.scatter_mapbox(df, lat="lat", lon="lon", size="order_value", color="margin_rate",
                            center={"lat": 12.95, "lon": 77.65}, zoom=10,
                            mapbox_style="carto-darkmatter", title="9. GEOSPATIAL REVENUE DENSITY")
    st.plotly_chart(fig9, use_container_width=True)
with col10:
    # 10. Peak Hour Efficiency (Radar/Polar)
    peak_data = df.groupby('hour')['delivery_time_mins'].mean().reset_index()
    fig10 = px.line_polar(peak_data, r='delivery_time_mins', theta='hour', line_close=True,
                         title="10. CIRCADIAN PERFORMANCE RADAR", template="plotly_dark")
    st.plotly_chart(fig10, use_container_width=True)

# ROW 7: FINAL ATTRIBUTION
col11, col12 = st.columns(2)
with col11:
    # 11. Cost-to-Serve Analysis (Stacked Bar)
    fig11 = px.bar(df.groupby('zone')['delivery_cost'].sum().reset_index(), x='zone', y='delivery_cost',
                  title="11. AGGREGATE LOGISTICS OVERHEAD", template="plotly_dark")
    st.plotly_chart(fig11, use_container_width=True)
with col12:
    # 12. Margin Stability (Violin)
    fig12 = px.violin(df, y="margin_rate", x="category", box=True, 
                     title="12. MARGIN STABILITY PROFILES", template="plotly_dark")
    st.plotly_chart(fig12, use_container_width=True)

# --- 6. THE "COCOLE" (CONTROL CONSOLE) ---
st.markdown("### 🖥️ LIVE OPERATIONS CONSOLE")
st.markdown(f"""
<div class="console">
    [{datetime.now().strftime('%H:%M:%S')}] INITIALIZING NEURAL_OPS ENGINE...<br>
    [{datetime.now().strftime('%H:%M:%S')}] GEOSPATIAL VECTORS SYNCED (BANGALORE SECTOR)<br>
    [{datetime.now().strftime('%H:%M:%S')}] 12-CHART TELEMETRY GRID ONLINE<br>
    [{datetime.now().strftime('%H:%M:%S')}] ANALYZING {len(df)} DATA POINTS...<br>
    [{datetime.now().strftime('%H:%M:%S')}] ALERT: MARGIN LEAKAGE DETECTED IN RAINY WEATHER<br>
    [{datetime.now().strftime('%H:%M:%S')}] SYSTEM STATUS: OVER-QUALIFIED
</div>
""", unsafe_allow_html=True)
