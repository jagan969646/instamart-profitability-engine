import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the generated data
try:
    df = pd.read_csv('swiggy_simulated_data.csv')
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Error: Run the data generation script first!")

# Set a professional style
sns.set_theme(style="whitegrid")
swiggy_orange = "#fc8019"

# Create a multi-panel figure for the Executive Summary
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Instamart Strategic Insights: Phase 2 Analysis', fontsize=20, fontweight='bold')

# --- PLOT 1: The Hourly Demand (Identifying Dead Zones) ---
hourly_counts = df.groupby('hour')['order_id'].count()
sns.lineplot(ax=axes[0, 0], x=hourly_counts.index, y=hourly_counts.values, marker='o', color=swiggy_orange, linewidth=2.5)
axes[0, 0].axvspan(14, 17, color='gray', alpha=0.2, label='Dead Zone (2PM-5PM)')
axes[0, 0].set_title('Hourly Order Volume: Underutilized Slots', fontsize=14)
axes[0, 0].set_xlabel('Hour of Day')
axes[0, 0].set_ylabel('Total Orders')
axes[0, 0].legend()

# --- PLOT 2: Contribution Margin by Zone (The Profitability Map) ---
zone_margin = df.groupby('zone')['contribution_margin'].mean().sort_values()
sns.barplot(ax=axes[0, 1], x=zone_margin.values, y=zone_margin.index, palette='RdYlGn')
axes[0, 1].set_title('Average Contribution Margin per Zone', fontsize=14)
axes[0, 1].set_xlabel('Mean Margin (₹)')

# --- PLOT 3: Weather Impact on Delivery Speed & Cost ---
weather_impact = df.groupby('weather').agg({'delivery_time_mins': 'mean', 'delivery_cost': 'mean'}).reset_index()
sns.barplot(ax=axes[1, 0], data=weather_impact, x='weather', y='delivery_time_mins', palette='Blues_d')
axes[1, 0].set_title('Impact of Weather on Delivery Speed (SLA Risk)', fontsize=14)
axes[1, 0].set_ylabel('Avg Delivery Time (mins)')

# --- PLOT 4: Perishable Risk (Freshness Life Left) ---
# Highlighting the urgency for Module A (Zero-Waste Intelligence)
perishables = df[df['category'] == 'Perishable']
sns.histplot(ax=axes[1, 1], data=perishables, x='freshness_hrs_left', bins=15, color='teal', kde=True)
axes[1, 1].set_title('Freshness Distribution of Perishables (Waste Risk)', fontsize=14)
axes[1, 1].set_xlabel('Hours of Life Remaining')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# --- Print Business Statistics for your Resume ---
print("\n--- STRATEGIC BUSINESS METRICS ---")
print(f"Overall Avg Contribution Margin: ₹{df['contribution_margin'].mean():.2f}")
print(f"Rainy Day Margin Erosion: ₹{df[df['weather']=='Clear']['contribution_margin'].mean() - df[df['weather']=='Rainy']['contribution_margin'].mean():.2f} drop per order")
print(f"Potential Waste: {len(df[(df['category']=='Perishable') & (df['freshness_hrs_left'] < 12)])} orders have <12hrs freshness left.")