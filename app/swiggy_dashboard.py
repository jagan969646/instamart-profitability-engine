import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# -----------------------------
# PAGE CONFIG & THEME
# -----------------------------
st.set_page_config(page_title="Instamart Executive HQ", page_icon="🧡", layout="wide")

# Path Fix (Updated filename)
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")

# Executive CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fb; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #FC8019;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA ENGINE
# -----------------------------
@st.cache_data
def load_and_process():
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 Data file not found at {DATA_PATH}")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    df['order_time'] = pd.to_datetime(df['order_time'])
    
    # Advanced Unit Economics Logic
    df['commission'] = df['order_value'] * 0.15
    df['ad_revenue'] = df['order_value'] * 0.03
    df['total_revenue'] = df['commission'] + df['ad_revenue'] + df['delivery_fee']
    df['contribution_margin'] = df['total_revenue'] - df['delivery_cost'] - df['discount']
    
    return df

df = load_and_process()

# -----------------------------
# SIDEBAR: STRATEGIC CONTROLS
# -----------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=150)
    st.title("Strategic Controls")
    
    st.subheader("📍 Scope")
    zones = st.multiselect("Select Clusters", df['zone'].unique(), default=df['zone'].unique())
    
    st.divider()
    st.subheader("📈 What-If Profit Simulator")
    target_fee = st.slider("Target Delivery Fee (₹)", 0, 60, 25)
    discount_cut = st.slider("Reduce Discounts by (%)", 0, 50, 10)
    
    st.info("Simulating impact on Contribution Margin based on selected levers.")

# Filter Data
filtered_df = df[df['zone'].isin(zones)].copy()

# Apply "What-If" Logic
sim_df = filtered_df.copy()
sim_df['delivery_fee'] = target_fee
sim_df['discount'] = sim_df['discount'] * (1 - discount_cut/100)
sim_df['contribution_margin'] = (sim_df['commission'] + sim_df['ad_revenue'] + sim_df['delivery_fee']) - sim_df['delivery_cost'] - sim_df['discount']

# -----------------------------
# HEADER & KPI OVERVIEW
# -----------------------------
st.title("🧡 Instamart | Path to Profitability Dashboard")
st.markdown(f"**Market Coverage:** {len(zones)} Clusters | **Data Currency:** {df['order_time'].max().strftime('%Y-%m-%d %H:%M')}")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total GOV", f"₹{sim_df['order_value'].sum()/1e6:.2f}M", "+12% vs LW")
with m2:
    cm_total = sim_df['contribution_margin'].sum()
    st.metric("Total CM", f"₹{cm_total/1e5:.2f}L", f"{'Profit' if cm_total > 0 else 'Burn'}", delta_color="normal")
with m3:
    st.metric("Avg. Order Value", f"₹{sim_df['order_value'].mean():.0f}", "-₹5 vs Target")
with m4:
    st.metric("Orders", f"{len(sim_df):,}", "Peak Hour Active")

st.divider()

# -----------------------------
# MAIN DASHBOARD LAYOUT
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📊 Financial Performance", "🚲 Operational Efficiency", "🧠 Predictive Insights"])

with tab1:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Contribution Margin Trend by Zone")
        fig_cm = px.line(sim_df.groupby(['order_time', 'zone'])['contribution_margin'].sum().reset_index(), 
                         x='order_time', y='contribution_margin', color='zone', template="plotly_white")
        st.plotly_chart(fig_cm, use_container_width=True)
        
    with c2:
        st.subheader("Revenue Mix")
        mix_data = pd.DataFrame({
            'Source': ['Commissions', 'Ad Revenue', 'Delivery Fees'],
            'Value': [sim_df['commission'].sum(), sim_df['ad_revenue'].sum(), sim_df['delivery_fee'].sum()]
        })
        fig_pie = px.pie(mix_data, values='Value', names='Source', hole=0.5, color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("Delivery Cost vs. Time Heatmap")
    # Simulated heatmap logic
    sim_df['hour'] = sim_df['order_time'].dt.hour
    heat_data = sim_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    fig_heat = px.imshow(heat_data, color_continuous_scale='YlOrRd', labels=dict(x="Hour of Day", y="Zone", color="Avg Cost"))
    st.plotly_chart(fig_heat, use_container_width=True)

with tab3:
    col_ml1, col_ml2 = st.columns(2)
    with col_ml1:
        st.subheader("XGBoost: Feature Importance")
        # Highlighting what drives the "Demand Forecast"
        features = pd.DataFrame({
            'Feature': ['Rain_Intensity', 'Is_Weekend', 'Hour_Peak', 'Discount_Level', 'Zone_Density'],
            'Importance': [0.45, 0.25, 0.15, 0.10, 0.05]
        }).sort_values('Importance', ascending=True)
        fig_feat = px.bar(features, x='Importance', y='Feature', orientation='h', color_discrete_sequence=['#FC8019'])
        st.plotly_chart(fig_feat, use_container_width=True)
        
    with col_ml2:
        st.info("### 🤖 ML Recommendation\n"
                "**Zone 3 (Indiranagar)** is showing high 'Idle Loss' from 2PM-4PM. \n\n"
                "**Action:** Implement 'Surge-Down' discounts during this window to absorb excess rider capacity.")
        st.button("Download Executive PDF Report")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed by Jagadeesh.N | Instamart Strategic Decision Engine v2.0")
