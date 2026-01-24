import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Simulate A/B Test Data
# Group A: Control (Current ₹100 discount)
# Group B: Treatment (New ₹50 discount)
np.random.seed(42)
n_users = 1000

group_a_conversions = np.random.binomial(1, 0.12, n_users) # 12% conversion
group_b_conversions = np.random.binomial(1, 0.10, n_users) # 10% conversion (slight drop)

# 2. Statistical Significance (Chi-Square Test)
# We want to know if the 2% drop is "Real" or just "Noise"
contingency_table = [
    [sum(group_a_conversions), n_users - sum(group_a_conversions)],
    [sum(group_b_conversions), n_users - sum(group_b_conversions)]
]

chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

# 3. Unit Economics impact
avg_order_val = 500
margin_a = (avg_order_val * 0.20) - 100  # Revenue - Discount
margin_b = (avg_order_val * 0.20) - 50   # Revenue - Discount

total_profit_a = sum(group_a_conversions) * margin_a
total_profit_b = sum(group_b_conversions) * margin_b

# --- Results Presentation ---
print(f"--- A/B Test Results: Discount Reduction ---")
print(f"Group A (Control) Conversion: {group_a_conversions.mean()*100:.1f}%")
print(f"Group B (Treatment) Conversion: {group_b_conversions.mean()*100:.1f}%")
print(f"P-Value: {p_value:.4f}")

if p_value < 0.05:
    print("RESULT: Statistically Significant. The drop in orders is real.")
else:
    print("RESULT: Not Significant. The drop might be due to chance.")

print(f"\nTotal Profit A: ₹{total_profit_a}")
print(f"Total Profit B: ₹{total_profit_b}")
print(f"Strategy Recommendation: {'Implement Group B' if total_profit_b > total_profit_a else 'Keep Group A'}")