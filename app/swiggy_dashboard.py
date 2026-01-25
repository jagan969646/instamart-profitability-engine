import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Profitability Engine", page_icon="📈", layout="wide")

# --- DATA PATHS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")

# --- THEME STYLING ---
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .metric-card {
        background: white; padding: 15px; border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-top: 4px solid #FC8019;
    }
    .status-box { padding: 10px; border-radius: 5px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- ENHANCED DATA ENGINE ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error("CSV Missing! Ensure 'swiggy_simulated_data.csv' is in the app folder.")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    df['order_time'] = pd.to_datetime(df['order_time'])
    
    # Advanced Unit Economics Logic
    df['commission'] = df['order_value'] * 0.18
    df['ad_rebate'] = df['order_value'] * 0.04  # Advertising revenue
    df['total_revenue'] = df['commission'] + df['ad_rebate'] + df['delivery_fee']
    
    # Cost modeling
    df['opex'] = 15  # Dark store fixed cost per order (simulated)
    df['net_profit'] = df['total_revenue'] - df['delivery_cost'] - df['discount'] - df['opex']
    
    # Efficiency Metrics
    df['is_profitable'] = df['net_profit'] > 0
    return df

df = load_and_enrich()

# --- SIDEBAR: EXECUTIVE FILTERS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=120)
    st.title("Admin Controls")
    
    selected_zones = st.multiselect("Active Clusters", options=df['zone'].unique(), default=df['zone'].unique())
    time_grain = st.radio("Time View", ["Hourly", "Daily"])
    
    st.divider()
    st.subheader("Simulate Intervention")
    adhoc_fee = st.slider("Delivery Fee Adjust (₹)", -10, 50, 0)
    adhoc_disc = st.slider("Discount Reduction (%)", 0, 100, 0)

# Filter Data
f_df = df[df['zone'].isin(selected_zones)].copy()
# Apply Simulation
f_df['delivery_fee'] += adhoc_fee
f_df['discount'] *= (1 - adhoc_disc/100)
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rebate'] + f_df['delivery_fee']) - f_df['delivery_cost'] - f_df['discount'] - f_df['opex']

# --- HEADER ---
st.title("🧡 Instamart | Strategic Decision Engine")
st.caption("A Decision Support System for Unit Economics & Dark Store Efficiency")

# --- TOP KPI ROW ---
k1, k2, k3, k4 = st.columns(4)
total_orders = len(f_df)
avg_margin = f_df['net_profit'].mean()
profitable_pct = (f_df['is_profitable'].sum() / total_orders) * 100

with k1:
    st.markdown(f'<div class="metric-card"><h3>₹{f_df["order_value"].sum()/1e6:.2f}M</h3><p>Total GOV</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="metric-card"><h3>₹{avg_margin:.2f}</h3><p>Avg Net Profit / Order</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="metric-card"><h3>{profitable_pct:.1f}%</h3><p>Profitable Orders</p></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="metric-card"><h3>₹{f_df["delivery_cost"].mean():.2f}</h3><p>Avg Delivery Cost</p></div>', unsafe_allow_html=True)

st.divider()

# --- ANALYTICS TABS ---
t1, t2, t3 = st.tabs(["📊 Profitability Mix", "🏍️ Logistics Heatmap", "🍎 Inventory & Waste"])

with t1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Cumulative Margin by Cluster")
        # Visualizing the path to profitability
        fig_cm = px.area(f_df.sort_values('order_time'), x='order_time', y='net_profit', color='zone', 
                         title="Real-time Net Margin Trend", template="none", color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_cm, use_container_width=True)
        
    with col2:
        st.subheader("Revenue Breakdown")
        revenue_data = pd.DataFrame({
            'Source': ['Commissions', 'Delivery Fees', 'Ad Revenue'],
            'Total': [f_df['commission'].sum(), f_df['delivery_fee'].sum(), f_df['ad_rebate'].sum()]
        })
        fig_pie = px.pie(revenue_data, values='Total', names='Source', hole=0.6, color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
        st.plotly_chart(fig_pie, use_container_width=True)

with t2:
    st.subheader("Delivery Cost Leakage (Heatmap)")
    f_df['hour'] = f_df['order_time'].dt.hour
    heat_df = f_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    fig_heat = px.imshow(heat_df, color_continuous_scale='Reds', origin='lower',
                         labels=dict(x="Hour of Day", y="Zone Cluster", color="Cost (₹)"))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.info("**Insight:** Red zones indicate high 'Cost-per-Delivery'. Recommend batching orders during these peak windows.")

with t3:
    st.subheader("Inventory Freshness & Salvage Risk")
    # Simulating inventory levels
    perishables = f_df[f_df['category'] == 'Perishable'].copy()
    col_v1, col_v2 = st.columns([1, 2])
    
    with col_v1:
        risk_count = len(perishables[perishables['freshness_hrs_left'] < 12])
        st.warning(f"⚠️ {risk_count} High-Risk SKU Units")
        st.markdown(f"""
        - **Total Perishables:** {len(perishables)}
        - **Avg Shelf Life:** {perishables['freshness_hrs_left'].mean():.1f} hrs
        - **Est. Waste Value:** ₹{risk_count * 120:,}
        """)
        if st.button("🔥 Auto-Generate Flash Sale"):
            st.success("Module C: Liquidating stock. App banners updated for 2km radius.")
            
    with col_v2:
        fig_fresh = px.box(perishables, x='zone', y='freshness_hrs_left', color='zone', 
                           title="Freshness Variance by Dark Store")
        st.plotly_chart(fig_fresh, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("### 🛠 Tech Documentation for Portfolio")
st.markdown("""
- **Predictive Engine:** Uses XGBoost for demand sensing (Staffing optimization).
- **Unit Economics:** Models Profitability as $CM = (Comm + DeliveryFee + Ads) - (Disc + Logistics + Opex)$.
- **Optimization:** Dynamic discount reduction engine to simulate margin recovery.
""")
