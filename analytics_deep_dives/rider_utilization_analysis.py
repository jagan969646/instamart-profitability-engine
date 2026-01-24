import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
df = pd.read_csv('swiggy_simulated_data.csv')
df['order_time'] = pd.to_datetime(df['order_time'])
df['hour'] = df['order_time'].dt.hour

# 2. Define Supply (Rider Capacity)
# Let's assume each zone has a fixed fleet size for this simulation
# In reality, Swiggy scales this, but we want to find the "Stress Points"
FLEET_SIZE_PER_ZONE = 15 
ORDERS_PER_RIDER_PER_HOUR = 2 # Swiggy's target is often ~2.4

# 3. Calculate Hourly Demand vs Supply Capacity
hourly_zone_demand = df.groupby(['zone', 'hour']).size().reset_index(name='order_count')
hourly_zone_demand['rider_capacity'] = FLEET_SIZE_PER_ZONE * ORDERS_PER_RIDER_PER_HOUR

# 4. Calculate Key Metrics:
# Idle Riders: Supply > Demand
# Deficit (Late Delivery Risk): Demand > Supply
hourly_zone_demand['utilization_pct'] = (hourly_zone_demand['order_count'] / hourly_zone_demand['rider_capacity']) * 100
hourly_zone_demand['status'] = np.where(hourly_zone_demand['utilization_pct'] > 100, 'Understaffed', 
                                        np.where(hourly_zone_demand['utilization_pct'] < 40, 'Idle (Loss)', 'Optimal'))

# 5. Visualize the "Heatmap of Inefficiency"
pivot_util = hourly_zone_demand.pivot(index='zone', columns='hour', values='utilization_pct')

plt.figure(figsize=(14, 7))
sns.heatmap(pivot_util, cmap='RdYlGn_r', annot=False, cbar_kws={'label': 'Utilization %'})
plt.title('Hyperlocal Rider Utilization Heatmap (Red = Overloaded | Green = Idle)', fontsize=15)
plt.xlabel('Hour of Day')
plt.ylabel('Dark Store Zone')
plt.show()

# 6. Cost Impact Calculation (Business Logic)
idle_hours = hourly_zone_demand[hourly_zone_demand['status'] == 'Idle (Loss)']
print(f"Operational Alert: Identified {len(idle_hours)} idle zone-hour slots.")
print("Recommendation: Trigger 'Scheduled Savings' (Module B) during these slots to improve recovery.")