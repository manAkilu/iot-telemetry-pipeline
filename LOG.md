# Progress Log

# Progress Log

Study log for my 12-week data engineering plan. Project: IoT telemetry pipeline.

## 8 Nov (Day 1)
- Installed and checked Python 3.13, Git and VS Code
- Created the GitHub repo with README and .gitignore
- Set up Git name and email
- Next: SQL practice sites and Databricks

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

## Lessons learned
- Python code goes in the editor and runs with `python file.py`. The terminal is for commands.
- Assign results back (`df = df.drop(...)`), or the change is lost.
- A condition in a left join's ON clause and one in WHERE give different results.
- `.gitignore` does not stop tracking files already committed. Use `git rm -r --cached <path>`.

## Next
- Finish clean_readings.py: missing values, spike detection (z-score and median/MAD), missing timestamps
- Docker basics and a compose file (week 3)
- Databricks Academy course and the bronze layer (week 4)