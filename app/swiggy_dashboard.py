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

# --- 2. DYNAMIC THEME ENGINE (LIGHT & DARK) ---
def apply_theme(theme_choice):
    if theme_choice == "Deep Neural (Dark)":
        bg, text, card, accent = "#050505", "#8F9BB3", "#0F0F12", "#FC8019"
        plot_bg = "rgba(0,0,0,0)"
    else:
        bg, text, card, accent = "#FFFFFF", "#282C3F", "#F4F4F5", "#FC8019"
        plot_bg = "#FFFFFF"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
        .stApp {{ background-color: {bg}; color: {text}; font-family: 'JetBrains Mono', monospace; }}
        [data-testid="stSidebar"] {{ background-color: {card} !important; border-right: 1px solid #ddd; }}
        .stMetric {{ background: {card} !important; border: 1px solid {accent}44 !important; border-radius: 8px; padding: 15px !important; }}
        [data-testid="stMetricValue"] {{ color: {accent} !important; font-size: 1.8rem !important; }}
        .console-box {{ 
            background: #000; color: #00FF41; padding: 12px; border-radius: 4px; 
            font-size: 0.75rem; border: 1px solid #00FF4133; margin-bottom: 25px; 
            font-family: 'JetBrains Mono';
        }}
        .header-box {{ text-align: center; padding: 10px 0; }}
        </style>
    """, unsafe_allow_html=True)
    return plot_bg

# --- 3. DATA & LOGO RESOLVER ---
def resolve_path(filename):
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files: return os.path.join(root, filename)
    return filename

@st.cache_data
def load_quantum_engine():
    path = resolve_path('swiggy_simulated_data.csv')
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_quantum_engine()

# --- 4. SIDEBAR: LOGO, NAVIGATION & FILTERS ---
with st.sidebar:
    # Sidebar Top Logo
    logo_file = resolve_path('Logo.png')
    if os.path.exists(logo_file): st.image(logo_file, use_container_width=True)
    
    st.markdown("### 🎛️ CONTROL PANEL")
    
    # Theme Toggle
    theme_choice = st.selectbox("VISUAL ENGINE", ["Deep Neural (Dark)", "Swiggy Standard (Light)"])
    plot_bg_color = apply_theme(theme_choice)
    
    st.markdown("---")
    
    # Navigation
    page = st.radio("INTELLIGENCE MODULE", 
                    ["GROWTH_VECTORS", "LOGISTICS_NEURAL", "FINANCIAL_QUANT", "RISK_ANALYSIS"])
    
    st.markdown("---")
    
    # Global Filters
    st.markdown("#### 🔍 FILTERS")
    zone_filter = st.multiselect("LOCATION (ZONE)", df['zone'].unique(), default=df['zone'].unique())
    weather_filter = st.multiselect("WEATHER", df['weather'].unique(), default=df['weather'].unique())
    market_filter = st.multiselect("MARKET (CATEGORY)", df['category'].unique(), default=df['category'].unique())

# Apply Filters to Data
f_df = df[(df['zone'].isin(zone_filter)) & 
          (df['weather'].isin(weather_filter)) & 
          (df['category'].isin(market_filter))]

# --- 5. MAIN STAGE: TOP LOGO & CONSOLE ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
if os.path.exists(logo_file): 
    st.image(logo_file, width=180)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] MODULE: {page} | FILTERS: ACTIVE<br>
    [{datetime.now().strftime('%H:%M:%S')}] DATA_STREAM: {len(f_df)} NODES | THEME: {theme_choice}
</div>
""", unsafe_allow_html=True)

# --- 6. CHART RENDERING UTILITY ---
def render_quantum_chart(fig):
    t = "plotly_dark" if theme_choice == "Deep Neural (Dark)" else "plotly_white"
    fig.update_layout(
        template=t,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 7. MODULAR PAGES ---
if page == 'GROWTH_VECTORS':
    st.markdown("#### 🛰️ REVENUE & TEMPORAL GROWTH")
    c1, c2, c3 = st.columns(3)
    with c1: render_quantum_chart(px.area(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', title="Hourly GMV Flow", color_discrete_sequence=['#FC8019']))
    with c2: render_quantum_chart(px.pie(f_df, names='zone', values='order_value', hole=0.5, title="Geographic Weight"))
    with c3: render_quantum_chart(px.bar(f_df.groupby('category')['order_value'].sum().reset_index(), x='category', y='order_value', title="Market Alpha"))

elif page == 'LOGISTICS_NEURAL':
    st.markdown("#### 🧠 LOGISTICS & FLEET VELOCITY")
    c1, c2, c3 = st.columns(3)
    with c1: render_quantum_chart(px.box(f_df, x="weather", y="delivery_time_mins", color="weather", title="SLA Weather Impact"))
    with c2: render_quantum_chart(px.line(f_df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins', title="Circadian Velocity"))
    with c3: render_quantum_chart(px.density_heatmap(f_df, x="delivery_time_mins", y="order_value", title="Velocity/Value Density"))

elif page == 'FINANCIAL_QUANT':
    st.markdown("#### 💎 MARGIN & UNIT ECONOMICS")
    c1, c2, c3 = st.columns(3)
    with c1: render_quantum_chart(px.scatter(f_df, x="discount", y="contribution_margin", trendline="ols", title="Discount Elasticity"))
    with c2: render_quantum_chart(px.violin(f_df, y="margin_rate", x="zone", box=True, title="Regional Margin Stability"))
    with c3: render_quantum_chart(px.scatter(f_df, x="delivery_cost", y="contribution_margin", color="category", title="Logistics vs Profit"))

elif page == 'RISK_ANALYSIS':
    st.markdown("#### 🚨 FORENSIC RISK VECTORS")
    c1, c2, c3 = st.columns(3)
    with c1: render_quantum_chart(px.histogram(f_df, x="delivery_cost", title="Delivery Overhead Risk"))
    with c2: render_quantum_chart(px.scatter(f_df, x="freshness_hrs_left", y="order_value", color="category", title="Perishable Decay Vector"))
    with c3: render_quantum_chart(px.scatter_3d(f_df.sample(min(500, len(f_df))), x='order_value', y='delivery_time_mins', z='margin_rate', color='zone', title="3D Operational Space"))

# --- 8. FOOTER SUMMARY ---
st.markdown("---")
f1, f2, f3, f4 = st.columns(4)
f1.metric("FILTERED GMV", f"₹{f_df['order_value'].sum()/1e5:.2f}L")
f2.metric("AVG MARGIN", f"{f_df['margin_rate'].mean():.1f}%")
f3.metric("SLA (MEAN)", f"{f_df['delivery_time_mins'].mean():.1f}m")
f4.metric("SYSTEM STATUS", "OPTIMIZED")
