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
LOGO_PATH = os.path.join(BASE_DIR, "Logo.png")
SWIGGY_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png"

# --- CUSTOM EXECUTIVE STYLING ---
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

    .kpi-metric {
        background-color: #FC8019;
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(252, 128, 25, 0.2);
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .kpi-label {
        font-size: 0.9rem;
        color: #ffffff;
        opacity: 0.9;
        font-weight: 500;
    }

     [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #3D4152;
    }

    /* Customizing Headings */
    h1, h2, h3 { color: #3D4152; }
</style>
""", unsafe_allow_html=True)


# --- KPI CARD FUNCTION ---
def kpi_card(title, value):
    return f"""
    <div class="kpi-metric">
        <div style="font-size:1.8rem; font-weight:800;">{value}</div>
        <div class="kpi-label">{title}</div>
    </div>
    """

# --- DATA ENGINE ---
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
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)
    else:
        st.image(SWIGGY_URL, width=120)

    st.title("Control Tower")

    zones = st.multiselect("Geographic Clusters", df['zone'].unique(), df['zone'].unique())

    st.divider()
    st.subheader("🛠️ Profitability Simulator")
    fee_adj = st.slider("Delivery Fee Premium (₹)", 0, 50, 5)
    disc_opt = st.slider("Discount Optimization (%)", 0, 100, 20)
    st.info("Simulating impact on Contribution Margin (CM).")

# --- SIMULATION ENGINE ---
f_df = df[df['zone'].isin(zones)].copy()
f_df['delivery_fee'] += fee_adj
f_df['discount'] *= (1 - disc_opt/100)
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

# --- EXECUTIVE KPI ROW (ORANGE BOXES) ---
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
        metrics = ['Commission', 'Ad Revenue', 'Delivery Fee', 'Delivery Cost', 'Discount', 'OPEX']
        vals = [f_df['commission'].mean(), f_df['ad_revenue'].mean(), f_df['delivery_fee'].mean(),
                -f_df['delivery_cost'].mean(), -f_df['discount'].mean(), -f_df['opex'].mean()]

        fig_water = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative"] * 6 + ["total"],
            x=metrics + ['Net Profit'],
            y=vals + [0],
            decreasing={"marker": {"color": "#EF4444"}},
            increasing={"marker": {"color": "#60B246"}},
            totals={"marker": {"color": "#FC8019"}}
        ))
        fig_water.update_layout(title="Average Unit Economics (Per Order)", template="simple_white")
        st.plotly_chart(fig_water, use_container_width=True)

    with col_b:
        st.subheader("Revenue Mix")
        rev_mix = pd.DataFrame({
            'Channel': ['Comm', 'Ads', 'Fees'],
            'Rev': [f_df['commission'].sum(), f_df['ad_revenue'].sum(), f_df['delivery_fee'].sum()]
        })
        st.plotly_chart(px.pie(rev_mix, values='Rev', names='Channel', hole=0.6),
                        use_container_width=True)

with t2:
    st.subheader("Logistics Efficiency Heatmap")
    f_df['hour'] = f_df['order_time'].dt.hour
    heat = f_df.pivot_table(index='zone', columns='hour', values='delivery_cost', aggfunc='mean')
    st.plotly_chart(px.imshow(heat, aspect="auto"), use_container_width=True)

with t3:
    st.subheader("Inventory Salvage Management")
    perishables = f_df[f_df['category'] == 'Perishable']
    risk = perishables[perishables['freshness_hrs_left'] < 12]
    st.warning(f"⚠️ {len(risk)} Units at Expiry Risk")

with t4:
    st.subheader("Predictive Demand Sensing")
    f_df['forecast'] = f_df['order_value'] * np.random.uniform(0.9, 1.1, len(f_df))
    hist = f_df.groupby(f_df['order_time'].dt.date)[['order_value', 'forecast']].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist['order_time'], y=hist['order_value'], name="Actual GOV"))
    fig.add_trace(go.Scatter(x=hist['order_time'], y=hist['forecast'], name="Forecast", line=dict(dash="dash")))
    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Jagadeesh.N | Built for Hyperlocal Analytics Case Studies")


