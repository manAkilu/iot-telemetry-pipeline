import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

SENSOR_IDS = ["A", "B", "C"]
START = "2026-11-13 00:00"
N_READINGS = 288  # 24 hours at one reading every 5 minutes


def make_clean_readings():
    timestamps = pd.date_range(START, periods=N_READINGS, freq="5min")
    frames = []
    for sensor_id in SENSOR_IDS:
        base = rng.uniform(20, 30)  # each sensor has its own typical temperature
        noise = rng.normal(0, 0.5, N_READINGS)
        frames.append(pd.DataFrame({
            "sensor_id": sensor_id,
            "reading_time": timestamps,
            "temperature": base + noise,
        }))
    return pd.concat(frames, ignore_index=True)


def add_mess(df):
    # TODO 1: spikes
    spike_rows = rng.choice(df.index, size=int(len(df) * 0.01), replace=False)
    df.loc[spike_rows, "temperature"] += 15

    # TODO 2: duplicate about 2% of the rows
    dupes = df.sample(frac=0.02, random_state=42)
    df = pd.concat([df, dupes], ignore_index=True)

    # TODO 3: set about 2% of temperatures to NaN (missing values)
    nan_indices = df.sample(frac=0.02, random_state=7).index
    df.loc[nan_indices, "temperature"] = np.nan

    # TODO 4: drop about 3% of rows (missing timestamps)
    drop_rows = rng.choice(df.index, size=int(len(df) * 0.03), replace=False)
    df = df.drop(index=drop_rows)

    # TODO 5: shuffle the rows so they arrive out of order
    df = df.sample(frac=1, random_state=42)
    return df

if __name__ == "__main__":
    df = add_mess(make_clean_readings())
    df.to_csv("raw_readings.csv", index=False)
    print(df.shape)
    print(df.head())