import pandas as pd

from clean_readings import (
    load_raw,
    remove_duplicates,
    sort_readings,
    handle_missing,
    flag_spikes,
)


def precision_recall(flagged, actual):
    tp = (flagged & actual).sum()    # flagged and really a spike
    fp = (flagged & ~actual).sum()   # flagged but not a spike (false alarm)
    fn = (~flagged & actual).sum()   # a spike we missed

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return tp, fp, fn, precision, recall, f1


if __name__ == "__main__":
    df = flag_spikes(handle_missing(sort_readings(remove_duplicates(load_raw()))))
    truth = pd.read_csv("spike_truth.csv", parse_dates=["reading_time"])

    # Mark the rows that are real spikes, matching on sensor and time
    keys = ["sensor_id", "reading_time"]
    truth_keys = pd.MultiIndex.from_frame(truth[keys])
    actual = pd.Series(pd.MultiIndex.from_frame(df[keys]).isin(truth_keys), index=df.index)
    print("real spikes still in the data:", actual.sum())

    methods = {
        "z-score": df["is_spike_z"],
        "MAD": df["is_spike_mad"],
        "both agree": df["is_spike_z"] & df["is_spike_mad"],
    }

    for name, flagged in methods.items():
        tp, fp, fn, precision, recall, f1 = precision_recall(flagged, actual)
        print(
            f"{name:<11} flagged={tp + fp:>3} TP={tp:>2} FP={fp:>2} FN={fn:>2} "
            f"precision={precision:.1%} recall={recall:.1%} f1={f1:.1%}"
        )