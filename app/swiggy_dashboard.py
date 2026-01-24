import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Instamart Strategy Portal",
    page_icon="🧡", 
    layout="wide",
)

# --- BRANDING CONSTANTS ---
SWIGGY_ORANGE = "#FC8019"
INSTAMART_GREEN = "#60B246"
DARK_TEXT = "#3D4152"

# --- PATH HANDLING ---
# Since files are in the same 'app' directory, we look locally
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'swiggy_simulated_data.csv')

# --- CUSTOM CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #fcfcfc; }}
    .kpi-metric {{
        background-color: {SWIGGY_ORANGE} !important; 
        color: white !important;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(252, 128, 25, 0.15);
    }}
    .kpi-label {{ font-size: 0.9rem; opacity: 0.9; font-weight: 400; }}
    .kpi-value {{ font-size: 1.8rem; font-weight: 700; margin: 0; }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    # Use a high-quality emoji fallback if Logo.png isn't present
    st.markdown(f"<h1 style='font-size: 80px; margin:0; text-align:center;'>🧡</h1>", unsafe_allow_html=True)

with col_text:
    st.markdown(f"<h1 style='color:{DARK_TEXT}; margin-bottom:0;'>Instamart Strategic Decision Engine</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{INSTAMART_GREEN};'>🚀 Goal: Positive Contribution Margin 2026</h4>", unsafe_allow_html=True)

st.divider()

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing CSV at {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    # Financial Logic
    df['revenue'] = df['order_value'] * 0.20
    df['net_profit'] = df['revenue'] - df['delivery_cost'] - df['discount']
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("Hyperlocal Filters")
zones = st.sidebar.multiselect("Select Delivery Zones", options=df['zone'].unique(), default=df['zone'].unique())
filtered_df = df[df['zone'].isin(zones)]

# --- KPI ROW ---
t_gov = filtered_df['order_value'].sum()
avg_p = filtered_df['net_profit'].mean()
burn = (filtered_df['discount'].sum() / t_gov * 100) if t_gov > 0 else 0

k1, k2, k3, k4 = st.columns(4)
metrics = [
    (f"₹{t_gov/1e6:.2f}M", "Total GOV"),
    (f"₹{avg_p:.2f}", "Profit/Order"),
    (f"{burn:.1f}%", "Burn Rate"),
    (f"{len(filtered_df):,}", "Total Orders")
]

for col, (val, label) in zip([k1, k2, k3, k4], metrics):
    col.markdown(f"""
        <div class="kpi-metric">
            <p class="kpi-value">{val}</p>
            <p class="kpi-label">{label}</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- MATCHED COLOR CHARTS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📍 Profitability by Zone")
    zone_stats = filtered_df.groupby('zone')['net_profit'].mean().reset_index().sort_values('net_profit')
    fig_zone = px.bar(
        zone_stats, x='net_profit', y='zone', 
        orientation='h',
        color_discrete_sequence=[SWIGGY_ORANGE], # Matching heart color
        template="plotly_white"
    )
    st.plotly_chart(fig_zone, use_container_width=True)

with c2:
    st.subheader("⏰ Order Velocity")
    hourly = filtered_df.groupby('hour').size().reset_index(name='orders')
    fig_hour = px.area(
        hourly, x='hour', y='orders',
        color_discrete_sequence=[INSTAMART_GREEN], # Swiggy's secondary green
        template="plotly_white"
    )
    fig_hour.add_vrect(x0=14, x1=17, fillcolor=SWIGGY_ORANGE, opacity=0.1, 
                       annotation_text="OFF-PEAK TARGET", annotation_position="top left")
    st.plotly_chart(fig_hour, use_container_width=True)

st.markdown("---")
st.caption("Developed by Jagadeesh.N | Instamart Decision Intelligence")
