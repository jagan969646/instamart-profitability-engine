import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="SWIGGY NEURAL OPS | ELITE", layout="wide", initial_sidebar_state="expanded")

# --- 2. DYNAMIC THEME ENGINE (SWIGGY BRANDED) ---
def apply_swiggy_theme(theme_choice):
    if theme_choice == "Swiggy Neural (Dark)":
        # Deep Indigo/Black Swiggy Dark
        bg, text, card, accent, sidebar_bg = "#050505", "#8F9BB3", "#111115", "#FC8019", "#0A0A0C"
        plot_bg = "rgba(0,0,0,0)"
        grid_color = "#1A1C23"
    else:
        # Swiggy Clean White
        bg, text, card, accent, sidebar_bg = "#FFFFFF", "#282C3F", "#F4F4F5", "#FC8019", "#FFFFFF"
        plot_bg = "#FFFFFF"
        grid_color = "#EEEEEE"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@300;500&display=swap');
        
        .stApp {{ background-color: {bg}; color: {text}; font-family: 'Inter', sans-serif; }}
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {accent}22; }}
        
        /* Metric & Container Styling */
        .stMetric {{ background: {card} !important; border: 1px solid {accent}33 !important; border-radius: 12px; padding: 20px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        [data-testid="stMetricValue"] {{ color: {accent} !important; font-size: 2rem !important; font-family: 'JetBrains Mono'; font-weight: 500; }}
        [data-testid="stMetricLabel"] {{ font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 1.2px; }}
        
        /* Console UI */
        .console-box {{ 
            background: #000; color: #00FF41; padding: 15px; border-radius: 8px; 
            font-size: 0.8rem; border: 1px solid #00FF4144; margin-bottom: 30px; 
            font-family: 'JetBrains Mono'; line-height: 1.6; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        /* Header & Logo */
        .header-box {{ text-align: center; padding: 20px 0; }}
        
        /* Navigation Buttons Customization */
        div[data-testid="stRadio"] > label {{ display: none; }}
        .stRadio label {{ font-weight: 600 !important; color: {accent} !important; }}
        </style>
    """, unsafe_allow_html=True)
    return plot_bg, grid_color

# --- 3. DATA ARCHITECTURE & PATH RESOLVER ---
def find_file(name):
    for root, dirs, files in os.walk("."):
        if name in files: return os.path.join(root, name)
    return name

@st.cache_data
def load_and_engineer_data():
    path = find_file('swiggy_simulated_data.csv')
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    
    # ADVANCED FEATURE ENGINEERING: MARKET CONTEXT
    # Defining Market scenarios based on complex logic
    def define_market(row):
        if row['weather'] == 'Rainy' and row['delivery_time_mins'] > 25:
            return 'EXTREME RAIN'
        elif row['hour'] >= 19 and row['hour'] <= 23:
            return 'IPL NIGHT'
        else:
            return 'NORMAL'
            
    df['market_context'] = df.apply(define_market, axis=1)
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

try:
    df = load_and_engineer_data()
except Exception as e:
    st.error(f"SYSTEM_SYNC_ERROR: {e}")
    st.stop()

# --- 4. SIDEBAR: THE CONTROL TOWER ---
with st.sidebar:
    # Top Sidebar Logo
    logo_path = find_file('Logo.png')
    if not os.path.exists(logo_path): logo_path = find_file('image_d988b9.png') # Fallback
    
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    
    st.markdown("### 🎛️ SYSTEM CONTROLS")
    
    # Theme Selection
    theme_choice = st.selectbox("CORE THEME ENGINE", ["Swiggy Neural (Dark)", "Swiggy Standard (Light)"])
    plot_bg, grid_col = apply_swiggy_theme(theme_choice)
    
    st.markdown("---")
    
    # Module Navigation
    module = st.radio("SELECT INTEL MODULE", 
                    ["REVENUE_GROWTH", "LOGISTICS_SLA", "ECONOMICS_UNIT", "RISK_VECTORS"])
    
    st.markdown("---")
    
    # MULTI-DIMENSIONAL FILTERS
    st.markdown("#### 🔍 SEGMENT FILTERS")
    zone_sel = st.multiselect("LOCATION SECTOR", df['zone'].unique(), default=df['zone'].unique())
    market_sel = st.multiselect("MARKET SCENARIO", df['market_context'].unique(), default=df['market_context'].unique())
    weather_sel = st.multiselect("WEATHER VECTORS", df['weather'].unique(), default=df['weather'].unique())

# Apply Intelligence Filters
f_df = df[(df['zone'].isin(zone_sel)) & 
          (df['market_context'].isin(market_sel)) & 
          (df['weather'].isin(weather_sel))]

# --- 5. MAIN INTERFACE: BRANDING & COCOLE ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
if os.path.exists(logo_path):
    st.image(logo_path, width=200)
st.markdown('</div>', unsafe_allow_html=True)

# THE COCOLE (CONTROL CONSOLE)
st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] BOOT_SEQUENCE: COMPLETED<br>
    [{datetime.now().strftime('%H:%M:%S')}] ACTIVE_MODULE: {module}<br>
    [{datetime.now().strftime('%H:%M:%S')}] CONTEXT_FILTER: {', '.join(market_sel)}<br>
    [{datetime.now().strftime('%H:%M:%S')}] ANALYSIS_NODES: {len(f_df)} | STATUS: OPTIMIZED
</div>
""", unsafe_allow_html=True)

# --- 6. PUSH NOTIFICATIONS (RISK ANALYSIS) ---
expiring_items = f_df[f_df['freshness_hrs_left'] < 5]
if not expiring_items.empty:
    st.toast(f"🚨 CRITICAL RISK: {len(expiring_items)} PRODUCTS EXPIRING WITHIN 5 HOURS", icon="⚠️")
    time.sleep(0.5)
    st.toast("⚡ ACTION REQUIRED: Trigger dynamic discounts for expiring inventory in " + f_df['zone'].iloc[0], icon="💸")

# --- 7. MODULAR CHART ENGINE (WITH TITLES) ---
def render_intel_chart(fig, title_text):
    t = "plotly_dark" if "Dark" in theme_choice else "plotly_white"
    fig.update_layout(
        title=dict(text=title_text, font=dict(size=18, family="Inter", weight="bold")),
        template=t,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# PAGE ROUTING
if module == 'REVENUE_GROWTH':
    st.markdown("### 📊 GROWTH STRATEGY MATRIX")
    c1, c2, c3 = st.columns(3)
    with c1: render_intel_chart(px.area(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', title="Hourly Volume Vector"), "1. HOURLY VOLUME FLOW")
    with c2: render_intel_chart(px.pie(f_df, names='zone', values='order_value', hole=0.6, title="Geographic Revenue Concentration"), "2. REGIONAL MARKET SHARE")
    with c3: render_intel_chart(px.bar(f_df.groupby('market_context')['order_value'].mean().reset_index(), x='market_context', y='order_value', color='market_context', title="Revenue per Market Context"), "3. MARKET CONTEXT ALPHA")

elif module == 'LOGISTICS_SLA':
    st.markdown("### 🧠 LOGISTICS NEURAL NET")
    c1, c2, c3 = st.columns(3)
    with c1: render_intel_chart(px.box(f_df, x="weather", y="delivery_time_mins", color="weather", title="Weather-Induced Latency Variance"), "4. CLIMATIC SLA VARIANCE")
    with c2: render_intel_chart(px.line(f_df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins', title="Temporal Velocity Trend"), "5. CIRCADIAN VELOCITY")
    with c3: render_intel_chart(px.density_heatmap(f_df, x="delivery_time_mins", y="order_value", title="Velocity/Value Cluster Density"), "6. LOGISTICS FRICTION INDEX")

elif module == 'ECONOMICS_UNIT':
    st.markdown("### 💎 UNIT ECONOMICS & QUANT")
    c1, c2, c3 = st.columns(3)
    with c1: render_intel_chart(px.scatter(f_df, x="discount", y="contribution_margin", trendline="ols", title="Discount Elasticity Attribution"), "7. DISCOUNT ELASTICITY")
    with c2: render_intel_chart(px.violin(f_df, y="margin_rate", x="zone", box=True, title="Zonal Margin Stability Profiles"), "8. REGIONAL MARGIN DEPTH")
    with c3: render_intel_chart(px.scatter(f_df, x="delivery_cost", y="contribution_margin", color="market_context", title="Logistics vs Margin Correlation"), "9. LOGISTICS OVERHEAD EFFICIENCY")

elif module == 'RISK_VECTORS':
    st.markdown("### 🚨 FORENSIC RISK ANALYSIS")
    c1, c2, c3 = st.columns(3)
    with c1: render_intel_chart(px.histogram(f_df, x="delivery_cost", nbins=30, title="Delivery Cost Risk Distribution"), "10. COST OVERHEAD ANOMALIES")
    with c2: render_intel_chart(px.scatter(f_df, x="freshness_hrs_left", y="order_value", color="category", size="delivery_time_mins", title="Inventory Decay Velocity"), "11. PERISHABLE DECAY VECTOR")
    with c3: render_intel_chart(px.scatter_3d(f_df.sample(min(400, len(f_df))), x='order_value', y='delivery_time_mins', z='margin_rate', color='market_context', title="High-Dimensional Operational Space"), "12. 3D SYSTEM VECTORS")

# --- 8. FOOTER: REAL-TIME TELEMETRY ---
st.markdown("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric("SEGMENT GMV", f"₹{f_df['order_value'].sum()/1e5:.2f}L", "+4.2% Alpha")
m2.metric("MEAN MARGIN", f"{f_df['margin_rate'].mean():.1f}%", "-0.2% Bias")
m3.metric("AVG VELOCITY", f"{f_df['delivery_time_mins'].mean():.1f}m", "Optimal")
m4.metric("RISK LOAD", f"{len(expiring_items)} NODES", "ACTION REQ.", delta_color="inverse")
