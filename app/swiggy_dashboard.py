import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# --- ARCHITECTURAL CONFIG ---
st.set_page_config(page_title="SWIGGY | NEURAL COMMAND", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS: MINIMALIST ELITE UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050505; color: #999; }
    
    /* Center Logo */
    .logo-container { text-align: center; padding-top: 30px; padding-bottom: 10px; }
    
    /* Minimalist Centered Nav Bar */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-bottom: 50px;
        border-bottom: 1px solid #1a1a1a;
        padding-bottom: 15px;
    }
    
    .nav-item {
        color: #666;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        cursor: pointer;
        transition: 0.3s;
        background: none;
        border: none;
    }
    
    .nav-item:hover { color: #FC8019; }
    .active-nav { color: #FC8019; border-bottom: 2px solid #FC8019; }

    /* Metric Styling */
    [data-testid="stMetricValue"] { color: #eee !important; font-size: 1.8rem !important; font-weight: 300 !important; }
    [data-testid="stMetricLabel"] { color: #666 !important; text-transform: uppercase; letter-spacing: 1px; font-size: 0.7rem !important; }
    
    /* Clean Cards */
    .stPlotlyChart { background-color: transparent !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: DATA ARCHITECTURE ---
@st.cache_data
def load_engine_data():
    path = next((os.path.join(r, 'swiggy_simulated_data.csv') for r, d, f in os.walk('.') if 'swiggy_simulated_data.csv' in f), 'swiggy_simulated_data.csv')
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = load_engine_data()

# --- LOGO & NAV STATE ---
if 'view' not in st.session_state:
    st.session_state.view = 'OVERVIEW'

# Logo
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
logo_path = next((os.path.join(r, 'image_d988b9.png') for r, d, f in os.walk('.') if 'image_d988b9.png' in f), None)
if logo_path:
    st.image(logo_path, width=140)
st.markdown('</div>', unsafe_allow_html=True)

# Centered Navigation
c1, c2, c3, c4, c5 = st.columns([2,1,1,1,2])
with c2: 
    if st.button("OVERVIEW", key="nav_ov", use_container_width=True): st.session_state.view = 'OVERVIEW'
with c3: 
    if st.button("NEURAL", key="nav_ai", use_container_width=True): st.session_state.view = 'NEURAL'
with c4: 
    if st.button("QUANT", key="nav_qu", use_container_width=True): st.session_state.view = 'QUANT'

st.markdown("<br>", unsafe_allow_html=True)

# --- PAGE 1: OVERVIEW ---
if st.session_state.view == 'OVERVIEW':
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("GMV ALPHA", f"₹{df['order_value'].sum()/1e5:.1f}L")
    col2.metric("NET MARGIN", f"{df['margin_rate'].mean():.1f}%")
    col3.metric("VELOCITY", f"{df['delivery_time_mins'].mean():.1f}m")
    col4.metric("SYSTEM RISK", "STABLE")

    fig = px.line(df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', 
                  template="plotly_dark", color_discrete_sequence=['#FC8019'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                      xaxis_visible=False, yaxis_visible=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: NEURAL (AI DRIVERS) ---
elif st.session_state.view == 'NEURAL':
    st.markdown("<h6 style='text-align: center; color: #444;'>LATENCY ATTRIBUTION MODEL (RANDOM FOREST)</h6>", unsafe_allow_html=True)
    
    ml_df = pd.get_dummies(df[['delivery_time_mins', 'order_value', 'hour', 'weather']], drop_first=True)
    X, y = ml_df.drop('delivery_time_mins', axis=1), ml_df['delivery_time_mins']
    rf = RandomForestRegressor(n_estimators=30).fit(X, y)
    
    imp = pd.DataFrame({'Feature': X.columns, 'Weight': rf.feature_importances_}).sort_values('Weight')
    fig = px.bar(imp, x='Weight', y='Feature', orientation='h', template="plotly_dark", color_discrete_sequence=['#FC8019'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 3: QUANT (STRATEGY) ---
elif st.session_state.view == 'QUANT':
    st.markdown("<h6 style='text-align: center; color: #444;'>MARGIN SENSITIVITY ANALYSIS</h6>", unsafe_allow_html=True)
    
    shift = st.select_slider("ADJUST BASIS POINTS", options=[-100, -50, 0, 50, 100])
    impact = (df['order_value'].sum() * (shift/10000))
    
    st.metric("EBITDA DELTA", f"₹{impact:,.0f}", f"{shift} BPS")
    
    fig = px.box(df, x="category", y="margin_rate", template="plotly_dark", color_discrete_sequence=['#FC8019'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
