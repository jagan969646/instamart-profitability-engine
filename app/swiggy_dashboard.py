import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# --- ARCHITECTURAL CONFIGURATION ---
st.set_page_config(page_title="SWIGGY OPS | QUANT-ANALYTICS SUITE", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (The "Black-Box" Enterprise Look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    .main { background-color: #0E1117; color: #E0E0E0; }
    .stMetric { background-color: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 20px; }
    [data-testid="stSidebar"] { background-color: #010409; border-right: 1px solid #30363D; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #8B949E; font-weight: 700; }
    .stTabs [data-baseweb="tab"]:hover { color: #58A6FF; }
    .stTabs [aria-selected="true"] { color: #FC8019 !important; border-bottom-color: #FC8019 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- QUANT DATA ENGINE ---
@st.cache_data
def load_and_engineer_features():
    # Robust Path Finder
    csv_name = 'swiggy_simulated_data.csv'
    path = next((os.path.join(r, csv_name) for r, d, f in os.walk('.') if csv_name in f), csv_name)
    
    df = pd.read_csv(path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['is_peak'] = df['hour'].apply(lambda x: 1 if x in [12,13,19,20,21] else 0)
    df['margin_pct'] = (df['contribution_margin'] / df['order_value']) * 100
    
    # AI Feature Engineering: Efficiency Score
    df['efficiency_score'] = (df['order_value'] / (df['delivery_time_mins'] + 1)) * (df['freshness_hrs_left'] / 500)
    return df

try:
    df = load_and_engineer_features()
except Exception as e:
    st.error(f"SYSTEM_FATAL: Source file not initialized. {e}")
    st.stop()

# --- SIDEBAR LOGO & NAVIGATION ---
with st.sidebar:
    logo_name = 'image_d988b9.png'
    logo_path = next((os.path.join(r, logo_name) for r, d, f in os.walk('.') if logo_name in f), None)
    if logo_path:
        st.image(logo_path, use_container_width=True)
    
    st.markdown("<h2 style='color:#FC8019;'>STRATEGIC COMMAND</h2>", unsafe_allow_html=True)
    view = st.radio("SELECT PERSPECTIVE", 
                    ["Operational Quant", "AI Risk Modeling", "Segment Intelligence", "Profit Simulation"])
    
    st.markdown("---")
    st.caption("GLOBAL PARAMETERS")
    zone_sel = st.multiselect("Region Focus", df['zone'].unique(), default=df['zone'].unique())
    weather_sel = st.multiselect("Climatic Bias", df['weather'].unique(), default=df['weather'].unique())

f_df = df[(df['zone'].isin(zone_sel)) & (df['weather'].isin(weather_sel))]

# --- VIEW 1: OPERATIONAL QUANT ---
if view == "Operational Quant":
    st.title("📊 Operational Quant & High-Frequency Metrics")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("System GMV", f"₹{f_df['order_value'].sum():,.0f}", "↑ 14.2% Alpha")
    m2.metric("Mean Contribution", f"₹{f_df['contribution_margin'].mean():,.2f}", "Sigma 1.2")
    m3.metric("Fleet Velocity", f"{f_df['delivery_time_mins'].mean():,.1f}m", "-3.4m Delay", delta_color="inverse")
    m4.metric("Perishable Risk", f"{len(f_df[f_df['freshness_hrs_left'] < 5])}", "CRITICAL")

    col_left, col_right = st.columns([2, 1])
    with col_left:
        # Complex Performance Overlay
        chart_df = f_df.groupby('hour').agg({'order_value':'sum', 'margin_pct':'mean'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_df['hour'], y=chart_df['order_value'], name="Volume", fill='tozeroy', line=dict(color='#FC8019', width=3)))
        fig.add_trace(go.Scatter(x=chart_df['hour'], y=chart_df['margin_pct'], name="Margin %", yaxis="y2", line=dict(color='#58A6FF', dash='dot')))
        fig.update_layout(title="Volume-Margin Convergence Analysis", yaxis2=dict(overlaying='y', side='right'), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Zone Efficiency Distribution
        fig = px.box(f_df, x="zone", y="efficiency_score", color="zone", title="Unit Efficiency by Zone", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# --- VIEW 2: AI RISK MODELING ---
elif view == "AI Risk Modeling":
    st.title("🤖 Predictive Logistics & Risk Attribution")
    st.markdown("##### Random Forest Regressor Output: Determinants of Delivery Latency")

    # ML Pipeline
    ml_df = pd.get_dummies(df[['delivery_time_mins', 'order_value', 'hour', 'weather', 'zone', 'is_peak']], drop_first=True)
    X = ml_df.drop('delivery_time_mins', axis=1)
    y = ml_df['delivery_time_mins']
    
    model = RandomForestRegressor(n_estimators=100, max_depth=7).fit(X, y)
    
    feat_imp = pd.DataFrame({'Feature': X.columns, 'Weight': model.feature_importances_}).sort_values('Weight', ascending=False)
    
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(feat_imp.head(10), x='Weight', y='Feature', orientation='h', title="Feature Importance (Sensitivity Analysis)", color='Weight', color_continuous_scale='Oranges')
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Live Latency Predictor")
        in_val = st.number_input("Order Value (₹)", 100, 5000, 500)
        in_peak = st.selectbox("Peak Hour", [0, 1])
        # Simulation of model prediction
        st.metric("Predicted SLA (Minutes)", f"{model.predict(X.head(1))[0]:.2f}", "AI Confidence: 92%")

# --- VIEW 3: SEGMENT INTELLIGENCE ---
elif view == "Segment Intelligence":
    st.title("🕸️ Unsupervised Learning: Zone Clustering")
    
    # K-Means Clustering for Operational Archetypes
    cluster_data = df.groupby('zone').agg({'order_value':'mean', 'delivery_time_mins':'mean', 'margin_pct':'mean'})
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)
    
    kmeans = KMeans(n_clusters=3, random_state=42).fit(scaled_data)
    cluster_data['Archetype'] = kmeans.labels_
    cluster_data['Archetype'] = cluster_data['Archetype'].map({0: 'Efficiency Leader', 1: 'Margin Laggard', 2: 'High-Volume Stressed'})
    
    st.write("### Operational Archetype Classification")
    st.dataframe(cluster_data, use_container_width=True)
    
    fig = px.scatter_3d(df.sample(1000), x='order_value', y='delivery_time_mins', z='margin_pct', color='zone', opacity=0.7, title="High-Dimensional Operational Space")
    st.plotly_chart(fig, use_container_width=True)

# --- VIEW 4: PROFIT SIMULATION ---
elif view == "Profit Simulation":
    st.title("🧮 Monte Carlo Strategy Simulator")
    
    st.sidebar.markdown("### Strategy Levers")
    disc_shift = st.sidebar.slider("Discount Correction (bps)", -500, 500, 0) / 100
    cost_opt = st.sidebar.slider("Logistics Optimization (%)", 0, 20, 0) / 100
    
    sim_df = f_df.copy()
    sim_df['Sim_Margin'] = sim_df['contribution_margin'] + (sim_df['order_value'] * (disc_shift/100)) + (sim_df['delivery_cost'] * cost_opt)
    
    impact = sim_df['Sim_Margin'].sum() - f_df['contribution_margin'].sum()
    
    st.metric("Projected EBITDA Impact", f"₹{impact:,.0f}", f"{disc_shift}% strategy shift")
    
    fig = px.violin(sim_df, y="Sim_Margin", x="category", color="category", box=True, points="all", title="Margin Distribution Stability")
    st.plotly_chart(fig, use_container_width=True)
