import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS & CONSTANTS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- CUSTOM EXECUTIVE STYLING ---
st.markdown("""
<style>
    .main-title {
        color: #FC8019;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        font-size: 2.5rem;
    }
    .target-sub {
        color: #3D4152;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
    .kpi-metric {
        background-color: #FC8019;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .kpi-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .kpi-subbox {
        margin-top: 10px;
        background-color: rgba(0,0,0,0.2);
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_and_enrich():
    # Creating simulated data if file doesn't exist for demo purposes
    if not os.path.exists(DATA_PATH):
        dates = pd.date_range(start='2025-12-01', periods=1000, freq='H')
        df = pd.DataFrame({
            'order_time': np.random.choice(dates, 1000),
            'zone': np.random.choice(['Indiranagar', 'Koramangala', 'HSR Layout', 'Adyar', 'Velachery'], 1000),
            'weather': np.random.choice(['Clear', 'Rainy', 'Overcast'], 1000),
            'category': np.random.choice(['FMCG', 'Perishable', 'Snacks', 'Beverages'], 1000),
            'order_value': np.random.normal(450, 100, 1000).clip(150, 1200),
            'delivery_fee': np.random.choice([15, 25, 35], 1000),
            'delivery_cost': np.random.normal(45, 10, 1000).clip(30, 80),
            'discount': np.random.normal(30, 15, 1000).clip(0, 100),
            'freshness_hrs_left': np.random.randint(2, 48, 1000)
        })
    else:
        df = pd.read_csv(DATA_PATH)
        df['order_time'] = pd.to_datetime(df['order_time'])

    # Fixed Economics [cite: 19, 24]
    df['commission'] = df['order_value'] * 0.18
    df['ad_revenue'] = df['order_value'] * 0.05
    df['opex'] = 12 
    return df

df = load_and_enrich()

# --- SIDEBAR CONTROL TOWER ---
with st.sidebar:
    st.image(SWIGGY_URL, width=120)
    st.title("Control Tower")
    
    st.subheader("📍 Market Clusters")
    zones = st.multiselect("Select Zones", df['zone'].unique(), df['zone'].unique())
    
    st.subheader("🛠️ Profitability Simulator")
    aov_boost = st.slider("AOV Expansion Strategy (₹)", 0, 150, 50, help="Simulating bundling & upsell impact [cite: 44, 45]")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 5)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 20, help="Reducing burn rate [cite: 37]")
    
    st.divider()
    st.info("💡 **BBA Insight:** Increasing AOV is the strongest lever for CM2 positivity. [cite: 34, 36]")

# --- SIMULATION LOGIC ---
f_df = df[df['zone'].isin(zones)].copy()
f_df['order_value'] += aov_boost
f_df['commission'] = f_df['order_value'] * 0.18 # Recalculate based on new AOV [cite: 17]
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

# CM2 Calculation: (Comm + Ads + Fees) - (Deliv Cost + Discount + Opex) [cite: 16, 20, 24]
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + f_df['opex'])

# --- HEADER ---
st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
st.markdown("<div class='target-sub'>🚀 Target: **Positive Contribution Margin (CM2)** by June 2026</div>", unsafe_allow_html=True)

# --- KPI ROW ---
total_gov = f_df['order_value'].sum()
avg_cm = f_df['net_profit'].mean()
burn_rate = (f_df['discount'].sum() / total_gov) * 100
orders = len(f_df)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-metric"><div style="font-size:1.8rem;">₹{total_gov/1e5:.1f}L</div><div class="kpi-label">Total GOV</div><div class="kpi-subbox">Scale Metric [cite: 14]</div></div>', unsafe_allow_html=True)
with k2:
    color = "#22C55E" if avg_cm > 0 else "#FF4B4B"
    st.markdown(f'<div class="kpi-metric" style="background-color:{color};"><div style="font-size:1.8rem;">₹{avg_cm:.2f}</div><div class="kpi-label">Avg. CM2 / Order</div><div class="kpi-subbox">Profit Lever [cite: 16]</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-metric"><div style="font-size:1.8rem;">{burn_rate:.1f}%</div><div class="kpi-label">Burn Rate</div><div class="kpi-subbox">Efficiency [cite: 37]</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-metric"><div style="font-size:1.8rem;">{orders:,}</div><div class="kpi-label">Sample Size</div><div class="kpi-subbox">Modeled Orders</div></div>', unsafe_allow_html=True)

st.divider()

# --- ANALYTICS TABS ---
t1, t2, t3, t4 = st.tabs(["📊 Financials", "🏍️ Ops & Logistics", "🥬 Wastage Control", "🧠 Demand Sensing"])

with t1:
    st.subheader("Unit Economics Waterfall (CM2 Breakdown)")
    # [cite: 17, 19]
    metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
    vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
            -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]
    
    fig_water = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["relative"] * 6 + ["total"],
        x = metrics + ['Net CM2'],
        y = vals + [0],
        decreasing = {"marker":{"color":"#EF4444"}},
        increasing = {"marker":{"color":"#22C55E"}},
        totals = {"marker":{"color":"#3D4152"}}
    ))
    fig_water.update_layout(template="none", height=450)
    st.plotly_chart(fig_water, use_container_width=True)
    

with t2:
    st.subheader("Delivery Cost Sensitivity by Zone")
    # [cite: 30, 38]
    fig_ops = px.box(f_df, x='zone', y='delivery_cost', color='zone', 
                     title="Last-Mile Cost Variance (Target: Batching Optimization)")
    st.plotly_chart(fig_ops, use_container_width=True)
    st.success("💡 **Recommendation:** Reducing delivery cost via batching is more sustainable than price hikes. [cite: 39]")

with t3:
    st.subheader("Wastage & Freshness Risk [cite: 63, 66]")
    perishables = f_df[f_df['category'] == 'Perishable']
    risk_count = len(perishables[perishables['freshness_hrs_left'] < 12])
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Units at High Risk (<12h)", risk_count)
        if st.button("🚀 Trigger Flash Liquidation"):
            st.toast("Discount notifications sent to nearby users!")
            st.balloons()
    with c2:
        fig_fresh = px.histogram(perishables, x='freshness_hrs_left', nbins=10, 
                                 title="Inventory Freshness Distribution", color_discrete_sequence=['#60B246'])
        st.plotly_chart(fig_fresh, use_container_width=True)

with t4:
    st.subheader("Predictive Demand Sensing (XGBoost Simulation) [cite: 55, 66]")
    # Simulated forecast line [cite: 51]
    f_df['hour'] = f_df['order_time'].dt.hour
    hourly_data = f_df.groupby('hour')['order_value'].sum().reset_index()
    hourly_data['forecast'] = hourly_data['order_value'] * np.random.uniform(0.95, 1.05, len(hourly_data))
    
    fig_demand = go.Figure()
    fig_demand.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['order_value'], name="Actual Demand", line=dict(color='#3D4152')))
    fig_demand.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['forecast'], name="Predicted (XGBoost)", line=dict(dash='dash', color='#FC8019')))
    st.plotly_chart(fig_demand, use_container_width=True)

# --- FOOTER ---
st.divider()
st.caption("Developed by **Jagadeesh N** | BBA, SRM IST (2023-26) | Aspiring Business Analyst")
st.caption("Built to solve real-world Q-commerce unit economics. [View GitHub Repo](https://github.com/jagan969646)")
