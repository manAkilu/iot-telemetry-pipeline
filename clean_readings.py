import pandas as pd


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