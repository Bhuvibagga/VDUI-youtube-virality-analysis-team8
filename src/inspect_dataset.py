
import pandas as pd

df = pd.read_csv("data/youtube_data.csv")

print("\n========== DATASET INSPECTION ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head().to_string())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nStatistical Summary:")
print(df.describe().to_string())

print("\n========== COMPLETE ==========")
