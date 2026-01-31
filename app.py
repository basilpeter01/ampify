import streamlit as st
import pandas as pd
import numpy as np
import time
from prediction import RULPredictor

# 1. Page Configuration
st.set_page_config(page_title="IOT Dashboard", layout="wide")
st.title("Predictive Maintenance Dashboard 🛠️")

@st.cache_resource
def load_resources():
    # Loading the multi-sensor dataset and the upgraded 92% accuracy brain
    return RULPredictor(), pd.read_csv('processed_multi.csv')

predictor, df = load_resources()

# --- SIDEBAR ---
st.sidebar.title("Setup")
# Default set to index 1 ("Live Simulation") instead of 0
mode = st.sidebar.radio("Mode", ["Spot Check", "Live Simulation"], index=1)
eq_type = st.sidebar.selectbox("Equipment Type", ["Motor", "Pump", "HVAC"])

# --- EQUIPMENT DISPLAY (The "Current Selection" Button/Box) ---
# Added as a dedicated info box to show the active weightage profile
st.info(f"**Active Profile:** {eq_type} Logic | **Sensors:** Vibration, Temperature, Pressure")

# --- STATIC LAYOUT (Placeholders prevent piling up) ---
status_head = st.empty()
col1, col2 = st.columns(2)
m_rul = col1.empty()
m_health = col2.empty()

# Sensor Row (Excluding Current as requested)
s1, s2, s3 = st.columns(3)
v_metric = s1.empty()
t_metric = s2.empty()
p_metric = s3.empty()

chart_place = st.empty()

if 'history' not in st.session_state:
    st.session_state.history = []

def run_prediction(index):
    row = df.iloc[index]
    # Passes the chosen equipment type to the weightage engine
    res = predictor.predict(row, eq_type=eq_type)
    
    # 1. Update Status Header
    status_head.markdown(f"## System Health: :{res['color']}[{res['status']}]")
    
    # 2. Update Primary Metrics
    m_rul.metric("Predicted RUL", f"{res['hours']} Hours")
    # Health score logic normalized to a 150-hour scale
    health_val = min(100, int((res['hours']/150)*100))
    m_health.metric("Health Score", f"{health_val}%", delta=f"{eq_type} Mode")

    # 3. Update Sensor Details
    v_metric.metric("Vibration (RMS)", f"{row['rms']:.4f}")
    t_metric.metric("Temp (°C)", f"{row['temperature']:.1f}")
    p_metric.metric("Pressure (PSI)", f"{row['pressure']:.1f}")

    # 4. Update Trend Chart
    st.session_state.history.append(res['hours'])
    if len(st.session_state.history) > 30: 
        st.session_state.history.pop(0)
    chart_place.line_chart(st.session_state.history)

# --- EXECUTION ---
if mode == "Spot Check":
    if st.sidebar.button("Predict"):
        run_prediction(np.random.randint(0, len(df)))
else:
    # This loop now runs automatically on app start
    while True:
        run_prediction(np.random.randint(0, len(df)))
        time.sleep(1.2)