import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# 1. Load your processed data
df = pd.read_csv('processed_multi.csv')

# 2. Add the "Answer Key" (RUL)
# We count down from the total number of files
total_files = len(df)
df['RUL'] = total_files - df['file_index']

# 3. Select Features (X) and Target (y)
features = ['rms', 'kurtosis', 'mean', 'std', 'max', 'temperature', 'current', 'pressure']
X = df[features]
y = df['RUL']

# 4. Split data (80% for learning, 20% for testing the AI)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Initialize and Train the Random Forest
print("Training the AI brain... please wait.")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Check Accuracy
score = model.score(X_test, y_test)
print(f"✅ Training Complete! Model Accuracy: {score:.2f}")

# 7. Save the model to a file
joblib.dump(model, 'bearing_brain.pkl')
print("✅ 'bearing_brain.pkl' saved! You can now use this for your live demo.")