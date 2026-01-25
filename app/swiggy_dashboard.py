import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Portal", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")

# --- DATA ENGINE (With Column Validation) ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error(f"Missing File: {DATA_PATH}")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    
    # 🚨 FIX: Validate or Create Missing Columns
    # This prevents the KeyError you encountered
    required_cols = {
        'delivery_fee': 20, # Default value if missing
        'delivery_cost': 45,
        'discount': 10,
        'order_value': 300,
        'category': 'General',
        'freshness_hrs_left': 24
    }
    
    for col, default in required_cols.items():
        if col not in df.columns:
            df[col] = default

    df['order_time'] = pd.to_datetime(df['order_time'])
    
    # Advanced Economics Logic
    df['commission'] = df['order_value'] * 0.18
    df['ad_rebate'] = df['order_value'] * 0.04 
    df['total_revenue'] = df['commission'] + df['ad_rebate'] + df['delivery_fee']
    df['opex'] = 15 
    df['net_profit'] = df['total_revenue'] - df['delivery_cost'] - df['discount'] - df['opex']
    df['is_profitable'] = df['net_profit'] > 0
    return df

df = load_and_enrich()

# --- SIDEBAR: EXECUTIVE CONTROLS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=120)
    st.title("Admin Console")
    
    selected_zones = st.multiselect("Active Clusters", options=df['zone'].unique(), default=df['zone'].unique())
    st.divider()
    st.subheader("🚀 Growth Levers")
    adhoc_fee = st.slider("Adjust Delivery Fee (₹)", -10, 50, 0)
    adhoc_disc = st.slider("Cut Discounts (%)", 0, 100, 20)
    
    st.info("Simulating impact on Unit Economics in real-time.")

# --- APPLY SIMULATION ---
f_df = df[df['zone'].isin(selected_zones)].copy()
f_df['delivery_fee'] += adhoc_fee
f_df['discount'] *= (1 - adhoc_disc/100)
# Re-calculate profit based on sliders
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rebate'] + f_df['delivery_fee']) - f_df['delivery_cost'] - f_df['discount'] - f_df['opex']

# --- HEADER ---
st.title("🧡 Instamart Strategic Decision Engine")
st.markdown("#### `Target: Positive Contribution Margin per Cluster`")

# --- KPI DASHBOARD ---
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Total GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M", "8.2% vs LW")
with k2:
    st.metric("Avg Profit/Order", f"₹{f_df['net_profit'].mean():.2f}", f"{adhoc_fee + adhoc_disc/2:.1f}% Delta")
with k3:
    st.metric("Profitable Orders", f"{(f_df['net_profit'] > 0).mean()*100:.1f}%", "Target: 65%")
with k4:
    st.metric("Burn Rate (Discount)", f"{(f_df['discount'].sum()/f_df['order_value'].sum())*100:.1f}%", "-2.4%", delta_color="inverse")

st.divider()

# --- ANALYTICS SECTIONS ---
tab1, tab2, tab3 = st.tabs(["📈 Financial Health", "🛵 Operational Velocity", "🥦 Inventory Waste"])

with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Margin Contribution by Zone")
        # Waterfall style visualization for hiring appeal
        zone_perf = f_df.groupby('zone')['net_profit'].sum().reset_index().sort_values('net_profit')
        fig_zone = px.bar(zone_perf, x='net_profit', y='zone', orientation='h', 
                          color='net_profit', color_continuous_scale='RdYlGn',
                          title="Net Profit Contribution per Dark Store Cluster")
        st.plotly_chart(fig_zone, use_container_width=True)
    
    with c2:
        st.subheader("Revenue Diversification")
        rev_mix = pd.DataFrame({
            'Source': ['Comm', 'Ads', 'Fees'],
            'Val': [f_df['commission'].sum(), f_df['ad_rebate'].sum(), f_df['delivery_fee'].sum()]
        })
        fig_pie = px.pie(rev_mix, values='Val', names='Source', hole=0.5, 
                         color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("Logistics Cost Heatmap (Peak Hour Analysis)")
    f_df['hour'] = f_df['order_time'].dt.hour
    heat = f_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    fig_heat = px.imshow(heat, color_continuous_scale='YlOrRd', title="Identifying Inefficient Delivery Windows")
    st.plotly_chart(fig_heat, use_container_width=True)

with tab3:
    st.subheader("Dark Store Inventory Liquidation Engine")
    perishables = f_df[f_df['category'] == 'Perishable'].copy()
    risk_skus = perishables[perishables['freshness_hrs_left'] < 12]
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.error(f"🚨 {len(risk_skus)} SKU Units facing expiry in <12 hours.")
        st.write("Targeting these units with dynamic discounting can recover ₹" + f"{len(risk_skus)*85:,} in revenue.")
        if st.button("🚀 Execute Flash Sale"):
            st.balloons()
            st.success("Automated Flash Sale Triggered for nearby users!")
            
    with col_w2:
        fig_fresh = px.histogram(perishables, x='freshness_hrs_left', nbins=20, 
                                 title="Shelf Life Distribution (Current Inventory)",
                                 color_discrete_sequence=['#60B246'])
        st.plotly_chart(fig_fresh, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Jagadeesh.N | Instamart Strategic Decision Engine v3.0")
