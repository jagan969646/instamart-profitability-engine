import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime, timedelta

# --- CORE SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Singularity v8.0", page_icon="🧡", layout="wide")

# --- PATH & ASSET RECOVERY ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- ELITE WAR-ROOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 128, 25, 0.4);
        padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .metric-value { font-size: 2.2rem; font-weight: 900; color: #FC8019; }
    .metric-label { font-size: 0.75rem; letter-spacing: 2px; color: #888; text-transform: uppercase; }
    .terminal {
        background: #000; border-left: 5px solid #2ECC71;
        padding: 15px; font-family: 'Courier New', monospace; color: #2ECC71;
        font-size: 0.85rem; margin-bottom: 20px; border-radius: 0 10px 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- NEURAL DATA ENGINE ---
@st.cache_data
def load_and_engineer():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        zones = ['Koramangala', 'Indiranagar', 'HSR Layout', 'Whitefield', 'Jayanagar']
        categories = ['Perishables', 'FMCG', 'Munchies', 'Beverages', 'Personal Care']
        data = {
            'order_time': [datetime.now() - timedelta(minutes=x*10) for x in range(1000)],
            'order_value': np.random.uniform(200, 1500, 1000),
            'delivery_cost': np.random.uniform(40, 110, 1000),
            'discount': np.random.uniform(0, 120, 1000),
            'zone': np.random.choice(zones, 1000),
            'category': np.random.choice(categories, 1000),
            'freshness_hrs_left': np.random.randint(1, 48, 1000),
            'delivery_time_mins': np.random.randint(12, 45, 1000),
            'customer_rating': np.random.uniform(3.5, 5.0, 1000)
        }
        df = pd.DataFrame(data)

    df.columns = df.columns.str.strip().str.lower()
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['commission'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 25.0
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGIC CONTROL TOWER ---
with st.sidebar:
    st.image(SWIGGY_URL, width=120)
    st.header("🛰️ Operations")
    situation = st.selectbox("Market Situation", ["Standard Ops", "IPL Final Night", "Heavy Rain Surge", "Weekend Peak"])
    weather = st.select_slider("Weather Friction", options=["Clear", "Cloudy", "Heavy Rain", "Extreme Storm"])
    st.divider()
    aov_adj = st.slider("AOV Expansion (₹)", 0, 200, 30)
    surge_adj = st.slider("Dynamic Surge Alpha (₹)", 0, 100, 20)
    disc_cut = st.slider("Subsidy Optimization (%)", 0, 100, 15)
    
    st.info("System optimized for profitability v8.0")

# --- PREDICTIVE PHYSICS ---
f_df = df.copy()
sit_map = {"Standard Ops": 1.0, "IPL Final Night": 2.2, "Heavy Rain Surge": 1.7, "Weekend Peak": 1.4}
weather_map = {"Clear": 1.0, "Cloudy": 1.2, "Heavy Rain": 1.8, "Extreme Storm": 2.5}
cost_mult = sit_map[situation] * weather_map[weather]

f_df['delivery_cost'] *= cost_mult
f_df['order_value'] *= sit_map[situation]
f_df['order_value'] += aov_adj
f_df['delivery_fee'] += surge_adj
f_df['discount'] *= (1 - disc_cut/100)
f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# --- MAIN INTERFACE ---
st.markdown("<h1 style='color: #FC8019;'>INSTAMART <span style='color:#FFF; font-weight:100;'>SINGULARITY v8.0</span></h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("Projected GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M"),
    ("CM2 / Order", f"₹{f_df['net_profit'].mean():.2f}"),
    ("Net Margin", f"{(f_df['net_profit'].sum()/f_df['order_value'].sum())*100:.1f}%"),
    ("Profitable Orders", f"{(f_df['net_profit']>0).mean()*100:.1f}%")
]
for col, (l, v) in zip([c1, c2, c3, c4], metrics):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)

st.write("")
st.markdown(f"""<div class="terminal">> [LOG]: {situation.upper()} ACTIVE | WEATHER: {weather.upper()} ({weather_map[weather]}x Friction)<br>> [STATUS]: Engine online. Parameters synced.</div>""", unsafe_allow_html=True)

# --- THE 12 CHART MATRIX ---
t1, t2, t3, t4 = st.tabs(["💰 Financial Architecture", "📍 Zonal Analytics", "🥬 Inventory & Risk", "👥 Customer Experience"])

with t1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### 1. Revenue Elasticity Mix")
        fig1 = px.pie(values=[f_df['commission'].sum(), f_df['ad_rev'].sum(), f_df['delivery_fee'].sum()], 
                     names=['Commission', 'Ad Revenue', 'Delivery Fees'], hole=0.6, color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.write("### 2. CM2 Waterfall")
        comps = ['Comm', 'Ads', 'Fees', 'Logistics', 'Discounts', 'OPEX']
        vals = [f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0]
        fig2 = go.Figure(go.Waterfall(orientation="v", x=comps+['Total'], y=vals+[sum(vals)], measure=["relative"]*6+["total"]))
        fig2.update_layout(template="plotly_dark", height=350, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        st.write("### 3. Hourly GOV Momentum")
        hourly = f_df.groupby('hour')['order_value'].sum().reset_index()
        fig3 = px.line(hourly, x='hour', y='order_value', color_discrete_sequence=['#FC8019'], markers=True)
        fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

with t2:
    col4, col5, col6 = st.columns(3)
    with col4:
        st.write("### 4. Zonal Profit Heatmap")
        z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
        fig4 = px.imshow(z_heat, color_continuous_scale='RdYlGn')
        fig4.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)
    with col5:
        st.write("### 5. Order Density by Zone")
        fig5 = px.sunburst(f_df, path=['zone', 'category'], values='order_value', color='order_value', color_continuous_scale='Oranges')
        fig5.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig5, use_container_width=True)
    with col6:
        st.write("### 6. Profit Margin Distribution")
        fig6 = px.histogram(f_df, x="net_profit", nbins=40, color_discrete_sequence=['#2ECC71'], marginal="box")
        fig6.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig6, use_container_width=True)

with t3:
    col7, col8, col9 = st.columns(3)
    with col7:
        st.write("### 7. Freshness vs. Category")
        fig7 = px.box(f_df, x="category", y="freshness_hrs_left", color="category")
        fig7.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig7, use_container_width=True)
    with col8:
        st.write("### 8. High-Risk Inventory Scatter")
        fig8 = px.scatter(f_df, x="freshness_hrs_left", y="order_value", size="delivery_cost", color="zone", hover_name="category")
        fig8.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig8, use_container_width=True)
    with col9:
        st.write("### 9. Category Waste Exposure")
        waste = f_df[f_df['freshness_hrs_left'] < 10].groupby('category')['order_value'].sum().reset_index()
        fig9 = px.bar(waste, x='category', y='order_value', color='order_value', color_continuous_scale='Reds')
        fig9.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig9, use_container_width=True)

with t4:
    col10, col11, col12 = st.columns(3)
    with col10:
        st.write("### 10. Delivery Time Efficiency")
        fig10 = px.violin(f_df, y="delivery_time_mins", x="zone", box=True, color="zone")
        fig10.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig10, use_container_width=True)
    with col11:
        st.write("### 11. Customer Satisfaction vs. Profit")
        fig11 = px.scatter(f_df, x="delivery_time_mins", y="customer_rating", color="net_profit", size="order_value")
        fig11.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig11, use_container_width=True)
    with col12:
        st.write("### 12. Rating Distribution")
        fig12 = px.histogram(f_df, x="customer_rating", nbins=10, color_discrete_sequence=['#FC8019'])
        fig12.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig12, use_container_width=True)

    st.divider()
    if st.button("🚀 EXECUTE GLOBAL FLASH SALVAGE"):
        st.balloons()
        st.success("SIMULATION COMPLETE: EBITDA Leak plugged. Push notifications dispatched to local zones.")

st.markdown("---")
st.caption(f"PROPRIETARY STRATEGY ENGINE | JAGADEESH N | 2026 | STATUS: DEPLOYED")
