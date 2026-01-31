import joblib
import pandas as pd

class RULPredictor:
    def __init__(self, model_path='bearing_brain.pkl'):
        self.model = joblib.load(model_path)
        # The model still expects 8 features from the last training
        self.feature_names = ['rms', 'kurtosis', 'mean', 'std', 'max', 'temperature', 'current', 'pressure']
        
        # New weightage profiles (Current excluded from logic)
        self.profiles = {
            "Motor": {"vib": 0.8, "temp": 0.2},
            "Pump":  {"vib": 0.4, "press": 0.6},
            "HVAC":  {"temp": 0.7, "vib": 0.3}
        }

    def predict(self, row, eq_type="Motor"):
        # 1. AI Inference
        input_df = pd.DataFrame([row], columns=self.feature_names)
        raw_rul = self.model.predict(input_df)[0]
        rul_hours = raw_rul * (10 / 60)

        # 2. Manual Weightage Overrides
        if eq_type == "HVAC" and row['temperature'] > 60:
            rul_hours = min(rul_hours, 3.0) # Temp is critical for HVAC
        elif eq_type == "Pump" and row['pressure'] < 85:
            rul_hours = min(rul_hours, 5.0) # Pressure drop is critical for Pumps

        # 3. Status Mapping
        if rul_hours < 6:
            status, color = 'CRITICAL', 'red'
        elif rul_hours < 24:
            status, color = 'WARNING', 'orange'
        else:
            status, color = 'NORMAL', 'green'
            
        return {'hours': round(max(0, rul_hours), 1), 'status': status, 'color': color}