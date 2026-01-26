import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime
import time

# --- 1. SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="SWIGGY NEURAL OPS", layout="wide", initial_sidebar_state="expanded")

# --- 2. THEME ENGINE (SWIGGY BRANDED LIGHT/DARK) ---
def apply_swiggy_theme(theme_choice):
    if theme_choice == "Swiggy Neural (Dark)":
        bg, text, card, accent, sidebar_bg = "#050505", "#8F9BB3", "#111115", "#FC8019", "#0A0A0C"
    else:
        bg, text, card, accent, sidebar_bg = "#FFFFFF", "#282C3F", "#F4F4F5", "#FC8019", "#FFFFFF"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@500&display=swap');
        .stApp {{ background-color: {bg}; color: {text}; font-family: 'Inter', sans-serif; }}
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {accent}22; }}
        
        /* Metric & Title Styling */
        .stMetric {{ background: {card} !important; border: 1px solid {accent}33 !important; border-radius: 12px; padding: 20px !important; }}
        [data-testid="stMetricValue"] {{ color: {accent} !important; font-size: 1.8rem !important; font-family: 'JetBrains Mono'; }}
        h1, h2, h3, h4 {{ color: {accent}; font-weight: 600; }}
        
        /* The Cocole (Console) */
        .console-box {{ 
            background: #000; color: #00FF41; padding: 15px; border-radius: 8px; 
            font-size: 0.8rem; border: 1px solid #00FF4144; margin-bottom: 30px; 
            font-family: 'JetBrains Mono'; line-height: 1.5;
        }}
        .header-box {{ text-align: center; padding: 15px 0; }}
        
        /* Sidebar Radio/Filter Styling */
        .stRadio label, .stMultiSelect label {{ color: {accent} !important; font-weight: 600; }}
        </style>
    """, unsafe_allow_html=True)
    return "plotly_dark" if "Dark" in theme_choice else "plotly_white"

# --- 3. DATA & LOGO RESOLVER ---
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
    
    # 🧠 MARKET CONTEXT LOGIC (EXTREME RAIN, IPL, NORMAL)
    def define_market(row):
        if row['weather'] == 'Rainy': return 'EXTREME RAIN'
        if 19 <= row['hour'] <= 23: return 'IPL'
        return 'NORMAL'
    
    df['market_context'] = df.apply(define_market, axis=1)
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_and_engineer_data()

# --- 4. SIDEBAR: NAVIGATION, LOGO & FILTERS ---
with st.sidebar:
    # Top Sidebar Logo
    logo_file = resolve_path('Logo.png')
    if os.path.exists(logo_file): 
        st.image(logo_file, use_container_width=True)
    
    st.markdown("### 🎛️ CONTROL CENTER")
    theme_choice = st.selectbox("SYSTEM THEME", ["Swiggy Neural (Dark)", "Swiggy Standard (Light)"])
    plot_template = apply_swiggy_theme(theme_choice)
    
    st.markdown("---")
    module = st.radio("INTELLIGENCE MODULE", 
                    ["GROWTH_VECTORS", "LOGISTICS_SLA", "ECONOMICS_UNIT", "RISK_VECTORS"])
    
    st.markdown("---")
    st.markdown("#### 🔍 SEGMENT FILTERS")
    zone_sel = st.multiselect("LOCATION (ZONE)", df['zone'].unique(), default=df['zone'].unique())
    market_sel = st.multiselect("MARKET SCENARIO", df['market_context'].unique(), default=df['market_context'].unique())
    weather_sel = st.multiselect("WEATHER VECTOR", df['weather'].unique(), default=df['weather'].unique())

# Filtering logic
f_df = df[(df['zone'].isin(zone_sel)) & 
          (df['market_context'].isin(market_sel)) & 
          (df['weather'].isin(weather_sel))]

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
if os.path.exists(logo_file): 
    st.image(logo_file, width=180)
st.markdown('</div>', unsafe_allow_html=True)

# THE COCOLE (CONTROL CONSOLE)
st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] BOOT_STATUS: OPTIMIZED | MODULE: {module}<br>
    [{datetime.now().strftime('%H:%M:%S')}] CONTEXT: {', '.join(market_sel)} | NODES: {len(f_df)}<br>
    [{datetime.now().strftime('%H:%M:%S')}] RISK_SCAN: PROACTIVE | THEME: {theme_choice}
</div>
""", unsafe_allow_html=True)

# Chart Helper with Title enforcement
def draw_intel_chart(fig, title_text):
    fig.update_layout(
        title=dict(text=title_text, font=dict(size=16)),
        template=plot_template,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 6. MODULAR PAGES ---
if module == "GROWTH_VECTORS":
    st.markdown("### 🛰️ Revenue Growth Matrix")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.area(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value'), "1. Hourly Revenue Flux")
    with c2: draw_intel_chart(px.pie(f_df, names='zone', values='order_value', hole=0.5), "2. Regional Market Concentration")
    with c3: draw_intel_chart(px.bar(f_df.groupby('market_context')['order_value'].sum().reset_index(), x='market_context', y='order_value', color='market_context'), "3. Market Scenario Alpha")

elif module == "LOGISTICS_SLA":
    st.markdown("### 🧠 Logistics Neural Net")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.box(f_df, x="weather", y="delivery_time_mins", color="weather"), "4. Climatic SLA Variance")
    with c2: draw_intel_chart(px.line(f_df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins'), "5. Circadian Velocity Trend")
    with c3: draw_intel_chart(px.density_heatmap(f_df, x="delivery_time_mins", y="order_value"), "6. Logistic Density Cluster")

elif module == "ECONOMICS_UNIT":
    st.markdown("### 💎 Profitability & Quant")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.scatter(f_df, x="discount", y="contribution_margin", trendline="ols"), "7. Discount Elasticity")
    with c2: draw_intel_chart(px.violin(f_df, y="margin_rate", x="zone", box=True), "8. Zonal Margin Stability")
    with c3: draw_intel_chart(px.scatter(f_df, x="delivery_cost", y="contribution_margin", color="market_context"), "9. Cost-Profit Correlation")

elif module == "RISK_VECTORS":
    st.markdown("### 🚨 Forensic Risk Analysis")
    
    # 🔔 PUSH NOTIFICATION BUTTON
    if st.button("📢 TRIGGER RISK ALERTS", use_container_width=True):
        expiring = f_df[f_df['freshness_hrs_left'] < 5]
        if not expiring.empty:
            st.toast(f"🚨 CRITICAL: {len(expiring)} Perishables expiring within 5 hours!", icon="⚠️")
            time.sleep(0.5)
            st.toast(f"📍 Action: Adjust dynamic pricing for {f_df['zone'].iloc[0]} sector.", icon="💸")
        else:
            st.toast("✅ SCAN COMPLETE: No immediate inventory risks detected.", icon="🛡️")

    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.histogram(f_df, x="delivery_cost"), "10. Delivery Overhead Risk")
    with c2: draw_intel_chart(px.scatter(f_df, x="freshness_hrs_left", y="order_value", color="category"), "11. Perishable Decay Vector")
    with c3: draw_intel_chart(px.scatter_3d(f_df.sample(min(len(f_df), 500)), x='order_value', y='delivery_time_mins', z='margin_rate', color='market_context'), "12. 3D Operational Space")

# --- 7. FOOTER: SYSTEM TELEMETRY ---
st.markdown("---")
f1, f2, f3, f4 = st.columns(4)
f1.metric("SEGMENT GMV", f"₹{f_df['order_value'].sum()/1e5:.1f}L")
f2.metric("MEAN MARGIN", f"{f_df['margin_rate'].mean():.1f}%")
f3.metric("SLA (MEAN)", f"{f_df['delivery_time_mins'].mean():.1f}m")
f4.metric("EXPIRY NODES", len(f_df[f_df['freshness_hrs_left'] < 5]), delta_color="inverse")
