import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
num_orders = 10000
zones = ['Indiranagar', 'Koramangala', 'HSR Layout', 'Whitefield', 'Jayanagar']
weather_options = ['Clear', 'Rainy', 'Cloudy']
item_categories = ['Perishable', 'Snacks', 'Home Needs', 'Beverages']

def generate_swiggy_data(n):
    data = []
    start_date = datetime(2025, 1, 1)
    
    # Define probabilities for 24 hours
    probs = np.array([0.01]*7 + [0.04]*5 + [0.03]*5 + [0.11]*5 + [0.02]*2)
    probs /= probs.sum()  # Normalize to sum exactly 1.0
    
    for i in range(n):
        order_id = 100000 + i
        
        # 1. Hyperlocal & Time Logic
        hour = int(np.random.choice(range(24), p=probs))  # cast to native int
        order_time = start_date + timedelta(
            days=random.randint(0, 30),
            hours=hour,
            minutes=random.randint(0, 59)
        )
        zone = random.choice(zones)
        
        # 2. Business Metrics Logic
        category = random.choice(item_categories)
        order_value = round(random.uniform(150, 1200), 2)
        
        # Weather impact simulation
        weather = np.random.choice(weather_options, p=[0.7, 0.15, 0.15])
        base_delivery = random.randint(10, 25)
        delivery_time = int(base_delivery + (15 if weather == 'Rainy' else 0))
        
        # 3. Unit Economics Fields
        delivery_cost = 40 + (5 if delivery_time > 30 else 0)
        discount = random.choice([0, 0, 0, 50, 100]) 
        
        # Freshness life for Module A (Decay Model)
        freshness_hrs = int(random.randint(1, 48) if category == 'Perishable' else 500)
        
        data.append([
            order_id, order_time, zone, category, order_value, 
            delivery_time, weather, delivery_cost, discount, freshness_hrs
        ])
    
    columns = [
        'order_id', 'order_time', 'zone', 'category', 'order_value', 
        'delivery_time_mins', 'weather', 'delivery_cost', 'discount', 'freshness_hrs_left'
    ]
    df = pd.DataFrame(data, columns=columns)
    
    # Phase 5 Calculation: Contribution Margin
    df['contribution_margin'] = df['order_value'] - df['delivery_cost'] - df['discount']
    
    return df

# Generate and Save
df = generate_swiggy_data(num_orders)

print("Successfully generated dataset with shape:", df.shape)
print(df.head())

# Save to CSV
df.to_csv('swiggy_simulated_data.csv', index=False)
