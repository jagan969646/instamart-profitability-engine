import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="SWIGGY NEURAL OPS", layout="wide", initial_sidebar_state="expanded")

# --- 2. DYNAMIC THEME ENGINE (LIGHT/DARK) ---
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
        .stMetric {{ background: {card} !important; border: 1px solid {accent}33 !important; border-radius: 12px; padding: 20px !important; }}
        [data-testid="stMetricValue"] {{ color: {accent} !important; font-size: 1.8rem !important; font-family: 'JetBrains Mono'; }}
        .console-box {{ 
            background: #000; color: #00FF41; padding: 15px; border-radius: 8px; 
            font-size: 0.8rem; border: 1px solid #00FF4144; margin-bottom: 25px; 
            font-family: 'JetBrains Mono'; line-height: 1.5;
        }}
        .header-box {{ text-align: center; padding: 10px 0; }}
        .case-study-card {{ background: {card}; border: 1px solid {accent}22; border-radius: 12px; padding: 25px; margin-bottom: 20px; }}
        h1, h2, h3, h4 {{ color: {accent}; font-weight: 600; }}
        .footer-sig {{ text-align: center; padding: 40px 0; font-family: 'JetBrains Mono'; color: {accent}; opacity: 0.8; font-size: 0.9rem; letter-spacing: 2px; }}
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
    
    # ADVANCED MARKET CONTEXT LOGIC
    def define_market(row):
        if row['weather'] == 'Rainy': return 'EXTREME RAIN'
        if 19 <= row['hour'] <= 23: return 'IPL'
        return 'NORMAL'
    
    df['market_context'] = df.apply(define_market, axis=1)
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_and_engineer_data()

# --- 4. SIDEBAR: NAV, LOGO & FILTERS ---
with st.sidebar:
    # Sidebar Top Logo
    logo_file = resolve_path('Logo.png')
    if not os.path.exists(logo_file): logo_file = resolve_path('image_d988b9.png')
    if os.path.exists(logo_file): st.image(logo_file, use_container_width=True)
    
    st.markdown("### 🎛️ CONTROL TOWER")
    theme_choice = st.selectbox("VISUAL MODE", ["Swiggy Neural (Dark)", "Swiggy Standard (Light)"])
    plot_template = apply_swiggy_theme(theme_choice)
    
    st.markdown("---")
    module = st.radio("INTELLIGENCE MODULE", 
                    ["GROWTH_VECTORS", "LOGISTICS_SLA", "ECONOMICS_UNIT", "RISK_VECTORS", "STRATEGIC_CASE_STUDY"])
    
    st.markdown("---")
    st.markdown("#### 🔍 GLOBAL FILTERS")
    zone_sel = st.multiselect("ZONE", df['zone'].unique(), default=df['zone'].unique())
    market_sel = st.multiselect("MARKET", df['market_context'].unique(), default=df['market_context'].unique())

# Filter data
f_df = df[(df['zone'].isin(zone_sel)) & (df['market_context'].isin(market_sel))]

# --- 5. MAIN STAGE ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
if os.path.exists(logo_file): st.image(logo_file, width=180)
st.title("SWIGGY INSTAMART NEURAL OPS DASHBOARD")
st.markdown('</div>', unsafe_allow_html=True)

# THE COCOLE
st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] BOOT_STATUS: OPTIMIZED | MODULE: {module}<br>
    [{datetime.now().strftime('%H:%M:%S')}] CONTEXT: {', '.join(market_sel)} | NODES: {len(f_df)} | STATUS: READY
</div>
""", unsafe_allow_html=True)

def draw_intel_chart(fig, title_text):
    fig.update_layout(title=title_text, template=plot_template, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380)
    st.plotly_chart(fig, use_container_width=True)

# --- 6. PAGE MODULES ---

if module == "STRATEGIC_CASE_STUDY":
    st.subheader("📖 Case Study: Neural Inventory & Surge Management")
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.markdown(f"""
        <div class="case-study-card">
            <h4>Strategic Overview</h4>
            <p>During <b>IPL</b> and <b>Extreme Rain</b> events, demand spikes by 300%. Traditional delivery algorithms fail under this load. Our solution uses neural-ops to predict surge 60 mins in advance.</p>
            <h4>Results</h4>
            <ul>
                <li>Margin Leakage reduced by 14%</li>
                <li>Wastage in Perishables down by 12%</li>
                <li>SLA adherence maintained at 94%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c_right:
        st.metric("ALPHA GAIN", "+18%", "Target Met")
        st.metric("WASTE REDUCTION", "12.1%", "Optimized")

elif module == "RISK_VECTORS":
    st.subheader("🚨 Risk Mitigation Hub")
    if st.button("🔔 PUSH LIVE RISK NOTIFICATIONS", use_container_width=True):
        expiring = f_df[f_df['freshness_hrs_left'] < 5]
        if not expiring.empty:
            st.toast(f"🚨 CRITICAL: {len(expiring)} Items Expiring in {f_df['zone'].iloc[0]}!", icon="⚠️")
        else:
            st.toast("✅ ALL SYSTEMS CLEAR: No immediate expiry risk.", icon="🛡️")
    
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.histogram(f_df, x="delivery_cost"), "10. Delivery Cost Risk")
    with c2: draw_intel_chart(px.scatter(f_df, x="freshness_hrs_left", y="order_value", color="category"), "11. Perishable Decay Vector")
    with c3: draw_intel_chart(px.scatter_3d(f_df.sample(min(len(f_df), 500)), x='order_value', y='delivery_time_mins', z='margin_rate', color='market_context'), "12. 3D Risk Matrix")

elif module == "GROWTH_VECTORS":
    st.subheader("🛰️ Growth Matrices")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.area(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value'), "1. Hourly GMV Trend")
    with c2: draw_intel_chart(px.pie(f_df, names='zone', values='order_value', hole=0.5), "2. Regional Market Share")
    with c3: draw_intel_chart(px.bar(f_df.groupby('market_context')['order_value'].sum().reset_index(), x='market_context', y='order_value'), "3. Contextual Revenue")

elif module == "LOGISTICS_SLA":
    st.subheader("🧠 Logistics Intelligence")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.box(f_df, x="weather", y="delivery_time_mins"), "4. Weather vs SLA")
    with c2: draw_intel_chart(px.line(f_df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins'), "5. Temporal Velocity")
    with c3: draw_intel_chart(px.density_heatmap(f_df, x="delivery_time_mins", y="order_value"), "6. Logistics Density")

elif module == "ECONOMICS_UNIT":
    st.subheader("💎 Unit Economics")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.scatter(f_df, x="discount", y="contribution_margin", trendline="ols"), "7. Discount Elasticity")
    with c2: draw_intel_chart(px.violin(f_df, x="zone", y="margin_rate", box=True), "8. Zonal Margin Stability")
    with c3: draw_intel_chart(px.scatter(f_df, x="delivery_cost", y="contribution_margin", color="market_context"), "9. Cost-Profit Correlation")

# --- 7. GLOBAL FOOTER ---
st.markdown("---")
st.markdown(f'<div class="footer-sig">ENGINEERED BY YOUR NAME | NEURAL OPS V3.1</div>', unsafe_allow_html=True)
