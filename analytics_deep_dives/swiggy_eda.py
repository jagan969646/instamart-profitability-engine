import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Swiggy-grade dataset
df = pd.read_csv('swiggy_simulated_data.csv')
df['order_time'] = pd.to_datetime(df['order_time'])
df['hour'] = df['order_time'].dt.hour

# Set Swiggy-themed aesthetics
sns.set_theme(style="whitegrid")
swiggy_orange = "#fc8019"

# --- 1. Identifying the "Dead Zones" (2 PM – 5 PM) ---
# This supports Module B: Hyperlocal Demand-Supply Arbitrage
hourly_data = df.groupby('hour')['order_id'].count().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=hourly_data, x='hour', y='order_id', color=swiggy_orange, lw=3)
plt.axvspan(14, 17, color='gray', alpha=0.2, label='Dead Zone (Underutilized Dark Stores)')
plt.title('Hourly Order Volume: Identifying Underutilized Slots', fontsize=15)
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)
plt.legend()
plt.xticks(range(0, 24))
plt.show()

# --- 2. Weather & Margin Erosion Analysis ---
# Answers: Does rain increase AOV but kill margin?
weather_analysis = df.groupby('weather').agg({
    'order_value': 'mean',
    'delivery_cost': 'mean',
    'contribution_margin': 'mean'
}).round(2)

print("--- Weather Impact on Unit Economics ---")
print(weather_analysis)

# --- 3. Perishable Waste Risk (Module A Hook) ---
# Highlighting perishables with low freshness left
perishable_risk = df[df['category'] == 'Perishable'].groupby('zone')['freshness_hrs_left'].mean().sort_values()

plt.figure(figsize=(10, 5))
perishable_risk.plot(kind='barh', color='teal')
plt.title('Average Freshness Life Remaining by Zone (Perishables)')
plt.xlabel('Hours Remaining')
plt.ylabel('Zone')
plt.show()

# --- 4. The "Hire Me" Metric: Contribution Margin by Zone ---
# Identify which areas are "discount heavy but low margin"
zone_profitability = df.groupby('zone').agg({
    'contribution_margin': 'mean',
    'discount': 'mean',
    'order_id': 'count'
}).sort_values(by='contribution_margin', ascending=False)

print("\n--- Zone-wise Profitability & Discount Strategy ---")
print(zone_profitability)