import pandas as pd
import numpy as np

def generate_robust_data(input_csv='processed.csv', output_csv='processed_multi.csv'):
    df = pd.read_csv(input_csv)
    total_rows = len(df)
    
    # 1. Life Progress (0.0 brand new -> 1.0 total failure)
    life_progress = np.linspace(0, 1, total_rows)
    
    # 2. Temperature: Stays steady, then spikes exponentially (Friction)
    # Physical logic: Heat builds up and stays high
    base_temp = 30.0
    # Exponential rise + correlation with vibration peaks
    temp_trend = 45 * (life_progress ** 5) 
    df['temperature'] = base_temp + temp_trend + (df['max'] * 10) + np.random.normal(0, 0.5, total_rows)
    
    # 3. Current: Motor works harder to turn a 'stiff/damaged' bearing
    base_current = 2.0
    current_load = 1.5 * (life_progress ** 3)
    df['current'] = base_current + current_load + (df['rms'] * 5) + np.random.normal(0, 0.1, total_rows)
    
    # 4. Pressure: Fluid/Lube pressure drops as seals vibrate loose
    base_pressure = 100.0
    pressure_drop = 20 * (life_progress ** 4)
    df['pressure'] = base_pressure - pressure_drop + np.random.normal(0, 1.5, total_rows)

    # 5. Labeling: Explicitly help the model identify states
    # This helps the Random Forest distinguish the 'OK' vs 'Failure' zones
    df['state_label'] = pd.cut(life_progress, bins=[0, 0.7, 0.9, 1.0], labels=[0, 1, 2]) # 0=OK, 1=Warn, 2=Fail

    df.to_csv(output_csv, index=False)
    print(f"✅ Enhanced Dataset Created: {output_csv}")

if __name__ == "__main__":
    generate_robust_data()