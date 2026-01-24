import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load Data
df = pd.read_csv('swiggy_simulated_data.csv')

# 2. Refine Unit Economics (Adding Swiggy-specific business logic)
COMMISSION_RATE = 0.20  # Swiggy takes ~20% from the merchant
FIXED_PACKAGING_COST = 5

# Calculate Net Revenue and True Contribution Margin
df['commission_revenue'] = df['order_value'] * COMMISSION_RATE
df['total_cost'] = df['delivery_cost'] + df['discount'] + FIXED_PACKAGING_COST
df['net_profit'] = df['commission_revenue'] - df['total_cost']

# 3. Segmenting Orders: Profitable vs. Loss-Making
df['profit_status'] = df['net_profit'].apply(lambda x: 'Profitable' if x > 0 else 'Loss-Making')

# 4. Analysis: Why are we losing money?
loss_analysis = df.groupby('profit_status').agg({
    'order_value': 'mean',
    'discount': 'mean',
    'delivery_cost': 'mean',
    'order_id': 'count'
}).reset_index()

print("--- Profitability Segment Analysis ---")
print(loss_analysis)

# 5. Visualizing the "Profit Drain"
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df.sample(1000), x='order_value', y='net_profit', hue='profit_status', palette={'Profitable': 'green', 'Loss-Making': 'red'}, alpha=0.6)
plt.axhline(0, color='black', linestyle='--')
plt.title('Order Value vs. Net Profit (Identifying the "Break-even" Point)', fontsize=15)
plt.xlabel('Order Value (₹)')
plt.ylabel('Net Profit per Order (₹)')
plt.show()

# 6. Identifying Loss-Making Zones
zone_profit = df.groupby('zone')['net_profit'].mean().sort_values()
print("\n--- Average Profit per Order by Zone ---")
print(zone_profit)