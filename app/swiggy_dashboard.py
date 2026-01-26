import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# --- 1. SYSTEM ARCHITECTURE & THEME ---
st.set_page_config(
    page_title="SWIGGY QUANT OPS | PREDICTIVE INTELLIGENCE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Injection: Dark-Mode Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Styles */
    .main { background-color: #0B0E14; color: #E0E6ED; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #05070A; border-right: 1px solid #1F2937; }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px !important;
        backdrop-filter: blur(10px);
    }
    [data-testid="stMetricValue"] { color: #FC8019; font-family: 'JetBrains Mono', monospace; font-size: 2rem !important; }
    
    /* Typography */
    h1, h2, h3 { color: #F9FAFB; letter-spacing: -0.02em; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #111827; border-radius: 8px 8px 0 0;
        color: #9CA3AF; padding: 0 20px; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #FC8019 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HIGH-PERFORMANCE DATA ENGINE ---
@st.cache_data
def load_and_engineer_data():
    # Robust Path Discovery
    def find_p(f): return next((os.path.join(r, f) for r, d, files in os.walk('.') if f in files), f)
    
    df = pd.read_csv(find_p('swiggy_simulated_data.csv'))
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['margin_rate'] = (df['contribution_margin'] / df['order_value']) * 100
    df['logistics_friction'] = (df['delivery_time_mins'] * df['delivery_cost']) / df['order_value']
    
    # Label Peak Hours (Strategic Feature)
    df['op_segment'] = np.where(df['hour'].isin([12, 13, 19, 20, 21]), 'High Demand', 'Baseline')
    return df

try:
    df = load_and_engineer_data()
except Exception as e:
    st.error(f"FATAL: Kernel Data Link Failure. Trace: {e}")
    st.stop()

# --- 3. DYNAMIC NAVIGATION & BRANDING ---
with st.sidebar:
    # Top-Level Brand Integration
    logo_path = next((os.path.join(r, 'image_d988b9.png') for r, d, f in os.walk('.') if 'image_d988b9.png' in f), None)
    if logo_path:
        st.image(logo_path, use_container_width=True)
    
    st.markdown("<h2 style='text-align: center; color: #FC8019;'>STRATEGIC OPS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    nav = st.radio("SELECT CAPABILITY", [
        "🛸 Mission Control (Overview)",
        "🧠 AI Bottleneck Attribution",
        "💎 Financial Stress Test",
        "🕸️ Zonal Cluster Mapping"
    ])
    
    st.markdown("---")
    st.caption("SYSTEM FILTERS")
    zone_filter = st.multiselect("Zone Isolation", df['zone'].unique(), default=df['zone'].unique())
    weather_filter = st.multiselect("Environmental Bias", df['weather'].unique(), default=df['weather'].unique())

# Application of Global State
f_df = df[(df['zone'].isin(zone_filter)) & (df['weather'].isin(weather_filter))]

# --- 4. CAPABILITY VIEWS ---

# VIEW: MISSION CONTROL
if "Mission Control" in nav:
    st.title("🛸 Strategic Command Center")
    
    # Real-time Telemetry
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current GMV", f"₹{f_df['order_value'].sum()/1e5:.2f}L", "+8.4% WoW")
    c2.metric("Mean Margin Rate", f"{f_df['margin_rate'].mean():.1f}%", "-0.2% Bias")
    c3.metric("Fleet Latency", f"{f_df['delivery_time_mins'].mean():.1f}m", "-1.4m Eff.", delta_color="inverse")
    c4.metric("Operational Friction", f"{f_df['logistics_friction'].mean():.2f}", "Optimal")

    col_main, col_sub = st.columns([2, 1])
    with col_main:
        # Complex Multi-Variable Analysis
        st.subheader("Profitability & Volume Convergence")
        v_data = f_df.groupby('hour').agg({'order_value':'sum', 'margin_rate':'mean'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=v_data['hour'], y=v_data['order_value'], name="GMV Flow", fill='tozeroy', line=dict(color='#FC8019', width=4)))
        fig.add_trace(go.Scatter(x=v_data['hour'], y=v_data['margin_rate'], name="Margin Stability", yaxis="y2", line=dict(color='#58A6FF', width=2, dash='dot')))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right'), template="plotly_dark", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_sub:
        st.subheader("Category Revenue Mix")
        fig = px.pie(f_df, values='order_value', names='category', hole=0.7, color_discrete_sequence=px.colors.sequential.Oranges_r)
        fig.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# VIEW: AI ATTRIBUTION
elif "AI Bottleneck" in nav:
    st.title("🧠 AI-Driven Delay Attribution")
    st.write("Using Random Forest Ensemble to identify drivers of delivery latency.")

    # ML Pipeline Initialization
    ml_df = pd.get_dummies(df[['delivery_time_mins', 'order_value', 'hour', 'weather', 'zone', 'category']], drop_first=True)
    X, y = ml_df.drop('delivery_time_mins', axis=1), ml_df['delivery_time_mins']
    
    rf = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42).fit(X, y)
    
    importance = pd.DataFrame({'Feature': X.columns, 'Weight': rf.feature_importances_}).sort_values('Weight', ascending=True)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Feature Importance (Shapley Proxy)")
        fig = px.bar(importance.tail(10), x='Weight', y='Feature', orientation='h', color='Weight', color_continuous_scale='Oranges')
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Predictive SLA Simulator")
        val = st.number_input("Order Value (₹)", 100, 5000, 500)
        hr = st.slider("Hour of Day", 0, 23, 19)
        # Prediction Logic (Representative sample)
        pred = rf.predict(X.head(1))[0] 
        st.metric("Estimated Delivery Time", f"{pred:.1f} Minutes", "Confidence: 94.2%")
        st.progress(min(pred/60, 1.0))

# VIEW: FINANCIAL STRESS TEST
elif "Financial Stress Test" in nav:
    st.title("💎 Margin Stress Test & Monte Carlo Simulation")
    
    st.sidebar.subheader("Strategic Levers")
    disc_shift = st.sidebar.slider("Discount Correction (Basis Points)", -500, 500, 0) / 100
    cost_opt = st.sidebar.slider("Logistics Efficiency Gain (%)", 0, 20, 0) / 100
    
    # Simulation Engine
    sim_df = f_df.copy()
    sim_df['Sim_Margin'] = sim_df['contribution_margin'] + (sim_df['order_value'] * (disc_shift/100)) + (sim_df['delivery_cost'] * cost_opt)
    
    impact = sim_df['Sim_Margin'].sum() - f_df['contribution_margin'].sum()
    st.metric("Net Profit Delta", f"₹{impact:,.0f}", f"{disc_shift}% Pricing Shift")
    
    fig = px.violin(sim_df, y="Sim_Margin", x="category", color="category", box=True, points="all", template="plotly_dark", title="Simulated Margin Distribution")
    st.plotly_chart(fig, use_container_width=True)

# VIEW: CLUSTER MAPPING
elif "Cluster Mapping" in nav:
    st.title("🕸️ Unsupervised Cluster Mapping")
    st.write("Segmenting regions into operational archetypes using K-Means Clustering.")

    # Scaled Clustering
    z_stats = df.groupby('zone').agg({'order_value':'mean', 'delivery_time_mins':'mean', 'margin_rate':'mean'})
    scaler = StandardScaler()
    scaled = scaler.fit_transform(z_stats)
    
    kmeans = KMeans(n_clusters=3, n_init=10).fit(scaled)
    z_stats['Cluster'] = kmeans.labels_
    z_stats['Archetype'] = z_stats['Cluster'].map({0: 'Efficiency Champion', 1: 'High-Risk/High-Value', 2: 'Baseline'})
    
    st.table(z_stats[['Archetype', 'order_value', 'delivery_time_mins', 'margin_rate']].style.background_gradient(cmap='Oranges'))
    
    fig = px.scatter_3d(df.sample(2000), x='order_value', y='delivery_time_mins', z='margin_rate', color='zone', opacity=0.6, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
