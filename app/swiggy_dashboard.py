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
st.set_page_config(page_title="SWIGGY NEURAL OPS", layout="wide", initial_sidebar_state="collapsed")

# --- ADVANCED GLASSMORPHISM & CENTERED UI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .main { background-color: #05070A; color: #E0E6ED; font-family: 'Inter', sans-serif; }
    
    /* Centered Header & Logo */
    .header-container { text-align: center; padding: 2rem 0; }
    .logo-img { width: 180px; filter: drop-shadow(0 0 10px #FC8019); }
    
    /* Capability Cards */
    .stButton>button {
        width: 100%;
        height: 150px;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        border-color: #FC8019 !important;
        background: rgba(252, 128, 25, 0.1) !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    
    /* Metric Styling */
    [data-testid="stMetric"] {
        background: #0D1117;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: QUANTITATIVE DATA DISCOVERY ---
@st.cache_data
def get_system_data():
    csv_name = 'swiggy_simulated_data.csv'
    path = next((os.path.join(r, csv_name) for r, d, f in os.walk('.') if csv_name in f), csv_name)
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    return df

df = get_system_data()

# --- INITIALIZE STATE ---
if 'view' not in st.session_state:
    st.session_state.view = 'Home'

# --- TOP NAVIGATION BAR (LOGO ONLY) ---
logo_name = 'image_d988b9.png'
logo_path = next((os.path.join(r, logo_name) for r, d, f in os.walk('.') if logo_name in f), None)

st.markdown('<div class="header-container">', unsafe_allow_html=True)
if logo_path:
    st.image(logo_path, width=200)
else:
    st.title("SWIGGY QUANT")
st.markdown('</div>', unsafe_allow_html=True)

# --- HOME VIEW: THE COMMAND PORTAL ---
if st.session_state.view == 'Home':
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>CORE CAPABILITY SELECTOR</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛸 MISSION CONTROL\n(Real-time Telemetry)"):
            st.session_state.view = 'Mission Control'
            st.rerun()
        if st.button("🧠 AI BOTTLENECK\n(Neural Attribution)"):
            st.session_state.view = 'AI Attribution'
            st.rerun()
            
    with col2:
        if st.button("💎 FINANCIAL STRESS TEST\n(Monte Carlo Engine)"):
            st.session_state.view = 'Financial Stress'
            st.rerun()
        if st.button("🕸️ ZONAL CLUSTER MAPPING\n(Unsupervised Learning)"):
            st.session_state.view = 'Cluster Mapping'
            st.rerun()

# --- SUB-PAGE: MISSION CONTROL ---
elif st.session_state.view == 'Mission Control':
    if st.button("← Return to Portal"):
        st.session_state.view = 'Home'
        st.rerun()
        
    st.title("🛸 Global Operations Telemetry")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("System GMV", f"₹{df['order_value'].sum()/1e5:.2f}L", "+12.4%")
    m2.metric("Mean Margin", f"{df['margin_rate'].mean():.1f}%", "-0.5%")
    m3.metric("Fleet Velocity", f"{df['delivery_time_mins'].mean():.1f}m", "Optimal")
    m4.metric("Risk Threshold", "0.14 Eta", "Stable")

    fig = px.area(df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value', 
                  title="High-Frequency Volume Distribution", template="plotly_dark", color_discrete_sequence=['#FC8019'])
    st.plotly_chart(fig, use_container_width=True)

# --- SUB-PAGE: AI ATTRIBUTION ---
elif st.session_state.view == 'AI Attribution':
    if st.button("← Return to Portal"):
        st.session_state.view = 'Home'
        st.rerun()
        
    st.title("🧠 Neural Attribution: Delivery Latency Drivers")
    
    # ML Component
    ml_df = pd.get_dummies(df[['delivery_time_mins', 'order_value', 'hour', 'weather']], drop_first=True)
    X, y = ml_df.drop('delivery_time_mins', axis=1), ml_df['delivery_time_mins']
    rf = RandomForestRegressor(n_estimators=50).fit(X, y)
    
    imp = pd.DataFrame({'Factor': X.columns, 'Weight': rf.feature_importances_}).sort_values('Weight')
    fig = px.bar(imp, x='Weight', y='Factor', orientation='h', title="Random Forest Feature Importance", 
                 template="plotly_dark", color_discrete_sequence=['#FC8019'])
    st.plotly_chart(fig, use_container_width=True)

# --- SUB-PAGE: FINANCIAL STRESS TEST ---
elif st.session_state.view == 'Financial Stress':
    if st.button("← Return to Portal"):
        st.session_state.view = 'Home'
        st.rerun()
        
    st.title("💎 Margin-at-Risk Simulator")
    sensitivity = st.select_slider("Select Strategy Shift (Basis Points)", options=[-200, -100, 0, 100, 200])
    
    df['Sim_Margin'] = df['contribution_margin'] + (df['order_value'] * (sensitivity/10000))
    impact = df['Sim_Margin'].sum() - df['contribution_margin'].sum()
    
    st.metric("Projected EBITDA Impact", f"₹{impact:,.0f}", f"{sensitivity} bps shift")
    fig = px.histogram(df, x="Sim_Margin", nbins=50, title="Margin Distribution Stability", 
                       template="plotly_dark", color_discrete_sequence=['#58A6FF'])
    st.plotly_chart(fig, use_container_width=True)

# --- SUB-PAGE: CLUSTER MAPPING ---
elif st.session_state.view == 'Cluster Mapping':
    if st.button("← Return to Portal"):
        st.session_state.view = 'Home'
        st.rerun()
        
    st.title("🕸️ Operational Archetype Clustering")
    
    z_data = df.groupby('zone').agg({'order_value':'mean', 'delivery_time_mins':'mean', 'margin_rate':'mean'})
    kmeans = KMeans(n_clusters=3, n_init=10).fit(StandardScaler().fit_transform(z_data))
    z_data['Cluster'] = kmeans.labels_
    
    st.table(z_data.style.background_gradient(cmap='Oranges'))
    fig = px.scatter_3d(df.sample(1000), x='order_value', y='delivery_time_mins', z='margin_rate', 
                        color='zone', template="plotly_dark", title="Global Operational Vector Space")
    st.plotly_chart(fig, use_container_width=True)
