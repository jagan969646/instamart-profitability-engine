import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- ADVANCED ENGINE CONFIG ---
st.set_page_config(page_title="Instamart Strategy v6.0", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png") 
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- ELITE EXECUTIVE CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0A0C10; }
    .kpi-box {
        background: linear-gradient(135deg, #FC8019 0%, #D86910 100%);
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 5px 5px 15px #000;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .kpi-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; color: white; }
    .kpi-value { font-size: 1.8rem; font-weight: 800; color: white; }
    
    .terminal-box {
        background-color: #000; border: 1px solid #2ECC71;
        padding: 15px; border-radius: 10px; font-family: 'Consolas', monospace;
    }
    .terminal-line { color: #2ECC71; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_and_engineer():
    if not os.path.exists(DATA_PATH):
        st.error("🚨 Missing Data: swiggy_simulated_data.csv")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Defaults for simulation
    if 'category' not in df.columns: df['category'] = np.random.choice(['FMCG', 'Perishable', 'Snacks'], len(df))
    if 'freshness_hrs_left' not in df.columns: df['freshness_hrs_left'] = np.random.randint(5, 48, len(df))
    
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['day'] = df['order_time'].dt.day_name()
    df['base_comm'] = df['order_value'] * 0.18
    df['ad_rev'] = df['order_value'] * 0.05
    return df

df = load_and_engineer()

# --- SIDEBAR: STRATEGIC CONTROLS ---
with st.sidebar:
    st.image(LOGO_PATH if os.path.exists(LOGO_PATH) else SWIGGY_URL, width=120)
    st.header("🕹️ Strategy Panel")
    
    # 1. Location & Market Situation
    selected_zones = st.multiselect("Geographic Clusters", df['zone'].unique(), default=df['zone'].unique()[:3])
    weather = st.selectbox("Current Weather", ["Clear", "Cloudy", "Heavy Rain", "Stormy"])
    situation = st.selectbox("Market Event", ["Standard", "IPL Match Night", "Weekend Peak", "End of Month"])
    
    st.divider()
    
    # 2. Financial Levers
    aov_adj = st.slider("AOV Boost (₹)", 0, 150, 30)
    surge_adj = st.slider("Surge Fee (₹)", 0, 100, 15)
    disc_opt = st.slider("Discount Cut (%)", 0, 100, 20)

    st.divider()
    
    # 3. Sidebar Pie Chart (Chart #1)
    st.write("### Simulation Rev Mix")
    temp_rev = pd.DataFrame({'Source': ['Comm', 'Ads', 'Fees'], 'Val': [18, 5, 10]})
    fig_side_pie = px.pie(temp_rev, values='Val', names='Source', hole=0.4, color_discrete_sequence=['#FC8019', '#3D4152', '#60B246'])
    fig_side_pie.update_layout(showlegend=False, height=200, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_side_pie, use_container_width=True)

# --- SIMULATION ENGINE ---
f_df = df[df['zone'].isin(selected_zones)].copy()

# Weather & Situation Modifiers
weather_mods = {"Clear": 1.0, "Cloudy": 1.1, "Heavy Rain": 1.6, "Stormy": 2.2}
sit_mods = {"Standard": 1.0, "IPL Match Night": 1.8, "Weekend Peak": 1.3, "End of Month": 0.9}

f_df['delivery_cost'] *= weather_mods[weather]
f_df['order_value'] *= sit_mods[situation]
f_df['order_value'] += aov_adj
f_df['delivery_fee'] += surge_adj
f_df['discount'] *= (1 - disc_opt/100)

f_df['net_profit'] = (f_df['base_comm'] + f_df['ad_rev'] + f_df['delivery_fee']) - \
                     (f_df['delivery_cost'] + f_df['discount'] + 14.0)

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='color: #FC8019;'>Instamart Strategy war Room v6.0</h1>", unsafe_allow_html=True)

# KPI Row
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi-box"><div class="kpi-label">GOV</div><div class="kpi-value">₹{f_df["order_value"].sum()/1e6:.2f}M</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi-box"><div class="kpi-label">CM2 / Order</div><div class="kpi-value">₹{f_df["net_profit"].mean():.2f}</div></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi-box"><div class="kpi-label">Net Margin</div><div class="kpi-value">{(f_df["net_profit"].sum()/f_df["order_value"].sum())*100:.1f}%</div></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="kpi-box"><div class="kpi-label">Risk Orders</div><div class="kpi-value">{len(f_df[f_df["net_profit"]<0])}</div></div>', unsafe_allow_html=True)

st.divider()

# --- THE ANALYTICS GRID (Charts 2-7) ---
tab1, tab2, tab3 = st.tabs(["📊 Profit Analytics", "🏍️ Ops & Weather", "🥬 Wastage Control"])

with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("### Chart #2: Unit Economics Waterfall")
        comps = ['Comm', 'Ads', 'Fees', 'Logistics', 'Discounts', 'OPEX']
        vals = [f_df['base_comm'].mean(), f_df['ad_rev'].mean(), f_df['delivery_fee'].mean(), 
                -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -14.0]
        fig2 = go.Figure(go.Waterfall(orientation="v", measure=["relative"]*6 + ["total"], x=comps + ['CM2'], y=vals + [0],
                                     totals={"marker":{"color":"#FC8019"}}, decreasing={"marker":{"color":"#FF4B4B"}}, increasing={"marker":{"color":"#2ECC71"}}))
        fig2.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        st.write("### Chart #3: Category Contribution")
        cat_data = f_df.groupby('category')['net_profit'].sum().reset_index()
        fig3 = px.bar(cat_data, x='category', y='net_profit', color='category', color_discrete_sequence=['#FC8019', '#60B246', '#3D4152'])
        fig3.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

with tab2:
    c3, c4 = st.columns(2)
    with c3:
        st.write("### Chart #4: Hourly Profitability Matrix")
        z_heat = f_df.pivot_table(index='zone', columns='hour', values='net_profit', aggfunc='mean')
        fig4 = px.imshow(z_heat, color_continuous_scale='RdYlGn', aspect="auto")
        fig4.update_layout(template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)
    with c4:
        st.write("### Chart #5: Delivery Cost vs Weather Surge")
        fig5 = px.line(f_df.groupby('hour')['delivery_cost'].mean().reset_index(), x='hour', y='delivery_cost', title=f"Cost Profile: {weather}")
        fig5.update_traces(line_color='#FC8019')
        fig5.update_layout(template="plotly_dark")
        st.plotly_chart(fig5, use_container_width=True)

with tab3:
    c5, c6 = st.columns([1, 1])
    with c5:
        st.write("### Chart #6: Freshness Risk by Zone")
        df_risk = f_df[f_df['freshness_hrs_left'] < 12]
        fig6 = px.box(f_df, x='zone', y='freshness_hrs_left', color='zone', points="all")
        fig6.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)
    with c6:
        st.write("### Chart #7: Wastage Value Distribution")
        fig7 = px.violin(f_df, y="order_value", x="category", color="category", box=True, points="all")
        fig7.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig7, use_container_width=True)
        
    if st.button("🚀 Push Flash Sale Notifications"):
        st.success(f"Sent 50% Off Coupons to {len(df_risk)*10} users near high-risk dark stores!")
        st.balloons()

st.markdown("---")
st.caption("Strategic Portfolio | Jagadeesh N | 2026 Build")
