import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Instamart Strategy Portal",
    page_icon="🧡",
    layout="wide",
)

# --- CUSTOM EXECUTIVE STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    /* KPI background style - Swiggy Orange with White Text */
    .kpi-metric {
        background-color: #FC8019 !important; 
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(252, 128, 25, 0.2);
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    /* Label inside the KPI box */
    .kpi-label {
        font-size: 0.9rem;
        color: #ffffff !important; 
        opacity: 0.9;
        font-weight: 400;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    h1, h2, h3 {
        color: #3D4152;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_text = st.columns([1, 5])

with col_logo:
    # Ensuring we look for Logo.png
    try:
        st.image("Logo.png", width=120) 
    except:
        st.subheader(":orange[SWIGGY]")

with col_text:
    st.title("Instamart Strategic Decision Engine")
    st.markdown("#### 🚀 Target: Positive Contribution Margin by June 2026")

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

# --- SIDEBAR FILTERS ---
st.sidebar.header("Hyperlocal Filters")
selected_zones = st.sidebar.multiselect("Select Target Zones", options=df['zone'].unique(), default=df['zone'].unique())
weather_filter = st.sidebar.multiselect("Weather Condition", options=df['weather'].unique(), default=df['weather'].unique())

filtered_df = df[(df['zone'].isin(selected_zones)) & (df['weather'].isin(weather_filter))]

# --- KPI ROW ---
total_gov = filtered_df['order_value'].sum()
avg_cm = filtered_df['net_profit'].mean()
burn_rate = (filtered_df['discount'].sum() / total_gov) * 100

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f'<div class="kpi-metric">₹{total_gov/1000000:.2f}M<br><span class="kpi-label">Total GOV</span></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="kpi-metric">₹{avg_cm:.2f}<br><span class="kpi-label">Avg Net Profit/Order</span></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="kpi-metric">{burn_rate:.1f}%<br><span class="kpi-label">Discount Burn Rate</span></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="kpi-metric">{len(filtered_df):,}<br><span class="kpi-label">Orders Modeled</span></div>', unsafe_allow_html=True)

st.divider()

# --- STRATEGIC VISUALS ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader(" Hyperlocal Contribution Margin (CM) Analysis")
    zone_data = filtered_df.groupby('zone')['net_profit'].mean().reset_index().sort_values('net_profit')
    fig_zone = px.bar(
        zone_data, x='net_profit', y='zone', 
        orientation='h', 
        color='net_profit',
        color_continuous_scale='RdYlGn',
        template="simple_white"
    )
    st.plotly_chart(fig_zone, use_container_width=True)

with row2_col2:
    st.subheader(" Peak vs. Non-Peak Operational Efficiency")
    hourly_vol = filtered_df.groupby('hour').size().reset_index(name='orders')
    fig_hour = px.area(
        hourly_vol, x='hour', y='orders',
        color_discrete_sequence=['#fc8019'],
        template="simple_white"
    )
    
    # Highlight Dead Zone - Now targeting both Module A & B
    fig_hour.add_vrect(
        x0=14, x1=17, 
        fillcolor="#60B246", 
        opacity=0.2, 
        annotation_text="🎯 STRATEGIC TARGET<br>Module A (Waste Clearance)<br>Module B (Scheduled Savings)",
        annotation_position="top left"
    )
    st.plotly_chart(fig_hour, use_container_width=True)

# --- MODULE A: PERISHABLE DECAY ALERT ---
st.divider()
st.subheader("Inventory Salvage & Revenue Recovery Engine")
perishables = filtered_df[filtered_df['category'] == 'Perishable']
high_risk = perishables[perishables['freshness_hrs_left'] < 12]

col_a1, col_a2 = st.columns([2, 1])

with col_a1:
    fig_decay = px.histogram(perishables, x='freshness_hrs_left', color_discrete_sequence=['#60B246'], nbins=30)
    fig_decay.update_layout(title="Freshness Distribution (Hours Left)")
    st.plotly_chart(fig_decay, use_container_width=True)

with col_a2:
    st.warning(f"**Action Required:** {len(high_risk)} units in {selected_zones} have <12 hours shelf life.")
    if st.button("🚀 Trigger 'Flash Deals' for High-Risk SKU"):
        st.success("Module A: Push notifications sent to 1,240 nearby users.")

st.markdown("---")
st.caption("Developed by Jagadeesh.N | Instamart Decision Intelligence")

(i want to add the logo which is in the same dictionary)

