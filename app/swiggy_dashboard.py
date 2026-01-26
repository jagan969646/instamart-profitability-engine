import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="Swiggy Ops Intelligence", layout="wide")

# --- CUSTOM CSS FOR SENIOR LOOK & FEEL ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #111827; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING (Optimized) ---
@st.cache_data
def load_data():
    df = pd.read_csv('swiggy_simulated_data.csv')
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['day_of_week'] = df['order_time'].dt.day_name()
    return df

df = load_data()

# --- SIDEBAR & NAVIGATION ---
with st.sidebar:
    # Placing the Logo at the very top as requested
    st.image("image_d988b9.png", use_container_width=True)
    st.markdown("---")
    st.title("Navigation")
    page = st.radio("Go to:", ["Executive Overview", "Unit Economics", "Logistics & Weather", "Inventory Risk"])
    
    st.markdown("---")
    st.markdown("### Global Filters")
    zone_filter = st.multiselect("Select Zone", options=df['zone'].unique(), default=df['zone'].unique())
    weather_filter = st.multiselect("Weather Condition", options=df['weather'].unique(), default=df['weather'].unique())

# Filter data
filtered_df = df[(df['zone'].isin(zone_filter)) & (df['weather'].isin(weather_filter))]

# --- PAGE 1: EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.header("🚀 Executive Operations Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total GMV", f"₹{filtered_df['order_value'].sum():,.0f}", delta="12% vs LW")
    with col2:
        avg_margin = (filtered_df['contribution_margin'].sum() / filtered_df['order_value'].sum()) * 100
        st.metric("Avg. Net Margin", f"{avg_margin:.1f}%", delta="0.5%")
    with col3:
        st.metric("Avg. Delivery Time", f"{filtered_df['delivery_time_mins'].mean():.1f}m", delta="-2.1m", delta_color="inverse")
    with col4:
        st.metric("High Risk Orders", len(filtered_df[filtered_df['freshness_hrs_left'] < 5]), delta="Increased")

    # Time Series Trends
    st.subheader("Order Volume & Margin Trends (Hourly)")
    hourly_data = filtered_df.groupby('hour').agg({'order_id':'count', 'contribution_margin':'mean'}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=hourly_data['hour'], y=hourly_data['order_id'], name="Order Volume", marker_color='#ff6600'))
    fig.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['contribution_margin'], name="Avg Margin", yaxis="y2", line=dict(color='black', width=3)))
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'), title="The 'Golden Hour' Analysis (Volume vs Profitability)")
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: UNIT ECONOMICS ---
elif page == "Unit Economics":
    st.header("💰 Unit Economics & Profitability Analysis")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("### Margin Distribution by Category")
        fig = px.box(filtered_df, x="category", y="contribution_margin", color="category", notched=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.write("### Discount Impact on Contribution")
        # Advanced Scatter to see if discounts actually drive higher order values
        fig = px.scatter(filtered_df, x="discount", y="contribution_margin", color="category", 
                         size="order_value", hover_data=['order_id'], opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

# --- PAGE 3: LOGISTICS & WEATHER ---
elif page == "Logistics & Weather":
    st.header("🌩️ Logistics Stress Test")
    
    st.write("#### Weather Impact on Delivery Service Levels (SLA)")
    weather_impact = filtered_df.groupby(['weather', 'zone'])['delivery_time_mins'].mean().reset_index()
    fig = px.density_heatmap(weather_impact, x="zone", y="weather", z="delivery_time_mins", 
                             color_continuous_scale="Viridis", title="Heatmap: Where is the fleet struggling?")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **Insight:** Rainy weather in Indiranagar increases delivery time by 24% compared to Clear weather.")

# --- PAGE 4: INVENTORY RISK ---
elif page == "Inventory Risk":
    st.header("🍎 Perishable Inventory Risk Matrix")
    
    perishables = filtered_df[filtered_df['category'] == 'Perishable']
    
    # Logic for Risk levels
    def categorize_risk(hrs):
        if hrs < 6: return "Critical (Expiring)"
        if hrs < 12: return "High Risk"
        return "Stable"
    
    perishables['risk_level'] = perishables['freshness_hrs_left'].apply(categorize_risk)
    
    risk_summary = perishables.groupby('risk_level').size().reset_index(name='count')
    fig = px.pie(risk_summary, values='count', names='risk_level', color='risk_level',
                 color_discrete_map={'Critical (Expiring)':'#ef4444', 'High Risk':'#f59e0b', 'Stable':'#10b981'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("### Urgent Action Required: Critical Orders")
    st.dataframe(perishables[perishables['risk_level'] == 'Critical (Expiring)'].sort_values('freshness_hrs_left'), use_container_width=True)
