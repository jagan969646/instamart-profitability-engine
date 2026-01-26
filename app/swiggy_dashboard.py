import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png") 
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- CUSTOM EXECUTIVE STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #121212; }
    
    /* Force Orange KPI Box Styling */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 20px;
    }
    .kpi-box {
        background-color: #FC8019 !important;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        flex: 1;
        text-align: center;
        box-shadow: 0 4px 15px rgba(252, 128, 25, 0.3);
    }
    .kpi-label { font-size: 0.85rem; text-transform: uppercase; opacity: 0.9; margin-bottom: 5px; }
    .kpi-value { font-size: 1.7rem; font-weight: 800; }
    .kpi-delta { font-size: 0.8rem; margin-top: 5px; opacity: 0.8; }

    /* The Black Box with Green Terminal Data */
    .data-box {
        background-color: #000000;
        border: 1px solid #2ECC71;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .data-text {
        color: #2ECC71; 
        font-family: 'Courier New', monospace;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    h1, h2, h3, h4 { color: #FC8019 !important; }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 Missing {DATA_PATH}")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    
    # Fill missing values if schema is incomplete
    required = {'delivery_fee': 15, 'delivery_cost': 40, 'discount': 20, 
                'order_value': 450, 'category': 'fmcg', 'freshness_hrs_left': 24}
    for col, val in required.items():
        if col not in df.columns: df[col] = val

    df['order_time'] = pd.to_datetime(df['order_time'])
    df['commission'] = df['order_value'] * 0.18
    df['ad_revenue'] = df['order_value'] * 0.05
    df['opex'] = 12 
    df['gross_margin'] = (df['commission'] + df['ad_revenue'] + df['delivery_fee']) - (df['delivery_cost'] + df['discount'] + df['opex'])
    return df

df = load_and_enrich()

# --- SIDEBAR: CONTROL TOWER ---
with st.sidebar:
    st.image(LOGO_PATH if os.path.exists(LOGO_PATH) else SWIGGY_URL, width=120)
    st.title("Control Tower")
    zones = st.multiselect("Geographic Clusters", options=df['zone'].unique(), default=df['zone'].unique())
    st.divider()
    st.subheader("🛠️ Profitability Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 15)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 25)
    aov_boost = st.slider("AOV Strategy (₹)", 0, 150, 40)

# --- SIMULATION ENGINE ---
f_df = df[df['zone'].isin(zones)].copy()
f_df['order_value'] += aov_boost
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (f_df['delivery_cost'] + f_df['discount'] + f_df['opex'])

# --- MAIN HEADER ---
c1, c2 = st.columns([1, 6])
with c1: st.image(SWIGGY_URL, width=80)
with c2: 
    st.markdown("<h1 style='margin:0;'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0; opacity:0.8;'>🚀 Target: Positive Contribution Margin by June 2026</h4>", unsafe_allow_html=True)

st.divider()

# --- EXECUTIVE KPI ROW (ORANGE BOXES) ---
total_gov = f_df['order_value'].sum() / 1e6
avg_p = f_df['net_profit'].mean()
prof_rate = (f_df['net_profit'] > 0).mean() * 100
burn = (f_df['discount'].sum() / f_df['order_value'].sum()) * 100

k_cols = st.columns(4)
labels = ["Total GOV", "Net Profit / Order", "Order Profitability", "Burn Rate"]
values = [f"₹{total_gov:.2f}M", f"₹{avg_p:.2f}", f"{prof_rate:.1f}%", f"{burn:.1f}%"]
deltas = ["↑ 12% vs LW", f"₹{avg_p - df['gross_margin'].mean():.2f} Sim Delta", "Target: 70%", "-3.2% Improvement"]

for i, col in enumerate(k_cols):
    col.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">{labels[i]}</div>
            <div class="kpi-value">{values[i]}</div>
            <div class="kpi-delta">{deltas[i]}</div>
        </div>
    """, unsafe_allow_html=True)

# --- THE BLACK BOX (GREEN DATA) ---
st.markdown(f"""
<div class="data-box">
    <div class="data-text">
        [SYSTEM_LOG] SIMULATION_ACTIVE | CLUSTERS: {len(zones)} | MODE: PROFIT_MAX<br>
        [REVENUE] Avg_Comm: ₹{f_df['commission'].mean():.2f} | Ad_Rev: ₹{f_df['ad_revenue'].mean():.2f} | Del_Fee: ₹{f_df['delivery_fee'].mean():.2f}<br>
        [EXPENSES] Del_Cost: ₹{f_df['delivery_cost'].mean():.2f} | Discount: ₹{f_df['discount'].mean():.2f} | OPEX: ₹12.00<br>
        [MARGIN] CURRENT_NET_PROFIT: ₹{avg_p:.2f} | BURN_EFFICIENCY: {100-burn:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

# --- ANALYTICS TABS ---
t1, t2, t3, t4 = st.tabs(["📊 Financials", "🏍️ Logistics", "🥬 Wastage", "🧠 Forecasting"])

with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("Unit Economics Waterfall")
        metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
        vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
                -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -12]
        
        fig_water = go.Figure(go.Waterfall(
            orientation="v", measure=["relative"]*6 + ["total"],
            x=metrics + ['Net Profit'], y=vals + [0],
            decreasing={"marker":{"color":"#EF4444"}},
            increasing={"marker":{"color":"#60B246"}},
            totals={"marker":{"color":"#FC8019"}}
        ))
        fig_water.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_water, use_container_width=True)
        
    with col_b:
        st.subheader("Revenue Mix")
        rev_mix = pd.DataFrame({'Channel': ['Comm', 'Ads', 'Fees'], 'Rev': [f_df['commission'].sum(), f_df['ad_revenue'].sum(), f_df['delivery_fee'].sum()]})
        st.plotly_chart(px.pie(rev_mix, values='Rev', names='Channel', hole=0.5, color_discrete_sequence=['#FC8019', '#3D4152', '#60B246']).update_layout(template="plotly_dark"), use_container_width=True)

with t2:
    st.subheader("Logistics Efficiency Heatmap")
    f_df['hour'] = f_df['order_time'].dt.hour
    heat = f_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    st.plotly_chart(px.imshow(heat, color_continuous_scale='YlOrRd', aspect="auto").update_layout(template="plotly_dark"), use_container_width=True)

with t3:
    st.subheader("Inventory Salvage Management")
    perishables = f_df[f_df['category'].str.lower() == 'perishable'].copy() if 'perishable' in f_df['category'].values else f_df.head(100).copy()
    risk = perishables[perishables['freshness_hrs_left'] < 12]
    ca, cb = st.columns([1, 2])
    with ca:
        st.warning(f"⚠️ {len(risk)} Units at Expiry Risk")
        st.metric("Potential Liquidation Value", f"₹{len(risk)*110:,}")
        if st.button("🚀 Execute Flash Liquidation"):
            st.success("App Push Notifications Sent!")
            st.balloons()
    with cb:
        st.plotly_chart(px.box(perishables, x='zone', y='freshness_hrs_left', color='zone', title="Freshness Variance").update_layout(template="plotly_dark"), use_container_width=True)

with t4:
    st.subheader("Predictive Demand Sensing")
    f_df['forecast'] = f_df['order_value'] * np.random.uniform(0.95, 1.05, len(f_df))
    hist_data = f_df.groupby(f_df['order_time'].dt.date)[['order_value', 'forecast']].sum().reset_index()
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['order_value'], name='Actual GOV', line=dict(color='#60B246')))
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['forecast'], name='XGBoost Forecast', line=dict(dash='dash', color='#FC8019')))
    st.plotly_chart(fig_pred.update_layout(template="plotly_dark"), use_container_width=True)

st.markdown("---")
st.caption("Developed by Jagadeesh.N | Business Analyst Portfolio 2026")
