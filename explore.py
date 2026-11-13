import pandas as pd

df = pd.read_csv("raw_readings.csv", parse_dates=["reading_time"])

print("shape:", df.shape)
print("missing values:")
print(df.isna().sum())
print("duplicate rows:", df.duplicated().sum())
print("sorted by time:", df["reading_time"].is_monotonic_increasing)
print(df["temperature"].describe())