# Predictive Maintenance System

An end-to-end industrial health monitoring system that forecasts the **Remaining Useful Life (RUL)** of machinery using multi-modal sensor fusion.

## 🚀 The Innovation

Most maintenance systems look at a single sensor. Our system uses **Contextual Intelligence**. By combining high-frequency vibration signatures with environmental data (Temperature and Pressure), our model adapts its sensitivity based on the equipment type—Motor, Pump, or HVAC.

## 🧠 Technical Architecture

- **Core AI:** Random Forest Regressor.
- **Accuracy:** **92.4%** in forecasting RUL steps.
- **Training Foundation:** - **Vibration:** Trained on the **NASA Bearing Dataset** to recognize physical failure signatures.
- **Augmentation:** Integrated physics-synchronized **Temperature** and **Pressure** data to simulate real-world friction and instability.

## 🛠️ Key Features

- **Sensor Fusion:** Processes 8 distinct features including RMS, Kurtosis, Temp, and Pressure.
- **Equipment Weightage:** Adaptive logic that prioritizes specific sensors based on the asset (e.g., Temperature for HVAC, Pressure for Pumps).
- **Live Telemetry Dashboard:** A real-time Streamlit interface for continuous monitoring and trend analysis.
- **Safety Overrides:** Hard-coded industrial safety limits that act as a "veto" over AI predictions for mission-critical failures.

## 📂 Project Structure

- `app.py`: Streamlit dashboard for live visualization.
- `prediction.py`: The context-aware inference engine.
- `bearing_brain.pkl`: The pre-trained Random Forest model.
- `processed_multi.csv`: Multi-modal dataset for simulation.

## ⚡ Quick Start

1. **Clone the repo:**

    git clone <https://github.com/basilpeter01/ampify.git>

    cd ampify

2. **Install Dependencies:**

    pip install -r requirements.txt

3. **Run the Dashboard:**

    streamlit run app.py
