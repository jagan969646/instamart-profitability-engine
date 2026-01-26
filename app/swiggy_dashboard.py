import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="SWIGGY NEURAL OPS", layout="wide", initial_sidebar_state="expanded")

# --- 2. HIGH-CONTRAST THEME ENGINE ---
def apply_swiggy_theme(theme_choice):
    if theme_choice == "Swiggy Neural (Dark)":
        bg, text, card, accent, sidebar_bg = "#050505", "#8F9BB3", "#111115", "#FC8019", "#0A0A0C"
    else:
        # FIXED LIGHT MODE: High contrast dark text on light background
        bg, text, card, accent, sidebar_bg = "#FFFFFF", "#1A1C2E", "#F8F9FA", "#FC8019", "#F0F2F6"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@500&display=swap');
        .stApp {{ background-color: {bg}; color: {text}; font-family: 'Inter', sans-serif; }}
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {accent}44; }}
        
        /* Metric Styling - Forced High Contrast */
        div[data-testid="stMetric"] {{ 
            background-color: {card} !important; 
            border: 1px solid {accent}44 !important; 
            border-radius: 12px; padding: 15px !important; 
        }}
        div[data-testid="stMetricValue"] {{ color: {accent} !important; font-weight: 700; }}
        div[data-testid="stMetricLabel"] {{ color: {text} !important; opacity: 0.8; }}

        /* Case Study Card */
        .case-card {{ 
            background-color: {card}; 
            border-left: 5px solid {accent}; 
            padding: 20px; border-radius: 8px; 
            color: {text}; margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .header-box {{ text-align: center; padding: 15px 0; border-bottom: 2px solid {accent}22; }}
        h1, h2, h3, h4 {{ color: {accent} !important; }}
        .footer-sig {{ text-align: center; padding: 30px; color: {accent}; font-family: 'JetBrains Mono'; font-size: 0.8rem; border-top: 1px solid {accent}22; }}
        </style>
    """, unsafe_allow_html=True)
    return "plotly_dark" if "Dark" in theme_choice else "plotly_white"

# --- 3. DATA & LOGO RESOLVER ---
def resolve_path(filename):
    for root, dirs, files in os.walk("."):
        if filename in files: return os.path.join(root, filename)
    return filename

@st.cache_data
def load_data():
    path = resolve_path('swiggy_simulated_data.csv')
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    logo_file = resolve_path('Logo.png')
    if not os.path.exists(logo_file): logo_file = resolve_path('image_d988b9.png')
    if os.path.exists(logo_file): st.image(logo_file, use_container_width=True)
    
    st.markdown("### 🎛️ CONTROL")
    theme_choice = st.selectbox("THEME", ["Swiggy Standard (Light)", "Swiggy Neural (Dark)"])
    plot_template = apply_swiggy_theme(theme_choice)
    
    module = st.radio("NAVIGATE", ["STRATEGIC_CASE_STUDY", "RISK_VECTORS", "GROWTH_VECTORS"])
    zone_sel = st.multiselect("ZONE", df['zone'].unique(), default=df['zone'].unique())

f_df = df[df['zone'].isin(zone_sel)]

# --- 5. HEADER ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
st.title("SWIGGY INSTAMART NEURAL OPS")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PAGE MODULES ---

if module == "STRATEGIC_CASE_STUDY":
    st.subheader("📖 Case Study: Improving Instamart Profitability [cite: 1]")
    st.caption("By: Jagadeesh N | BBA, SRM IST (2026) [cite: 2]")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class="case-card">
            <h4>The Problem Statement</h4>
            <p>Quick-commerce operates on thin margins due to last-mile costs and discount-heavy growth[cite: 5]. 
            Achieving <b>Contribution Margin (CM2) positivity</b> is the primary challenge.</p>
        </div>
        <div class="case-card">
            <h4>Key Strategic Insights</h4>
            <ul>
                <li><b>AOV Lever:</b> Increasing AOV by ₹50-70 via cross-selling is more impactful than volume growth.</li>
                <li><b>Batching Sustainability:</b> Reducing costs via batching is 2x more sustainable than fee hikes[cite: 14].</li>
                <li><b>Scale Paradox:</b> High volume without margin accelerates "burn"[cite: 15].</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.metric("AVG MARGIN RATE", f"{f_df['margin_rate'].mean():.1f}%")
        st.metric("STRATEGIC GOAL", "CM2 POSITIVE [cite: 26]")

elif module == "RISK_VECTORS":
    st.subheader("🚨 Risk Mitigation")
    if st.button("📢 PUSH NOTIFICATION", use_container_width=True):
        st.toast("🚨 ALERT: High perishable decay detected in South Sector!", icon="⚠️")
    
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(f_df, x="delivery_cost", title="Delivery Cost Distribution")
        fig.update_layout(template=plot_template, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(f_df, x="freshness_hrs_left", y="order_value", title="Freshness Decay Vector")
        fig.update_layout(template=plot_template, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

elif module == "GROWTH_VECTORS":
    st.subheader("🛰️ Growth Analysis")
    fig = px.area(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', title="Hourly GMV")
    fig.update_layout(template=plot_template, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# --- 7. FOOTER ---
st.markdown(f'<div class="footer-sig">JAGADEESH N | NEURAL OPS DASHBOARD 2026</div>', unsafe_allow_html=True)
