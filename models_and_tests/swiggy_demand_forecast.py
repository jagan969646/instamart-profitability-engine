import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# 1. Load and Resample Data
df = pd.read_csv('swiggy_simulated_data.csv')
df['order_time'] = pd.to_datetime(df['order_time'])

# Aggregate orders by hour
ts_data = df.set_index('order_time').resample('H').size().reset_index()
ts_data.columns = ['ds', 'y']

# 2. Feature Engineering (Creating 'Time' features for the model)
def create_features(df):
    df = df.copy()
    df['hour'] = df['ds'].dt.hour
    df['dayofweek'] = df['ds'].dt.dayofweek
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    return df

ts_features = create_features(ts_data)

# 3. Train/Test Split
# Using the last 48 hours as a test set
train = ts_features.iloc[:-48]
test = ts_features.iloc[-48:]

X_train = train[['hour', 'dayofweek', 'is_weekend']]
y_train = train['y']
X_test = test[['hour', 'dayofweek', 'is_weekend']]
y_test = test['y']

# 4. Build the XGBoost Model
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.01)
model.fit(X_train, y_train)

# 5. Predict and Evaluate
test['prediction'] = model.predict(X_test)
mae = mean_absolute_error(test['y'], test['prediction'])

# --- Visualizing the Forecast ---
plt.figure(figsize=(12, 6))
plt.plot(test['ds'], test['y'], label='Actual Demand', color='black', marker='o')
plt.plot(test['ds'], test['prediction'], label='Predicted Demand', color='#fc8019', linestyle='--')
plt.title(f'Phase 3: 48-Hour Demand Forecast (MAE: {mae:.2f} orders)')
plt.xlabel('Time')
plt.ylabel('Order Volume')
plt.legend()
plt.show()

print(f"Model Training Complete. Mean Absolute Error: {mae:.2f}")