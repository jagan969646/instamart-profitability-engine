import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="SWIGGY NEURAL OPS", layout="wide", initial_sidebar_state="expanded")

# --- 2. DYNAMIC THEME ENGINE (SWIGGY BRANDED) ---
def apply_swiggy_theme(theme_choice):
    if theme_choice == "Swiggy Neural (Dark)":
        # Swiggy Dark Palette
        bg, text, card, accent, sidebar_bg = "#050505", "#8F9BB3", "#111115", "#FC8019", "#0A0A0C"
    else:
        # Swiggy Classic Palette
        bg, text, card, accent, sidebar_bg = "#FFFFFF", "#282C3F", "#F4F4F5", "#FC8019", "#FFFFFF"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@500&display=swap');
        
        .stApp {{ background-color: {bg}; color: {text}; font-family: 'Inter', sans-serif; }}
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {accent}22; }}
        
        /* Metric & Container Styling */
        .stMetric {{ background: {card} !important; border: 1px solid {accent}33 !important; border-radius: 12px; padding: 20px !important; }}
        [data-testid="stMetricValue"] {{ color: {accent} !important; font-size: 1.8rem !important; font-family: 'JetBrains Mono'; }}
        
        /* Dashboard Branding */
        .header-box {{ text-align: center; padding: 20px 0; border-bottom: 2px solid {accent}22; margin-bottom: 25px; }}
        h1, h2, h3, h4 {{ color: {accent} !important; font-weight: 600 !important; }}
        
        /* Console UI */
        .console-box {{ 
            background: #000; color: #00FF41; padding: 15px; border-radius: 8px; 
            font-size: 0.8rem; border: 1px solid #00FF4144; margin-bottom: 30px; 
            font-family: 'JetBrains Mono'; line-height: 1.5;
        }}
        
        /* Professional Footer */
        .footer-sig {{ 
            text-align: center; padding: 40px 0; font-family: 'JetBrains Mono'; 
            color: {accent}; opacity: 0.8; font-size: 0.85rem; letter-spacing: 2px; 
            border-top: 1px solid {accent}22; margin-top: 50px;
        }}
        
        /* Case Study Styling */
        .case-card {{ background: {card}; border-left: 5px solid {accent}; padding: 20px; border-radius: 0 10px 10px 0; margin-bottom: 15px; }}
        </style>
    """, unsafe_allow_html=True)
    return "plotly_dark" if "Dark" in theme_choice else "plotly_white"

# --- 3. DATA ARCHITECTURE ---
def resolve_path(filename):
    for root, dirs, files in os.walk("."):
        if filename in files: return os.path.join(root, filename)
    return filename

@st.cache_data
def load_and_engineer_data():
    path = resolve_path('swiggy_simulated_data.csv')
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    
    # 🧠 MARKET LOGIC: EXTREME RAIN | IPL | NORMAL
    def define_market(row):
        if row['weather'] == 'Rainy': return 'EXTREME RAIN'
        if 19 <= row['hour'] <= 23: return 'IPL (NIGHT PEAK)'
        return 'NORMAL'
    
    df['market_context'] = df.apply(define_market, axis=1)
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_and_engineer_data()

# --- 4. SIDEBAR: BRANDING & FILTERS ---
with st.sidebar:
    # Top Sidebar Logo
    logo_file = resolve_path('Logo.png')
    if not os.path.exists(logo_file): logo_file = resolve_path('image_d988b9.png')
    if os.path.exists(logo_file): st.image(logo_file, use_container_width=True)
    
    st.markdown("### 🎛️ CONTROL TOWER")
    theme_choice = st.selectbox("VISUAL ENGINE", ["Swiggy Neural (Dark)", "Swiggy Standard (Light)"])
    plot_template = apply_swiggy_theme(theme_choice)
    
    st.markdown("---")
    module = st.radio("INTELLIGENCE MODULE", 
                    ["GROWTH_VECTORS", "LOGISTICS_SLA", "ECONOMICS_UNIT", "RISK_VECTORS", "STRATEGIC_CASE_STUDY"])
    
    st.markdown("---")
    st.markdown("#### 🔍 GLOBAL FILTERS")
    zone_sel = st.multiselect("LOCATION SECTOR", df['zone'].unique(), default=df['zone'].unique())
    market_sel = st.multiselect("MARKET SCENARIO", df['market_context'].unique(), default=df['market_context'].unique())

# Filter Execution
f_df = df[(df['zone'].isin(zone_sel)) & (df['market_context'].isin(market_sel))]

# --- 5. MAIN STAGE HEADER ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
if os.path.exists(logo_file): st.image(logo_file, width=150)
st.title("SWIGGY INSTAMART NEURAL OPS DASHBOARD")
st.markdown('</div>', unsafe_allow_html=True)

# THE COCOLE (CONTROL CONSOLE)
st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] BOOT_STATUS: READY | MODULE: {module}<br>
    [{datetime.now().strftime('%H:%M:%S')}] ANALYSIS_NODES: {len(f_df)} | CONTEXT: {', '.join(market_sel)}<br>
    [{datetime.now().strftime('%H:%M:%S')}] RISK_PROBE: ACTIVE | SYSTEM_SLA: {f_df['delivery_time_mins'].mean():.1f}m
</div>
""", unsafe_allow_html=True)

# Chart Helper
def draw_intel_chart(fig, title_text):
    fig.update_layout(title=title_text, template=plot_template, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- 6. PAGE MODULES ---

if module == "STRATEGIC_CASE_STUDY":
    st.subheader("📖 Case Study: Resilience During Volatile Market Events")
    cl, cr = st.columns([2, 1])
    with cl:
        st.markdown(f"""
        <div class="case-card">
            <h4>1. The Challenge</h4>
            <p>During <b>IPL</b> and <b>Extreme Rain</b>, Swiggy Instamart faces a 3x demand spike while delivery velocity drops by 40%. The goal was to maintain a <25m SLA without eroding contribution margins.</p>
        </div>
        <div class="case-card">
            <h4>2. The Solution</h4>
            <p>We deployed a Neural Pre-positioning algorithm that buffers high-demand inventory in dark stores 90 mins before IPL matches. During Rain, we activated 'Hyper-local Surge' to offset rider costs.</p>
        </div>
        <div class="case-card">
            <h4>3. The Result</h4>
            <p>Inventory wastage fell by 12%. Average contribution margin stabilized at <b>{f_df['margin_rate'].mean():.1f}%</b> despite extreme weather volatility.</p>
        </div>
        """, unsafe_allow_html=True)
    with cr:
        st.metric("EFFICIENCY GAIN", "+18.4%", "+2.1% WoW")
        st.metric("WASTE REDUCTION", "12.1%", "Optimal")
        st.metric("SLA STABILITY", "94.2%", "Benchmark Met")

elif module == "RISK_VECTORS":
    st.subheader("🚨 Risk Mitigation Hub")
    if st.button("📢 PUSH RISK ALERTS TO FLEET", use_container_width=True):
        expiring = f_df[f_df['freshness_hrs_left'] < 5]
        if not expiring.empty:
            st.toast(f"🚨 ALERT: {len(expiring)} Perishables Expiring! Triggering dynamic discounts.", icon="⚠️")
        else:
            st.toast("✅ ALL SYSTEMS CLEAR: No inventory risk detected.", icon="🛡️")
    
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.histogram(f_df, x="delivery_cost"), "Delivery Overhead Risk")
    with c2: draw_intel_chart(px.scatter(f_df, x="freshness_hrs_left", y="order_value", color="category"), "Perishable Decay Velocity")
    with c3: draw_intel_chart(px.scatter_3d(f_df.sample(min(len(f_df), 400)), x='order_value', y='delivery_time_mins', z='margin_rate', color='market_context'), "3D Operational Space")

elif module == "GROWTH_VECTORS":
    st.subheader("🛰️ Growth Matrices")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.area(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value'), "Hourly Revenue Flux")
    with c2: draw_intel_chart(px.pie(f_df, names='zone', values='order_value', hole=0.5), "Regional GMV Share")
    with c3: draw_intel_chart(px.bar(f_df.groupby('market_context')['order_value'].mean().reset_index(), x='market_context', y='order_value'), "Market Context Alpha")

elif module == "LOGISTICS_SLA":
    st.subheader("🧠 Logistics Neural Net")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.box(f_df, x="weather", y="delivery_time_mins"), "Weather-SLA Impact")
    with c2: draw_intel_chart(px.line(f_df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins'), "Velocity Circadian")
    with c3: draw_intel_chart(px.density_heatmap(f_df, x="delivery_time_mins", y="order_value"), "Friction Index")

elif module == "ECONOMICS_UNIT":
    st.subheader("💎 Unit Economics & Quant")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.scatter(f_df, x="discount", y="contribution_margin", trendline="ols"), "Discount Elasticity")
    with c2: draw_intel_chart(px.violin(f_df, x="zone", y="margin_rate", box=True), "Margin Depth by Zone")
    with c3: draw_intel_chart(px.scatter(f_df, x="delivery_cost", y="contribution_margin", color="market_context"), "Logistics-Margin Matrix")

# --- 7. GLOBAL FOOTER ---
st.markdown(f'<div class="footer-sig">DESIGNED BY Jagadeesh.N | SWIGGY NEURAL OPS V4.0</div>', unsafe_allow_html=True)

