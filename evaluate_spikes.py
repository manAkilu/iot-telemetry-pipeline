import pandas as pd

from clean_readings import (
    load_raw,
    remove_duplicates,
    sort_readings,
    handle_missing,
    flag_spikes,
)


def precision_recall(flagged, truth):
    # TODO: count true positives, false positives and false negatives
# Formulas
    precision_recall = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * precision * recall / (precision + recall)

# Output
print(f"{'Precision':<10} {precision:.1%}")
print(f"{'Recall':<10} {recall:.1%}")
print(f"{'F1':<10} {f1:.1%}")

if __name__ == "__main__":
    df = flag_spikes(handle_missing(sort_readings(remove_duplicates(load_raw()))))
    truth = pd.read_csv("spike_truth.csv", parse_dates=["reading_time"])

    # TODO: build the three flag columns (z-score, MAD, both agree),
    #       mark which rows are in the truth file, and print the results
    lst = [1, 2, 3, 4, 5]
flag = True

for el in lst:
	if el < 0:
		flag = False
		
print(flag) # True since all numbers are positive