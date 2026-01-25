import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")

# --- DATA ENGINE (WITH ROBUST ERROR HANDLING) ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 Data file not found at {DATA_PATH}. Please check your GitHub repository.")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    
    # PREVENT KEYERROR: Check if required columns exist, if not, create simulated ones
    required_cols = {
        'delivery_fee': 15, 
        'delivery_cost': 40,
        'discount': 20,
        'order_value': 450,
        'category': 'FMCG',
        'freshness_hrs_left': 24,
        'zone': 'Default Zone'
    }
    
    for col, default_val in required_cols.items():
        if col not in df.columns:
            df[col] = default_val

    df['order_time'] = pd.to_datetime(df['order_time'])
    
    # 💎 Advanced Financial Logic (The "Hiring" Logic)
    df['commission'] = df['order_value'] * 0.18 # Swiggy's take-rate
    df['ad_revenue'] = df['order_value'] * 0.05 # High-margin revenue
    df['gross_revenue'] = df['commission'] + df['ad_revenue'] + df['delivery_fee']
    
    # Cost modeling (Dark Store OPEX + Logistics)
    df['dark_store_cost'] = 12 # Fixed cost per order for warehouse
    df['contribution_margin'] = df['gross_revenue'] - df['delivery_cost'] - df['discount'] - df['dark_store_cost']
    
    return df

df = load_and_enrich()

# --- SIDEBAR: EXECUTIVE INTERVENTION ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=120)
    st.title("Admin HQ")
    
    target_zones = st.multiselect("Select Delivery Clusters", options=df['zone'].unique(), default=df['zone'].unique())
    
    st.divider()
    st.subheader("💡 'Path to Profit' Simulation")
    fee_bump = st.slider("Delivery Fee Increase (₹)", 0, 40, 5)
    discount_slashing = st.slider("Reduce Discounts by (%)", 0, 100, 25)
    
    st.info("Adjusting these levers simulates the impact on your Contribution Margin (CM).")

# --- PROCESS FILTERED DATA ---
f_df = df[df['zone'].isin(target_zones)].copy()
# Apply "What-If" Simulation Logic
f_df['delivery_fee'] += fee_bump
f_df['discount'] *= (1 - discount_slashing/100)
f_df['contribution_margin'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - f_df['delivery_cost'] - f_df['discount'] - f_df['dark_store_cost']

# --- MAIN DASHBOARD ---
st.title("🧡 Instamart | Strategic Decision Engine")
st.markdown("### `Unit Economics & Dark Store Efficiency Command Center` ")

# --- KPI METRICS ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M", "9.4% vs Prev")
with m2:
    avg_cm = f_df['contribution_margin'].mean()
    st.metric("Avg CM / Order", f"₹{avg_cm:.2f}", f"₹{avg_cm - df['contribution_margin'].mean():.1f} Delta", delta_color="normal")
with m3:
    prof_rate = (f_df['contribution_margin'] > 0).mean() * 100
    st.metric("Profitable Orders %", f"{prof_rate:.1f}%", "Target: 70%")
with m4:
    st.metric("Total Burn (Discounts)", f"₹{f_df['discount'].sum()/1e5:.1f}L", "-12% improvement", delta_color="inverse")

st.divider()

# --- TABS FOR MULTI-DIMENSIONAL ANALYSIS ---
tab_finance, tab_ops, tab_inv = st.tabs(["💰 Financial Performance", "🚲 Operational Efficiency", "🥬 Inventory Salvage"])

with tab_finance:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Margin Trajectory by Cluster")
        zone_perf = f_df.groupby('zone')['contribution_margin'].sum().reset_index().sort_values('contribution_margin')
        fig_cm = px.bar(zone_perf, x='contribution_margin', y='zone', orientation='h', 
                         color='contribution_margin', color_continuous_scale='RdYlGn', template="plotly_white")
        st.plotly_chart(fig_cm, use_container_width=True)
    
    with c2:
        st.subheader("Revenue Diversification")
        rev_data = pd.DataFrame({
            'Source': ['Commissions', 'Ads (CPG)', 'Delivery Fees'],
            'Val': [f_df['commission'].sum(), f_df['ad_revenue'].sum(), f_df['delivery_fee'].sum()]
        })
        fig_pie = px.pie(rev_data, values='Val', names='Source', hole=0.5, color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
        st.plotly_chart(fig_pie, use_container_width=True)

with tab_ops:
    st.subheader("Cost-per-Delivery (CPD) Peak Hour Analysis")
    f_df['hour'] = f_df['order_time'].dt.hour
    heat = f_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    fig_heat = px.imshow(heat, color_continuous_scale='Viridis', title="Dark Store Inefficiencies (Yellow = High Cost)")
    st.plotly_chart(fig_heat, use_container_width=True)
    st.info("🎯 **Strategic Opportunity:** High cost windows detected. Recommend order batching in yellow zones to lower CPD.")

with tab_inv:
    col_v1, col_v2 = st.columns([1, 2])
    perishables = f_df[f_df['category'] == 'Perishable'].copy()
    risk_units = perishables[perishables['freshness_hrs_left'] < 12]
    
    with col_v1:
        st.warning(f"🚨 {len(risk_units)} Units with <12h Shelf Life")
        st.markdown(f"**Potential Waste Loss:** ₹{len(risk_units)*150:,}")
        if st.button("🚀 Trigger 'Flash Sale' Push"):
            st.success("App Push Sent to 4,500 users in high-risk zones!")
            st.balloons()
            
    with col_v2:
        fig_fresh = px.box(perishables, x='zone', y='freshness_hrs_left', color='zone', title="Inventory Health by Cluster")
        st.plotly_chart(fig_fresh, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Jagadeesh.N | Built for Hyperlocal Analytics Case Studies")
