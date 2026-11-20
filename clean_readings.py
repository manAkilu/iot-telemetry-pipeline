import pandas as pd
import numpy as np


def load_raw(path="raw_readings.csv"):
    return pd.read_csv(path, parse_dates=["reading_time"])


def remove_duplicates(df):
    # One reading per sensor per timestamp. Sort so a real value comes
    # before NaN, then keep the first row of each pair.
    df = df.sort_values(
        ["sensor_id", "reading_time", "temperature"], na_position="last"
    )
    return df.drop_duplicates(subset=["sensor_id", "reading_time"], keep="first")


def sort_readings(df):
    return df.sort_values(["sensor_id", "reading_time"]).reset_index(drop=True)


def handle_missing(df):
    # 1. Flag the rows where the temperature is missing
    df["temperature_imputed"] = df["temperature"].isna()

    # 2. Fill the gaps with linear interpolation, separately for each sensor
    df["temperature"] = df.groupby("sensor_id")["temperature"].transform(
        lambda s: s.interpolate(method="linear", limit_direction="both")
    )
    return df


def flag_spikes(df, window=12, z_threshold=4.0, mad_threshold=5.0):
    df = df.sort_values(["sensor_id", "reading_time"]).reset_index(drop=True)
    grouped = df.groupby("sensor_id")["temperature"]

    # Method 1: z-score against the previous readings only (shift(1) keeps the current row out of its own window)
    def zscore(s):
        r = s.rolling(window, min_periods=3)
        m = r.mean().shift(1)
        sd = r.std(ddof=0).shift(1)
        return (s - m) / sd

    df["z"] = grouped.transform(zscore)
    df["is_spike_z"] = df["z"].abs() > z_threshold

    # Method 2: rolling median and MAD (centred window)
    def robust_z(s):
        med = s.rolling(window, center=True, min_periods=6).median()
        mad = (s - med).abs().rolling(window, center=True, min_periods=3).median()
        return 0.6745 * (s - med) / mad

    df["robust_z"] = grouped.transform(robust_z)
    df["is_spike_mad"] = df["robust_z"].abs() > mad_threshold
    return df


def handle_spikes(df):
    # 1. Keep the original reading
    df["temperature_before_spike_fix"] = df["temperature"]

    # 2. A spike is a row that both detectors flagged
    df["is_spike"] = df["is_spike_z"] & df["is_spike_mad"]

    # 3. Blank out the spikes
    df.loc[df["is_spike"], "temperature"] = np.nan

    # 4. Fill them in again with linear interpolation, per sensor
    df["temperature"] = df.groupby("sensor_id")["temperature"].transform(
        lambda s: s.interpolate(method="linear", limit_direction="both")
    )
    return df


def find_missing_timestamps(df):
    # 1. Every 5-minute step from the first to the last reading
    grid = pd.date_range(
        df["reading_time"].min(), df["reading_time"].max(), freq="5min"
    )

    # 2. Every sensor at every step (what we expect to have)
    expected = pd.MultiIndex.from_product(
        [df["sensor_id"].unique(), grid], names=["sensor_id", "reading_time"]
    )

    # 3. The sensor/time pairs we actually have
    actual = pd.MultiIndex.from_frame(df[["sensor_id", "reading_time"]])

    # 4. Expected but not actual = missing
    missing = expected.difference(actual)
    return missing.to_frame(index=False)


def save_outputs(df, missing):
    columns = [
        'sensor_id', 'reading_time', 'temperature',
        'temperature_imputed', 'is_spike', 'temperature_before_spike_fix',
    ]
    df[columns].to_csv('clean_readings.csv', index=False)
    missing.to_csv('missing_timestamps.csv', index=False)
    

if __name__ == "__main__":
    df = load_raw()
    print("raw rows:", len(df))

    df = remove_duplicates(df)
    print("after removing duplicates:", len(df))

    df = sort_readings(df)
    print("missing before:", df["temperature"].isna().sum())

    df = handle_missing(df)
    print("missing after:", df["temperature"].isna().sum())
    print("imputed rows:", df["temperature_imputed"].sum())

    print(df.head())

    df = flag_spikes(df)
    print("z-score spikes:", df["is_spike_z"].sum())
    print("MAD spikes:", df["is_spike_mad"].sum())
    both = df["is_spike_z"] & df["is_spike_mad"]
    print("flagged by both:", both.sum())
    print("only z-score:", (df["is_spike_z"] & ~df["is_spike_mad"]).sum())
    print("only MAD:", (~df["is_spike_z"] & df["is_spike_mad"]).sum())

    flagged = df[df["is_spike_z"] | df["is_spike_mad"]]
    print(flagged[["sensor_id", "reading_time", "temperature", "z", "robust_z"]]
          .sort_values("robust_z", key=abs, ascending=False)
          .to_string())

    df = handle_spikes(df)
    print("spikes replaced:", df["is_spike"].sum())
    print("max temperature before:", df["temperature_before_spike_fix"].max())
    print("max temperature after:", df["temperature"].max())

    missing = find_missing_timestamps(df)
    print("missing timestamps:", len(missing))
    print(missing.groupby("sensor_id").size())
    print(missing.head())

    save_outputs(df, missing)
    print('saved clean_readings.csv and missing_timestamps.csv')