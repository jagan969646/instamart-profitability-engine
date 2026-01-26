import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime

# --- 1. SYSTEM CONFIGURATION ---
# Swiggy Orange Heart Favicon "🧡"
st.set_page_config(
    page_title="SWIGGY NEURAL OPS", 
    page_icon="🧡", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. DYNAMIC THEME ENGINE (HIGH CONTRAST) ---
def apply_swiggy_theme(theme_choice):
    if theme_choice == "Swiggy Neural (Dark)":
        bg, text, card, accent, sidebar_bg = "#050505", "#8F9BB3", "#111115", "#FC8019", "#0A0A0C"
    else:
        # High Contrast Light Mode for readability
        bg, text, card, accent, sidebar_bg = "#FFFFFF", "#1A1C2E", "#F8F9FA", "#FC8019", "#F0F2F6"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@500&display=swap');
        
        .stApp {{ background-color: {bg}; color: {text}; font-family: 'Inter', sans-serif; }}
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {accent}44; }}
        
        /* Metric Styling */
        div[data-testid="stMetric"] {{ 
            background-color: {card} !important; 
            border: 1px solid {accent}33 !important; 
            border-radius: 12px; padding: 20px !important; 
        }}
        div[data-testid="stMetricValue"] {{ color: {accent} !important; font-family: 'JetBrains Mono'; font-weight: 700; }}
        div[data-testid="stMetricLabel"] {{ color: {text} !important; opacity: 0.8; font-weight: 600; }}

        /* Case Study Cards */
        .case-card {{ 
            background: {card}; 
            border-left: 5px solid {accent}; 
            padding: 25px; border-radius: 0 12px 12px 0; 
            margin-bottom: 20px;
            color: {text};
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        
        .header-box {{ text-align: center; padding: 20px 0; border-bottom: 2px solid {accent}22; margin-bottom: 25px; }}
        h1, h2, h3, h4 {{ color: {accent} !important; font-weight: 600 !important; }}
        
        .console-box {{ 
            background: #000; color: #00FF41; padding: 15px; border-radius: 8px; 
            font-size: 0.8rem; border: 1px solid #00FF4144; margin-bottom: 30px; 
            font-family: 'JetBrains Mono'; line-height: 1.5;
        }}

        .footer-sig {{ 
            text-align: center; padding: 40px 0; font-family: 'JetBrains Mono'; 
            color: {accent}; opacity: 0.9; font-size: 0.9rem; letter-spacing: 2px;
            border-top: 1px solid {accent}22; margin-top: 50px;
        }}
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
    
    # Market Scenarios: Rainy (Extreme), Night (IPL Peak), or Normal
    def define_market(row):
        if row['weather'] == 'Rainy': return 'EXTREME RAIN'
        if 19 <= row['hour'] <= 23: return 'IPL (NIGHT PEAK)'
        return 'NORMAL'
    
    df['market_context'] = df.apply(define_market, axis=1)
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_and_engineer_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    logo_file = resolve_path('Logo.png')
    if not os.path.exists(logo_file): logo_file = resolve_path('image_d988b9.png')
    if os.path.exists(logo_file): st.image(logo_file, use_container_width=True)
    
    st.markdown("### 🎛️ CONTROL TOWER")
    theme_choice = st.selectbox("VISUAL MODE", ["Swiggy Standard (Light)", "Swiggy Neural (Dark)"])
    plot_template = apply_swiggy_theme(theme_choice)
    
    st.markdown("---")
    module = st.radio("INTELLIGENCE MODULE", 
                    ["STRATEGIC_CASE_STUDY", "ECONOMICS_UNIT", "LOGISTICS_SLA", "RISK_VECTORS"])
    
    st.markdown("---")
    st.markdown("#### 🔍 GLOBAL FILTERS")
    zone_sel = st.multiselect("ZONE", df['zone'].unique(), default=df['zone'].unique())
    market_sel = st.multiselect("MARKET", df['market_context'].unique(), default=df['market_context'].unique())

# Filter data for charts
f_df = df[(df['zone'].isin(zone_sel)) & (df['market_context'].isin(market_sel))]

# --- 5. MAIN STAGE ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
if os.path.exists(logo_file): st.image(logo_file, width=150)
st.title("SWIGGY INSTAMART NEURAL OPS")
st.markdown('</div>', unsafe_allow_html=True)

# System Console Output
st.markdown(f"""
<div class="console-box">
    [{datetime.now().strftime('%H:%M:%S')}] BOOT_STATUS: OPTIMIZED | MODULE: {module}<br>
    [{datetime.now().strftime('%H:%M:%S')}] NODES: {len(f_df)} | CONTEXT: {', '.join(market_sel)}
</div>
""", unsafe_allow_html=True)

def draw_intel_chart(fig, title_text):
    fig.update_layout(title=title_text, template=plot_template, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- 6. PAGE MODULES ---

if module == "STRATEGIC_CASE_STUDY":
    st.subheader("📖 Case Study: Improving Instamart Profitability")
    st.markdown("By: **Jagadeesh N** | BBA, SRM IST (2026) | Aspiring Business Analyst [cite: 2]")
    
    cl, cr = st.columns([2, 1])
    with cl:
        st.markdown(f"""
        <div class="case-card">
            <h4>1. Problem Statement</h4>
            <p>Quick-commerce businesses operate on thin margins due to high last-mile costs and dark store overheads[cite: 5]. 
            Achieving <b>Contribution Margin (CM2) positivity</b> is the industry's primary challenge[cite: 6].</p>
        </div>
        <div class="case-card">
            <h4>2. Key Strategic Insights</h4>
            <ul>
                <li><b>AOV Lever:</b> A ₹50-₹70 increase in AOV (via cross-selling) has a significantly higher impact on profitability than volume growth.</li>
                <li><b>Cost Efficiency:</b> Reducing delivery costs via batching is 2x more sustainable for retention than increasing fees[cite: 14].</li>
                <li><b>The Scale Paradox:</b> High volume without a healthy contribution margin accelerates "burn"[cite: 15].</li>
            </ul>
        </div>
        <div class="case-card">
            <h4>3. Recommendations</h4>
            <p>Incentivize high-AOV baskets with tiered delivery pricing and prioritize <b>Demand Clustering</b> during peak hours like IPL nights[cite: 18, 19].</p>
        </div>
        """, unsafe_allow_html=True)
    with cr:
        st.metric("CURRENT MARGIN", f"{f_df['margin_rate'].mean():.1f}%")
        st.metric("TARGET CM2", "POSITIVE [cite: 6]")
        st.metric("AOV GOAL", "₹500+ [cite: 18]")

elif module == "ECONOMICS_UNIT":
    st.subheader("💎 Unit Economics Analysis")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.scatter(f_df, x="discount", y="contribution_margin", trendline="ols"), "Discount Elasticity")
    with c2: draw_intel_chart(px.violin(f_df, x="zone", y="margin_rate", box=True), "Margin Depth by Zone")
    with c3: draw_intel_chart(px.scatter(f_df, x="delivery_cost", y="contribution_margin", color="market_context"), "Cost-Profit Correlation")

elif module == "LOGISTICS_SLA":
    st.subheader("🧠 Logistics Intelligence")
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.box(f_df, x="weather", y="delivery_time_mins"), "Weather impact on SLA")
    with c2: draw_intel_chart(px.line(f_df.groupby('hour')['delivery_time_mins'].mean().reset_index(), x='hour', y='delivery_time_mins'), "Temporal SLA Velocity")
    with c3: draw_intel_chart(px.histogram(f_df, x="delivery_time_mins", color="market_context"), "SLA Density Distribution")

elif module == "RISK_VECTORS":
    st.subheader("🚨 Operational Risk Vectors")
    if st.button("🔔 PUSH LIVE RISK ALERTS", use_container_width=True):
        st.toast("🚨 ALERT: Perishable decay detected in South Sector! Triggering dynamic discounts.", icon="⚠️")
    
    c1, c2, c3 = st.columns(3)
    with c1: draw_intel_chart(px.histogram(f_df, x="delivery_cost"), "Last-Mile Overhead Risk")
    with c2: draw_intel_chart(px.scatter(f_df, x="freshness_hrs_left", y="order_value", color="category"), "Inventory Decay Vector")
    with c3: draw_intel_chart(px.scatter_3d(f_df.sample(min(len(f_df), 400)), x='order_value', y='delivery_time_mins', z='margin_rate', color='market_context'), "3D Operational Matrix")

# --- 7. FOOTER ---
st.markdown(f'<div class="footer-sig">DESIGNED BY JAGADEESH N | NEURAL OPS V4.0</div>', unsafe_allow_html=True)

