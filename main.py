import os
import pandas as pd
import numpy as np

# Path to 2nd_test folder
path = './data/2nd_test/2nd_test'

# Check if path exists
if not os.path.exists(path):
    print(f"❌ Error: {path} not found!")
    print("Make sure you unzipped the dataset to ./data/")
    exit()

# Get all files (excluding hidden files)
files = sorted([f for f in os.listdir(path) if not f.startswith('.')])
print(f"Found {len(files)} files to process")

data_list = []
print("Starting extraction... This takes about 2-3 minutes.")

for i, filename in enumerate(files):
    try:
        # Progress indicator
        if i % 100 == 0:
            print(f"Processing file {i}/{len(files)}...")
        
        # Read the file (tab-separated, no headers)
        df = pd.read_csv(os.path.join(path, filename), sep='\t', header=None)
        
        # NASA Set 2: Bearing 1 is the one that fails (Column 0)
        b1_data = df[0]
        
        # Calculate Features
        rms = np.sqrt(np.mean(b1_data**2))
        kurt = b1_data.kurtosis()
        mean_val = b1_data.mean()
        std_val = b1_data.std()
        max_val = b1_data.max()
        
        data_list.append({
            'time': filename,
            'file_index': i,
            'rms': rms,
            'kurtosis': kurt,
            'mean': mean_val,
            'std': std_val,
            'max': max_val
        })
        
    except Exception as e:
        print(f"⚠️ Warning: Error processing {filename}: {e}")
        continue

# Save to CSV
processed_df = pd.DataFrame(data_list)
processed_df.to_csv('processed.csv', index=False)

print(f"\n✅ Done! Processed {len(processed_df)} files")
print(f"✅ Created 'processed.csv' with {len(processed_df)} rows")
print(f"✅ Features: {list(processed_df.columns)}")
print("\nFirst few rows:")
print(processed_df.head())