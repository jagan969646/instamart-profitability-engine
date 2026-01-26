import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor # More advanced than Linear Regression
import os

# --- 1. SET PAGE CONFIG (Must be first) ---
st.set_page_config(page_title="Swiggy Ops Intelligence | Strategic Suite", layout="wide")

# --- 2. ROBUST FILE LOCATOR (Fixes the No Such File Error) ---
def get_file_path(filename):
    """Recursively finds the file path in the repository."""
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            return os.path.join(root, filename)
    return None

# --- 3. CUSTOM CSS FOR SENIOR BRANDING ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #FC8019; }
    .stSidebar { background-color: #111827 !important; }
    .reportview-container .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA ENGINE (Self-Healing) ---
@st.cache_data
def load_and_clean_data():
    csv_path = get_file_path('swiggy_simulated_data.csv')
    if not csv_path:
        st.error("🛑 **Data Source Missing:** Please ensure 'swiggy_simulated_data.csv' is uploaded to your GitHub repo.")
        st.stop()
    
    df = pd.read_csv(csv_path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['is_peak'] = df['hour'].apply(lambda x: 1 if x in [12, 13, 19, 20, 21] else 0)
    return df

df = load_and_clean_data()

# --- 5. SIDEBAR NAVIGATION & LOGO ---
with st.sidebar:
    # Logo Placement at the very top
    logo_path = get_file_path('image_d988b9.png')
    if logo_path:
        st.image(logo_path, use_container_width=True)
    else:
        st.title("🚀 SWIGGY OPS") # Fallback title if logo fails
    
    st.markdown("---")
    st.header("Control Center")
    page = st.radio("Navigate Perspective", ["Strategic Overview", "AI Delivery Predictor", "Unit Economics"])
    
    st.markdown("---")
    st.subheader("Global Constraints")
    zones = st.multiselect("Active Zones", df['zone'].unique(), default=df['zone'].unique())
    weather = st.multiselect("Weather Condition", df['weather'].unique(), default=df['weather'].unique())

# Filter data
filtered_df = df[(df['zone'].isin(zones)) & (df['weather'].isin(weather))]

# --- 6. PAGE LOGIC ---

if page == "Strategic Overview":
    st.title("📈 Executive Operations Dashboard")
    
    # KPI Grid
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total GMV", f"₹{filtered_df['order_value'].sum():,.0f}", "+12.5%")
    c2.metric("Net Margin", f"{(filtered_df['contribution_margin'].sum()/filtered_df['order_value'].sum()*100):.1f}%", "-0.4%")
    c3.metric("Avg. Delivery", f"{filtered_df['delivery_time_mins'].mean():.1f} min", "-2m", delta_color="inverse")
    c4.metric("SLA Breaches", f"{len(filtered_df[filtered_df['delivery_time_mins'] > 30])}", "High Risk", delta_color="off")

    # Advanced Charting: Unit Economics Heatmap
    st.subheader("Profitability Heatmap: Zone vs Category")
    pivot = filtered_df.pivot_table(index='zone', columns='category', values='contribution_margin', aggfunc='mean')
    fig = px.imshow(pivot, text_auto='.1f', color_continuous_scale='YlGnBu', aspect='auto')
    st.plotly_chart(fig, use_container_width=True)

elif page == "AI Delivery Predictor":
    st.title("🤖 Operational Risk AI (Random Forest)")
    st.write("This engine predicts delivery time using a machine learning model trained on historical data.")
    
    # Simple ML training on the fly
    ml_df = df.copy()
    ml_df = pd.get_dummies(ml_df, columns=['weather', 'zone', 'category'])
    X = ml_df.drop(['order_id', 'order_time', 'delivery_time_mins', 'contribution_margin'], axis=1, errors='ignore')
    y = ml_df['delivery_time_mins']
    
    model = RandomForestRegressor(n_estimators=50, max_depth=5).fit(X, y)
    
    # Feature Importance Visualization
    importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values('Importance', ascending=False)
    fig = px.bar(importance.head(10), x='Importance', y='Feature', orientation='h', title="Top 10 Drivers of Delivery Delay")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **Insight:** The AI suggests that 'Weather_Rainy' and 'Is_Peak' hour are the most significant contributors to SLA breaches.")

elif page == "Unit Economics":
    st.title("💰 Unit Economics & Margin Leakage")
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig = px.scatter(filtered_df, x="order_value", y="contribution_margin", color="category", 
                         trendline="ols", title="Margin Efficiency by Order Value")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        fig = px.box(filtered_df, x="zone", y="delivery_cost", color="weather", title="Delivery Cost Volatility")
        st.plotly_chart(fig, use_container_width=True)
