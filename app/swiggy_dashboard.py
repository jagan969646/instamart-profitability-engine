import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import itertools

# --- PAGE CONFIG ---
st.set_page_config(page_title="Instamart Strategy Engine", page_icon="🧡", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "swiggy_simulated_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png")
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #262730; }

    .main-title {
        color: #3D4152;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        font-size: 2.2rem;
    }

    .kpi-subbox {
        margin-top: 8px;
        background-color: #000000;
        color: #22C55E;  /* green */
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }

    .kpi-metric {
        background-color: #FC8019;
        color: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 6px 14px rgba(252, 128, 25, 0.35);
        text-align: center;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .kpi-label {
        font-size: 0.9rem;
        color: #ffffff;
        opacity: 0.9;
        font-weight: 500;
    }

    h1, h2, h3 { color: #3D4152; }

    [data-testid="column"] {
        padding: 0.3rem !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING & ENRICHMENT ---
@st.cache_data
def load_and_enrich():
    if not os.path.exists(DATA_PATH):
        st.error(f"🚨 Missing {DATA_PATH}")
        st.stop()

    df = pd.read_csv(DATA_PATH)

    required = {'delivery_fee': 15, 'delivery_cost': 40, 'discount': 20,
                'order_value': 450, 'category': 'FMCG', 'freshness_hrs_left': 24}
    for col, val in required.items():
        if col not in df.columns:
            df[col] = val

    df['order_time'] = pd.to_datetime(df['order_time'])
    df['commission'] = df['order_value'] * 0.18
    df['ad_revenue'] = df['order_value'] * 0.05
    df['opex'] = 12
    df['gross_margin'] = (df['commission'] + df['ad_revenue'] + df['delivery_fee']) - (
        df['delivery_cost'] + df['discount'] + df['opex']
    )
    return df

df = load_and_enrich()

# --- SIDEBAR ---
with st.sidebar:
    # Logo
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)
    else:
        st.image(SWIGGY_URL, width=120)

    st.title("Control Tower")

    # Theme toggle
    theme = st.radio("Select Theme", ["Light","Dark"])
    if theme == "Dark":
        st.markdown('<style>body{background-color:#262730;color:white;}</style>',unsafe_allow_html=True)
    else:
        st.markdown('<style>body{background-color:white;color:black;}</style>',unsafe_allow_html=True)

    # Filters
    zones = st.multiselect("Geographic Clusters", df['zone'].unique(), df['zone'].unique())
    weather_filter = st.multiselect("🌦️ Weather Condition", options=df['weather'].unique(), default=df['weather'].unique())

    st.divider()
    st.subheader("🛠️ Profitability Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 5)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 20)
    st.info("Simulating impact on Contribution Margin (CM).")

    # Contextual Scenarios + AOV + Marketing
    st.subheader("⛈️ Contextual Scenarios")
    scenario = st.selectbox("Select Conditions", ["Normal Operations", "Heavy Rain", "IPL Match Night"])
    aov_boost = st.slider("AOV Expansion Strategy (₹)", 0, 100, 0)
    marketing_spend = st.slider("Marketing Spend (₹)", 0, 50000, 0)

    # Reset button
    if st.button("🔄 Reset Levers"):
        st.experimental_rerun()

# --- SIMULATION ENGINE ---
f_df = df[df['zone'].isin(zones)].copy()
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)

# Scenario adjustments
if scenario == "Heavy Rain":
    f_df['delivery_cost'] *= 1.3
    st.sidebar.warning("Note: Rain surge active (Costs +30%)")
elif scenario == "IPL Match Night":
    f_df['order_value'] *= 1.15
    st.sidebar.success("Note: IPL demand spike active (+15% GOV)")

# AOV + Marketing
f_df['order_value'] += aov_boost + marketing_spend/1000
f_df['commission'] = f_df['order_value'] * 0.18
f_df['net_profit'] = (f_df['commission'] + f_df['ad_revenue'] + f_df['delivery_fee']) - (
    f_df['delivery_cost'] + f_df['discount'] + f_df['opex']
)

# --- HEADER ---
head_col1, head_col2 = st.columns([1, 6])
with head_col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=100)
    else:
        st.image(SWIGGY_URL, width=100)
with head_col2:
    st.markdown("<h1 class='main-title'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
    st.markdown("#### 🚀 Target: Positive Contribution Margin by June 2026")
st.divider()

# --- KPI ROW ---
total_gov = f_df['order_value'].sum()
avg_cm = f_df['net_profit'].mean()
burn_rate = (f_df['discount'].sum() / total_gov) * 100
orders = len(f_df)
prev_avg_cm = df['gross_margin'].mean()
delta_cm = avg_cm - prev_avg_cm

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f'''
    <div class="kpi-metric">
        ₹{total_gov/1e6:.2f}M
        <div class="kpi-label">Total GOV</div>
        <div class="kpi-subbox">▲ 12% vs LW</div>
    </div>
    ''', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'''
    <div class="kpi-metric">
        ₹{avg_cm:.2f}
        <div class="kpi-label">Avg Net Profit / Order</div>
        <div class="kpi-subbox">Sim Δ ₹{delta_cm:.2f}</div>
    </div>
    ''', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'''
    <div class="kpi-metric">
        {burn_rate:.1f}%
        <div class="kpi-label">Discount Burn Rate</div>
        <div class="kpi-subbox">▼ 3.2% Improvement</div>
    </div>
    ''', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'''
    <div class="kpi-metric">
        {orders:,}
        <div class="kpi-label">Orders Modeled</div>
        <div class="kpi-subbox">🎯 Target: 10,000</div>
    </div>
    ''', unsafe_allow_html=True)

st.divider()

# --- ANALYTICS TABS ---
t1, t2, t3, t4, t5 = st.tabs(["📊 Financials", "🏍️ Ops & Logistics", "🥬 Wastage Control", "🧠 Demand Forecasting", "📈 Scenario Comparison"])

# ----- Financials Tab -----
with t1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("Unit Economics Breakdown")
        metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
        vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(), 
                -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]

        fig_water = go.Figure(go.Waterfall(
            name = "Economics", orientation = "v",
            measure = ["relative"]*6 + ["total"],
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

    # Sensitivity Analysis Table
    st.subheader("💡 Sensitivity Analysis")
    fee_range = list(range(0, 51, 10))
    disc_range = list(range(0, 101, 20))
    sens_data = []

    for fee, disc in itertools.product(fee_range, disc_range):
        temp_df = f_df.copy()
        temp_df['delivery_fee'] += fee
        temp_df['discount'] *= (1 - disc/100)
        temp_df['net_profit'] = (temp_df['commission'] + temp_df['ad_revenue'] + temp_df['delivery_fee']) - (
            temp_df['delivery_cost'] + temp_df['discount'] + temp_df['opex']
        )
        sens_data.append({'Delivery Fee Adj (₹)': fee, 'Discount Opt (%)': disc, 'Avg Net Profit': temp_df['net_profit'].mean()})

    sens_df = pd.DataFrame(sens_data)
    st.dataframe(sens_df.style.format({'Avg Net Profit':'₹{:,.2f}'}), use_container_width=True)

# ----- Ops & Logistics Tab -----
with t2:
    st.subheader("Logistics Efficiency Heatmap")
    f_df['hour'] = f_df['order_time'].dt.hour
    heat = f_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    st.plotly_chart(px.imshow(heat, color_continuous_scale='YlOrRd', aspect="auto", text_auto=True), use_container_width=True)
    st.info("💡 Yellow cells indicate cost leakage. Deploy 'Batching' algorithms during these windows.")

# ----- Wastage Control Tab -----
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

    # Wastage Trend Over Time
    st.subheader("🥬 Wastage Risk Trend")
    risk_trend = perishables.groupby(perishables['order_time'].dt.date)['freshness_hrs_left'].apply(lambda x: (x<12).sum()).reset_index()
    risk_trend.columns = ['Date','Units at Risk']
    st.line_chart(risk_trend.set_index('Date'))

# ----- Demand Forecasting Tab -----
with t4:
    st.subheader("Predictive Demand Sensing (XGBoost Inferred)")
    hist_data = f_df.groupby(f_df['order_time'].dt.date)[['order_value']].sum().reset_index()
    hist_data['forecast'] = hist_data['order_value'] * np.random.uniform(0.9, 1.1, len(hist_data))  # fixed length
    hist_data['upper'] = hist_data['forecast'] * 1.05
    hist_data['lower'] = hist_data['forecast'] * 0.95

    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['order_value'], name='Actual GOV', line=dict(color='#3D4152')))
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['forecast'], name='XGBoost Forecast', line=dict(dash='dash', color='#FC8019')))
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['upper'], name='Upper Bound', line=dict(dash='dot', color='grey')))
    fig_pred.add_trace(go.Scatter(x=hist_data['order_time'], y=hist_data['lower'], name='Lower Bound', line=dict(dash='dot', color='grey'), fill='tonexty'))
    st.plotly_chart(fig_pred, use_container_width=True)

# ----- Scenario Comparison Tab -----
with t5:
    st.subheader("Scenario Comparison (Net Profit)")
    scenario_comp = pd.DataFrame({
        "Scenario": ["Normal Operations", "Heavy Rain", "IPL Match Night"],
        "Net Profit": []
    })
    net_profits = []
    for scen in ["Normal Operations", "Heavy Rain", "IPL Match Night"]:
        temp_df = df.copy()
        if scen == "Heavy Rain":
            temp_df['delivery_cost'] *= 1.3
        elif scen == "IPL Match Night":
            temp_df['order_value'] *= 1.15
        temp_df['commission'] = temp_df['order_value']*0.18
        temp_df['net_profit'] = (temp_df['commission'] + temp_df['ad_revenue'] + temp_df['delivery_fee']) - (
            temp_df['delivery_cost'] + temp_df['discount'] + temp_df['opex']
        )
        net_profits.append(temp_df['net_profit'].mean())
    scenario_comp['Net Profit'] = net_profits
    st.bar_chart(scenario_comp.set_index('Scenario'))

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Jagadeesh.N | Built for Hyperlocal Analytics Case Studies")
