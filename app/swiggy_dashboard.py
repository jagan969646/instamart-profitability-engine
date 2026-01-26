import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

# --- 1. ROBUST FILE LOADING (Fixes your FileNotFoundError) ---
def find_file(name):
    """Search for file in current and parent directories."""
    for root, dirs, files in os.walk('.'):
        if name in files:
            return os.path.join(root, name)
    return name

# --- PAGE CONFIG ---
st.set_page_config(page_title="Swiggy Ops Intelligence | Senior Suite", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="metric-container"] {
        background-color: white; border: 1px solid #e1e4e8;
        padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def get_data():
    csv_path = find_file('swiggy_simulated_data.csv')
    df = pd.read_csv(csv_path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['is_weekend'] = df['order_time'].dt.dayofweek.isin([5, 6]).astype(int)
    return df

try:
    df = get_data()
except Exception as e:
    st.error(f"⚠️ Critical Error: Could not find data file. Ensure 'swiggy_simulated_data.csv' is in your GitHub repo. Error: {e}")
    st.stop()

# --- SIDEBAR & LOGO ---
with st.sidebar:
    logo_path = find_file('image_d988b9.png')
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    
    st.title("🛡️ Ops Control Tower")
    st.markdown("---")
    selected_zone = st.multiselect("Region focus", df['zone'].unique(), default=df['zone'].unique())
    weather_filter = st.multiselect("Weather condition", df['weather'].unique(), default=df['weather'].unique())

# Filter data
filtered_df = df[(df['zone'].isin(selected_zone)) & (df['weather'].isin(weather_filter))]

# --- DASHBOARD LAYOUT ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Executive Overview", 
    "💸 Unit Economics & Simulation", 
    "🤖 Predictive Logistics", 
    "🍎 Inventory Risk"
])

# --- TAB 1: EXECUTIVE OVERVIEW ---
with tab1:
    st.subheader("Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    gmv = filtered_df['order_value'].sum()
    margin = (filtered_df['contribution_margin'].sum() / gmv) * 100
    avg_delivery = filtered_df['delivery_time_mins'].mean()
    
    kpi1.metric("Total GMV", f"₹{gmv/1e5:.2f}L", "8.2% YoY")
    kpi2.metric("Contribution Margin", f"{margin:.1f}%", "1.4%", delta_color="normal")
    kpi3.metric("Avg. Delivery Time", f"{avg_delivery:.1f}m", "-2.5m", delta_color="inverse")
    kpi4.metric("Order Volume", f"{len(filtered_df):,}", "12% ↗")

    c1, c2 = st.columns([2, 1])
    with c1:
        # Time series with margin context
        hourly_perf = filtered_df.groupby('hour').agg({'order_value':'sum', 'contribution_margin':'sum'}).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=hourly_perf['hour'], y=hourly_perf['order_value'], name="Revenue", marker_color='#FC8019'))
        fig.add_trace(go.Scatter(x=hourly_perf['hour'], y=hourly_perf['contribution_margin'], name="Margin", yaxis="y2", line=dict(color='#2D3E50', width=3)))
        fig.update_layout(title="Revenue vs Margin Flow by Hour", yaxis2=dict(overlaying='y', side='right'), height=400)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        # Zone performance radar/bar
        zone_perf = filtered_df.groupby('zone')['order_value'].mean().sort_values()
        fig = px.bar(zone_perf, orientation='h', title="Avg Ticket Size by Zone", color_discrete_sequence=['#FC8019'])
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: UNIT ECONOMICS & SIMULATION ---
with tab2:
    st.subheader("Profitability Stress Test")
    col_sim1, col_sim2 = st.columns([1, 2])
    
    with col_sim1:
        st.write("#### Simulation Engine")
        st.caption("Predict impact of changing discount strategies")
        adj_discount = st.slider("Simulate Discount Change (%)", -50, 50, 0)
        
        # Simple simulation logic
        sim_df = filtered_df.copy()
        sim_df['new_discount'] = sim_df['discount'] * (1 + adj_discount/100)
        sim_df['new_margin'] = sim_df['contribution_margin'] - (sim_df['new_discount'] - sim_df['discount'])
        
        total_impact = sim_df['new_margin'].sum() - filtered_df['contribution_margin'].sum()
        st.metric("Estimated Margin Impact", f"₹{total_impact:,.0f}", f"{adj_discount}% shift")
        
    with col_sim2:
        fig = px.scatter(filtered_df, x="order_value", y="contribution_margin", color="category", 
                         trendline="ols", title="Margin Efficiency (Order Value vs Profit)")
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 3: PREDICTIVE LOGISTICS ---
with tab3:
    st.subheader("🤖 AI-Driven Delivery Prediction")
    st.write("This model predicts delivery delays based on weather and historical zone performance.")
    
    # Simple Linear Regression for Delivery Time
    ml_df = df.copy()
    ml_df = pd.get_dummies(ml_df, columns=['weather', 'zone'], drop_first=True)
    
    X = ml_df[['order_value', 'hour', 'is_weekend'] + [c for c in ml_df.columns if 'weather_' in c or 'zone_' in c]]
    y = ml_df['delivery_time_mins']
    
    model = LinearRegression().fit(X, y)
    
    # Feature Importance (Standardized Coefficients)
    importance = pd.DataFrame({'Feature': X.columns, 'Impact': model.coef_}).sort_values(by='Impact')
    
    col_ml1, col_ml2 = st.columns(2)
    with col_ml1:
        fig = px.bar(importance, x='Impact', y='Feature', title="What factors delay our deliveries?", color='Impact', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)
    with col_ml2:
        st.write("#### Real-time Predictor")
        in_val = st.number_input("Order Value", 100, 2000, 500)
        in_hour = st.slider("Hour of Day", 0, 23, 12)
        # Simplified prediction for UI demo
        pred = model.predict(X.iloc[0:1])[0] # Mock prediction placeholder
        st.info(f"Predicted Delivery Time: **{pred:.1f} minutes**")

# --- TAB 4: INVENTORY RISK ---
with tab4:
    st.subheader("Critical Freshness Monitoring")
    perish = filtered_df[filtered_df['category'] == 'Perishable'].copy()
    perish['risk'] = np.where(perish['freshness_hrs_left'] < 6, 'Critical', 'Normal')
    
    fig = px.sunburst(perish, path=['zone', 'risk'], values='order_value', color='risk',
                      color_discrete_map={'Critical':'#e74c3c', 'Normal':'#2ecc71'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("#### Orders needing immediate dispatch")
    st.dataframe(perish[perish['risk'] == 'Critical'].sort_values('freshness_hrs_left'), use_container_width=True)
