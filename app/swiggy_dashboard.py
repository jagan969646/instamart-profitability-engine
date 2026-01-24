import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Instamart Strategy Portal",
    page_icon="🧡",
    layout="wide",
)

# --- SMART PATH DISCOVERY ---
def find_file(filename):
    """
    Search for the file in:
    1. The same folder as the script
    2. The data_pipeline folder relative to the script
    3. The parent folder (root)
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Possible locations
    search_paths = [
        os.path.join(script_dir, filename),                               # Same folder
        os.path.join(script_dir, 'data_pipeline', filename),              # Subfolder
        os.path.join(script_dir, '..', 'data_pipeline', filename),         # Sibling folder
        os.path.join(script_dir, '..', filename)                          # Root folder
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return path
    return None

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .kpi-metric {
        background-color: #FC8019 !important; 
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(252, 128, 25, 0.2);
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .kpi-label { font-size: 0.9rem; color: #ffffff; opacity: 0.9; font-weight: 400; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    logo_path = find_file("Logo.png")
    if logo_path:
        st.image(logo_path, width=120)
    else:
        st.subheader(":orange[SWIGGY]")

with col_text:
    st.title("Instamart Strategic Decision Engine")
    st.markdown("#### 🚀 Target: Positive Contribution Margin by June 2026")

st.divider()

# --- DATA LOADING ---
@st.cache_data
def load_data():
    file_path = find_file('swiggy_simulated_data.csv')
    if not file_path:
        raise FileNotFoundError("Could not locate swiggy_simulated_data.csv in any expected directory.")
    
    df = pd.read_csv(file_path)
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    df['revenue'] = df['order_value'] * 0.20
    df['net_profit'] = df['revenue'] - df['delivery_cost'] - df['discount']
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Critical Error: {e}")
    st.info("Check if 'swiggy_simulated_data.csv' is uploaded correctly to GitHub.")
    st.stop()

# --- FILTERS & KPIs ---
st.sidebar.header("Hyperlocal Filters")
selected_zones = st.sidebar.multiselect("Zones", options=df['zone'].unique(), default=df['zone'].unique())
filtered_df = df[df['zone'].isin(selected_zones)]

total_gov = filtered_df['order_value'].sum()
avg_cm = filtered_df['net_profit'].mean()
burn_rate = (filtered_df['discount'].sum() / total_gov) * 100 if total_gov != 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi-metric">₹{total_gov/1e6:.2f}M<br><span class="kpi-label">Total GOV</span></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi-metric">₹{avg_cm:.2f}<br><span class="kpi-label">Avg Profit/Order</span></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi-metric">{burn_rate:.1f}%<br><span class="kpi-label">Burn Rate</span></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="kpi-metric">{len(filtered_df):,}<br><span class="kpi-label">Orders</span></div>', unsafe_allow_html=True)

st.divider()

# --- CHARTS ---
c1, c2 = st.columns(2)
with c1:
    zone_data = filtered_df.groupby('zone')['net_profit'].mean().reset_index().sort_values('net_profit')
    st.plotly_chart(px.bar(zone_data, x='net_profit', y='zone', orientation='h', color='net_profit', title="Zone Profitability"), use_container_width=True)
with c2:
    hourly_vol = filtered_df.groupby('hour').size().reset_index(name='orders')
    fig_hour = px.area(hourly_vol, x='hour', y='orders', title="Peak Efficiency")
    fig_hour.add_vrect(x0=14, x1=17, fillcolor="green", opacity=0.1, annotation_text="TARGET ZONE")
    st.plotly_chart(fig_hour, use_container_width=True)

st.caption("Developed by Jagadeesh.N")

