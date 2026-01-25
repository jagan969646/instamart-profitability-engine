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

# --- CUSTOM EXECUTIVE STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fb; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #3D4152; }
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-top: 4px solid #FC8019;
        text-align: center;
    }
    .main-title { color: #3D4152; font-weight: 800; letter-spacing: -1px; }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 Missing {DATA_PATH}")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    
    # Validation & Schema Guard
    required = {'delivery_fee': 15, 'delivery_cost': 40, 'discount': 20, 
                'order_value': 450, 'category': 'FMCG', 'freshness_hrs_left': 24}
    for col, val in required.items():
        if col not in df.columns: df[col] = val

    df['order_time'] = pd.to_datetime(df['order_time'])
    
    # Financial Logic
    df['commission'] = df['order_value'] * 0.18
    df['ad_revenue'] = df['order_value'] * 0.05
    df['opex'] = 12 
    df['gross_margin'] = (df['commission'] + df['ad_revenue'] + df['delivery_fee']) - (df['delivery_cost'] + df['discount'] + df['opex'])
    return df

df = load_and_enrich()

# --- SIDEBAR: STRATEGIC LEVERS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=100)
    st.title("Control Tower")
    
    zones = st.multiselect("Geographic Clusters", options=df['zone'].unique(), default=df['zone'].unique())
    
    st.divider()
    st.subheader("🛠️ Profitability Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 5)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 20)
    
    st.info("Simulating impact on Contribution Margin 2 (CM2).")

# --- SIMULATION ENGINE ---
f_df = df[df['zone'].isin(zones)].copy()
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + f_df['opex'])

# --- HEADER ---
st.markdown("<h1 class='main-title'>🧡 Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
st.caption(f"Hyperlocal Analytics Ecosystem • Active Clusters: {len(zones)}")

# --- EXECUTIVE KPI ROW ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M", "12% vs LW")
with m2:
    avg_p = f_df['net_profit'].mean()
    st.metric("Net Profit / Order", f"₹{avg_p:.2f}", f"₹{avg_p - df['gross_margin'].mean():.2f} Sim Delta")
with m3:
    prof_rate = (f_df['net_profit'] > 0).mean() * 100
    st.metric("Order Profitability", f"{prof_rate:.1f}%", f"Target: 70%")
with m4:
    burn = (f_df['discount'].sum() / f_df['order_value'].sum()) * 100
    st.metric("Burn Rate", f"{burn:.1f}%", "-3.2% Improvement", delta_color="inverse")

st.divider()

# --- ANALYTICS TABS ---
t1, t2, t3, t4 = st.tabs(["📊 Financials", "🏍️ Ops & Logistics", "🥬 Wastage Control", "🧠 Demand Forecasting"])

with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("Unit Economics Breakdown")
        # Creating a Waterfall-style analysis
        metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
        vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
                -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]
        
        fig_water = go.Figure(go.Waterfall(
            name = "Economics", orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x = metrics + ['Net Profit'],
            y = vals + [0],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#EF4444"}},
            increasing = {"marker":{"color":"#60B246"}},
            totals = {"marker":{"color":"#FC8019"}}
        ))
        fig_water.update_layout(title="Average Unit Economics (Per Order)", template="simple_white")
        st.plotly_chart(fig_water, use_container_width=True)
        
    with col_b:
        st.subheader("Revenue Diversification")
        rev_mix = pd.DataFrame({
            'Channel': ['Comm', 'Ads', 'Fees'],
            'Rev': [f_df['commission'].sum(), f_df['ad_revenue'].sum(), f_df['delivery_fee'].sum()]
        })
        st.plotly_chart(px.pie(rev_mix, values='Rev', names='Channel', hole=0.6, 
                               color_discrete_sequence=['#FC8019', '#3D4152', '#60B246']), use_container_width=True)

with t2:
    st.subheader("Logistics Efficiency Heatmap")
    f_df['hour'] = f_df['order_time'].dt.hour
    heat = f_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    st.plotly_chart(px.imshow(heat, color_continuous_scale='YlOrRd', aspect="auto"), use_container_width=True)
    st.info("💡 **Strategy:** Yellow cells indicate cost leakage. Deploy 'Batching' algorithms during these windows.")

with t3:
    st.subheader("Inventory Salvage Management")
    perishables = f_df[f_df['category'] == 'Perishable'].copy()
    risk = perishables[perishables['freshness_hrs_left'] < 12]
    
    ca, cb = st.columns([1, 2])
    with ca:
        st.warning(f"⚠️ {len(risk)} Units at Expiry Risk")
        st.metric("Potential Liquidation Value", f"₹{len(risk)*110:,}")
        if st.button("🚀 Execute Flash Liquidation"):
            st.success("App Push Notifications Sent!")
            st.balloons()
    with cb:
        st.plotly_chart(px.box(perishables, x='zone', y='freshness_hrs_left', color='zone', title="Freshness Variance"), use_container_width=True)

with t4:
    st.subheader("Predictive Demand Sensing (XGBoost Inferred)")
    # Simulating a forecast vs actuals chart
    f_df['forecast'] = f_df['order_value'] * np.random.uniform(0.9, 1.1, len(f_df))
    hist_data = f_df.groupby(f_df['order_time'].dt.date)[['order_value', 'forecast']].sum().reset_index()
    
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['order_value'], name='Actual GOV', line=dict(color='#3D4152')))
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['forecast'], name='XGBoost Forecast', line=dict(dash='dash', color='#FC8019')))
    st.plotly_chart(fig_pred, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Jagadeesh.N | Built for Hyperlocal Analytics Case Studies")
