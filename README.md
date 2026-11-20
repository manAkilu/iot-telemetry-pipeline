# IoT Telemetry Pipeline

A data engineering project that generates messy simulated IoT sensor data, cleans it, finds sensor faults and measures how well the fault detection works.

## What it does

1. **Simulates** three temperature sensors that report every 5 minutes for 24 hours, then adds realistic mess: sudden spikes, duplicate rows, missing values, missing timestamps and out-of-order rows.
2. **Cleans** the data: removes duplicates, fills missing temperatures per sensor, flags and replaces spikes, and lists the readings that never arrived.
3. **Evaluates** the spike detection against a known answer key, using precision and recall.

## Spike detection results

Two detectors flag spikes: a rolling z-score and a rolling median with MAD. A reading counts as a spike when both agree. Results on four random seeds (precision / recall):

| Method | Average precision | Average recall |
|---|---|---|
| z-score | 72.7% | 87.5% |
| median and MAD | 71.6% | 100% |
| both agree | 94.1% | 87.5% |

Median and MAD found every spike but raised more false alarms. The z-score sometimes missed a spike that came shortly after another one on the same sensor. Requiring both to agree gave the fewest false alarms.

**Limits:** only 31 spikes across the four runs, and every simulated spike is a large +15 degrees. Real faults are usually smaller, so these scores are probably optimistic.

## How to run it

```
python -m venv .venv
source .venv/bin/activate
pip install pandas polars
python simulate_sensors.py
python clean_readings.py
python evaluate_spikes.py
```
### Run it with Docker

```
docker build -t iot-pipeline .
docker run --rm iot-pipeline
```

This runs the simulator, the cleaning script and the evaluation in one container and prints the results. The files it creates stay inside the container.

## Files

- `simulate_sensors.py` creates `raw_readings.csv` and the answer key `spike_truth.csv`
- `clean_readings.py` cleans the data and writes `clean_readings.csv` and `missing_timestamps.csv`
- `evaluate_spikes.py` scores the spike detection
- `LOG.md` is my study log with decisions and lessons
- `Dockerfile` builds the image that runs the three scripts
- `requirements.txt` lists the Python libraries (pandas and numpy)
- `.dockerignore` keeps local files out of the image

## Status

Stage 1 (raw data to clean data) is finished. Next: Databricks bronze, silver and gold tables, then dbt, Dagster and automated tests.