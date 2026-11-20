# Progress Log

Study log for my 12-week data engineering plan. Project: IoT telemetry pipeline.

## 8 Nov (Day 1)
- Installed and checked Python 3.13, Git and VS Code
- Created the GitHub repo with README and .gitignore
- Set up Git name and email

## 9 to 10 Nov
- Finished the Intro to SQL tutorial
- Solved 3 easy DataLemur problems
- Continued the WorldQuant data science course (capped at about 1 hour a day)

## 11 Nov
- Signed up for Databricks Free Edition and verified my account
- Practised window functions: LAG, LEAD, ROW_NUMBER, RANK, DENSE_RANK
- Practised running totals and moving averages
- Latest row per group pattern with ROW_NUMBER and a CTE

## 12 Nov
- Practised self-joins, left joins and gap detection (ON versus WHERE with a left join)
- Practised INSERT, UPDATE, DELETE and DESCRIBE HISTORY in Databricks
- Read about star schemas: fact tables hold measurements and foreign keys, dimension tables describe the who, what and where
- Compared MySQL and PostgreSQL versions of a DataLemur problem (CASE WHEN versus FILTER)
- Self-test done: moving average, change from previous reading, latest reading per sensor

## 13 Nov
- Set up a .venv with pandas and polars
- Recreated my SQL queries in pandas (groupby, shift, rolling)
- Wrote simulate_sensors.py: spikes, duplicates, missing values, dropped rows and shuffling
- Checked the output with explore.py (855 rows, 18 missing, 13 duplicates, unsorted)
- Added raw_readings.csv and .vscode to .gitignore
- Started clean_readings.py (duplicates and sorting)

## 16 Nov
- Finished the cleaning steps in clean_readings.py: kept the best duplicate (sorted so a real value comes before NaN), interpolated the 16 missing temperatures per sensor and flagged them in temperature_imputed
- Wrote spike detection: rolling z-score (against the previous readings) and rolling median with MAD
- Wrote evaluate_spikes.py, which compares the flags with spike_truth.csv and prints precision, recall and F1
- First result on seed 42: all spikes found by MAD, z-score missed 3

## 17 Nov
- Tested the detectors on three more seeds (7, 1 and 2) without changing any thresholds
- Set the seed back to 42 and checked that the original results are reproduced

## 18 Nov
- Added handle_spikes: keeps the previous reading in temperature_before_spike_fix, flags a spike where both detectors agree, blanks those readings and interpolates them per sensor
- Seed 42: 5 spikes replaced, maximum temperature fell from 43.1 to 42.9, because the 3 spikes the z-score misses are left in
- Committed the evaluation work and stopped tracking generated files (spike_truth.csv, raw_readings.csv)
- Added find_missing_timestamps: builds the full 5-minute grid per sensor and compares it with the readings that exist
- Result on seed 42: 24 readings never arrived (A 12, B 4, C 8). 840 rows + 24 missing = 864, which is 3 sensors x 288 readings
- Decision: the gaps are reported, not filled, because filling them would invent readings that never existed. Short gaps could be interpolated later and flagged
- Added save_outputs: the cleaned data goes to clean_readings.csv (840 rows) and the gaps to missing_timestamps.csv (24 rows)
- Rewrote the README with the results, limits and run instructions

## 20 Nov
- Pushed the cleaned-data and README commit to GitHub and checked the repo page
- Tidied this log
- Stage 1 of the project (raw data to clean data) is finished

## Spike detection results

Settings: window 12, z-score threshold 4.0 (needs at least 3 earlier readings), MAD threshold 5.0 (centred window, median needs at least 6 readings, MAD at least 3), spikes of +15 degrees on about 1% of rows. Each cell is precision / recall.

| Method | Seed 42 | Seed 7 | Seed 1 | Seed 2 | Average precision | Average recall |
|---|---|---|---|---|---|---|
| z-score | 62.5% / 62.5% | 77.8% / 100% | 77.8% / 87.5% | 72.7% / 100% | 72.7% | 87.5% |
| MAD | 80.0% / 100% | 53.8% / 100% | 72.7% / 100% | 80.0% / 100% | 71.6% | 100% |
| both agree | 100% / 62.5% | 100% / 100% | 87.5% / 87.5% | 88.9% / 100% | 94.1% | 87.5% |

What I learned:
- MAD found every spike on all four seeds, but about 3 in 10 of its flags were false alarms.
- The z-score missed spikes when two spikes landed close together on one sensor. The earlier spike inflated the standard deviation and hid the next one (masking).
- Requiring both methods to agree gave the fewest false alarms (at most one per run) but sometimes missed spikes.
- After seed 42 alone I thought MAD was the best choice. Testing more seeds showed that was because I had tuned on that data.

Decision: use "both agree" as the spike flag, because false alarms trigger unnecessary checks. If missing a fault were the bigger problem, I would use MAD alone.

Limits:
- Only 31 spikes across four runs, so the percentages are noisy.
- Every spike is a large +15 degrees. Real faults are subtler, so these scores are probably optimistic.
- I tuned the thresholds on seed 42, then tested on three other seeds.

## Lessons learned
- Save the file before running it. Most "it did not work" moments were unsaved files.
- Python code goes in the editor and runs with `python file.py`. The terminal is for commands.
- Assign results back (`df = df.drop(...)`), or the change is lost.
- A condition in a left join's ON clause and one in WHERE give different results.
- `.gitignore` does not stop tracking files already committed. Use `git rm --cached <path>`.
- Deduplicate on the business key (sensor and time), and decide which duplicate to keep.
- Flag values before filling them, so I always know which ones are real.
- A trailing window that includes an earlier outlier can hide the next one. Median and MAD resist this.
- Tune on one dataset and test on others before trusting a result.
- Change one parameter at a time, or I cannot tell which change helped.

## 20 Nov
- Installed Docker Desktop and checked it with hello-world
- Wrote requirements.txt, .dockerignore and a Dockerfile
- Built the image and ran the whole pipeline in a container. The output matched my Mac run exactly (840 rows, 5 spikes replaced, 24 missing timestamps, same precision and recall)