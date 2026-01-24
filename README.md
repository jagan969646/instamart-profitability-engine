# 🧡 Instamart Strategic Decision Engine
> **An End-to-End Analytics Ecosystem for Hyperlocal Unit Economics**

![Dashboard Preview](assets/dashboard_main.png) 

## 📌 Project Overview
This project simulates a high-growth environment for **Swiggy Instamart**, focusing on the "Path to Profitability." By integrating data engineering, machine learning, and business intelligence, this engine identifies operational drains and provides automated intervention strategies.

## 🚀 The 4-Pillar Architecture

### 1. Data Engineering & Simulation (`/data_pipeline`)
* **`instamart_unit_economics_gen.py`**: A custom-built simulation engine creating 10,000+ transactions with realistic constraints (Weather-impacted delivery costs, category-specific freshness decay, and hyperlocal demand variance).

### 2. Strategic Business Intelligence (`/analytics_deep_dives`)
* **`profitability_analysis.py`**: A deep-dive into "Profit Drains," identifying why specific orders result in negative contribution margins.
* **`rider_utilization_analysis.py`**: Visualizes the **"Dead Zone" (2 PM – 5 PM)** using heatmaps to identify fleet idle-time losses.
* **`swiggy_eda_visuals.py`**: Multi-panel executive summaries of zone-wise performance and SLA risks.

### 3. Predictive Modeling & Testing (`/models_and_tests`)
* **`swiggy_demand_forecast.py`**: An **XGBoost-powered** regression model predicting hourly order volume to optimize dark-store staffing.
* **`swiggy_ab_test_sim.py`**: A statistical framework using **Chi-Square tests** to measure the impact of discount reduction on user conversion vs. net margin.

### 4. Executive Command Center (`/app`)
* **`swiggy_dashboard.py`**: A high-fidelity Streamlit interface for Category Managers.
    * **Module A (Inventory Salvage):** Real-time liquidation of SKUs with <12h shelf life.
    * **Module B (Strategic Window):** Demand-shifting incentives to fill idle rider capacity.



---

## 📊 Strategic Business Metrics
| Metric | Value (Simulated) | Impact |
| :--- | :--- | :--- |
| **Total GOV** | ₹6.73M | Scale of operations across 5 zones |
| **Avg Net Profit/Order** | ₹64.39 | Current unit economic health |
| **Inventory At Risk** | 500+ Units | High-priority targets for Module A |
| **Target Utilization** | 85% | Goal for the "Dead Zone" optimization |

## 🛠 Tech Stack
* **Language:** Python 3.9+
* **Libraries:** Pandas, Numpy, Plotly, Scikit-Learn, XGBoost, Scipy, Streamlit.
* **Aesthetics:** Swiggy Brand Identity (#FC8019) & Dark-Mode Executive Styling.

## 📈 How to Run
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/Jagadeesh-N/instamart-strategic-engine.git](https://github.com/Jagadeesh-N/instamart-strategic-engine.git)
