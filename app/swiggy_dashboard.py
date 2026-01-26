import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- CORE SYSTEM CONFIG ---
st.set_page_config(page_title="INSTAMART | Strategic Singularity", page_icon="🧡", layout="wide")

# --- ASSET RECOVERY ---
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- ELITE WAR-ROOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    /* Neumorphic Strategy Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 128, 25, 0.4);
        padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .metric-value { font-size: 2rem; font-weight: 900; color: #FC8019; }
    .metric-label { font-size: 0.7rem; letter-spacing: 2px; color: #888; text-transform: uppercase; }
    
    /* Terminal Console */
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
    # Schema Protection
    DATA_PATH = "swiggy_simulated_data.csv"
    if not os.path.exists(DATA_PATH):
        st.error("DATABASE_OFFLINE: Connect swiggy_simulated_data.csv")
        st.stop()
    
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Auto-generate advanced vectors if missing
    if 'category' not in df.columns: df['category'] = np.random.choice(['Perishables', 'FMCG', 'Munchies'], len(df))
    if 'freshness_hrs_left' not in df.columns: df['freshness_hrs_left'] = np.random.randint(4, 48, len(df))
    if 'delivery_fee' not in df.columns: df['delivery_fee'] = 20.0
    
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['commission'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGIC CONTROL TOWER ---
with st.sidebar:
    st.image(SWIGGY_URL, width=120)
    st.header("🛰️ Operations Control")
    
    # Contextual Modifiers
    situation = st.selectbox("Market Situation", ["Standard Ops", "IPL Final Night", "Heavy Rain Surge", "Weekend Peak"])
    weather = st.select_slider("Weather Friction", options=["Clear", "Cloudy", "Heavy Rain", "Extreme Storm"])
    
    st.divider()
    
    # Financial Levers
    aov_adj = st.slider("AOV Expansion (₹)", 0, 200, 50)
    surge_adj = st.slider("Dynamic Surge Alpha (₹)", 0, 100, 25)
    disc_cut = st.slider("Subsidy Optimization (%)", 0, 100, 20)

    st.divider()
    
    # CHART #1: Sidebar Revenue Elasticity (Pie)
    st.write("### Simulation Revenue Mix")
    fig1 = px.pie(values=[18, 5, 12], names=['Comm', 'Ads', 'Fees'], hole=0.6, 
                 color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
    fig1.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

# --- PREDICTIVE SIMULATION ENGINE ---
f_df = df.copy()

# Market Physics Matrix
sit_map = {"Standard Ops": 1.0, "IPL Final Night": 2.2, "Heavy Rain Surge": 1.7, "Weekend Peak": 1.4}
weather_map = {"Clear": 1.0, "Cloudy": 1.2, "Heavy Rain": 1.8, "Extreme Storm": 2.5}

# Apply Global Physics
cost_mult = sit_map[situation] * weather_map[weather]
f_df['delivery_cost'] *= cost_mult
f_df['order_value'] *= sit_map[situation]
f_df['order_value'] += aov_adj
f_df['delivery_fee'] += surge_adj
f_df['discount'] *= (1 - disc_cut/100)

f_df['net_profit'] = (f_df['commission'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + 15.0)

# --- MAIN INTERFACE ---
st.markdown("<h1 style='color: #FC8019;'>INSTAMART <span style='color:#FFF; font-weight:100;'>SINGULARITY v7.2</span></h1>", unsafe_allow_html=True)

# Top KPI Matrix
c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("Projected GOV", f"₹{f_df['order_value'].sum()/1e6:.2f}M"),
    ("CM2 / Order", f"₹{f_df['net_profit'].mean():.2f}"),
    ("Net Margin", f"{(f_df['net_profit'].sum()/f_df['order_value'].sum())*100:.1f}%"),
    ("System Alpha", f"{(f_df['net_profit']>0).mean()*100:.1f}pts")
]
for col, (l, v) in zip([c1, c2, c3, c4], metrics):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)

st.write("")
st.markdown(f"""<div class="terminal">> [LOG]: {situation.upper()} ACTIVE | WEATHER_INDEX: {weather_map[weather]}x<br>> [ACTION]: Applying Alpha-Surge ₹{surge_adj} | AOV Target +₹{aov_adj}</div>""", unsafe_allow_html=True)

# --- THE 7 REMAINING CHARTS ---
t1, t2, t3 = st.tabs(["💎 Financial Architecture", "📍 Zonal Intelligence", "🥬 Wastage & Push AI"])

with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write("### Chart #2: CM2 Waterfall Structure")
        
        comps = ['Comm', 'Ads', 'Fees', 'Logistics', 'Discounts', 'OPEX']
        vals = [f_df['commission'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), 
                -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -15.0]
        fig2 = go.Figure(go.Waterfall(orientation="v", x=comps+['Total'], y=vals+[0], measure=["relative"]*6+["total"]))
        fig2.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        st.write("### Chart #3: Daily GOV Vector")
        fig3 = px.line(f_df.groupby('hour')['order_value'].sum().reset_index(), x='hour', y='order_value')
        fig3.update_traces(line_color='#FC8019', fill='tozeroy')
        fig3.update_layout(template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

with t2:
    col_c, col_d = st.columns(2)
    with col_c:
        st.write("### Chart #4: Zonal Profitability Heatmap")
        z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
        fig4 = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
        fig4.update_layout(template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)
    with col_d:
        st.write("### Chart #5: Profit Distribution (Risk)")
        fig5 = px.histogram(f_df, x="net_profit", nbins=50, color_discrete_sequence=['#FC8019'], marginal="box")
        fig5.update_layout(template="plotly_dark")
        st.plotly_chart(fig5, use_container_width=True)

with t3:
    col_e, col_f = st.columns(2)
    with col_e:
        st.write("### Chart #6: Freshness vs. Category Risk")
        fig6 = px.box(f_df, x="category", y="freshness_hrs_left", color="category")
        fig6.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)
    with col_f:
        st.write("### Chart #7: Inventory Value at Risk")
        
        fig7 = px.scatter(f_df[f_df['freshness_hrs_left'] < 12], x="order_value", y="delivery_cost", color="zone", size="order_value")
        fig7.update_layout(template="plotly_dark")
        st.plotly_chart(fig7, use_container_width=True)
    
    st.write("### Chart #8: Predicted Salvage Reach")
    fig8 = px.bar(x=['Push Notifications', 'In-App Banners', 'SMS Alerts'], y=[85, 92, 45], 
                 labels={'x': 'Channel', 'y': 'Success %'}, color_discrete_sequence=['#60B246'])
    fig8.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig8, use_container_width=True)
    
    if st.button("🚀 EXECUTE GLOBAL FLASH SALVAGE"):
        st.success("SIMULATION COMPLETE: EBITDA Leak plugged. Push notifications dispatched.")
        st.balloons()

st.markdown("---")
st.caption("PROPRIETARY STRATEGY ENGINE | JAGADEESH N | 2026")
