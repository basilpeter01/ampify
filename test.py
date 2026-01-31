import pandas as pd
from prediction import RULPredictor

if __name__ == "__main__":
    # 1. Initialize
    predictor = RULPredictor(model_path='bearing_brain.pkl')
    
    # 2. Load the actual data to test on real values
    df = pd.read_csv('processed.csv')
    
    # 3. Test a "Near Failure" sample (near the end of the file)
    print("--- 🧪 Testing AI on Near-Failure Data ---")
    late_sample = df.iloc[950] 
    result = predictor.predict(late_sample)
    
    print(f"File Index: 950")
    print(f"Predicted RUL: {result['hours']} hours")
    print(f"Status: {result['status']}")
    print(f"Hardware Code: {result['alert_char']}")