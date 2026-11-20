FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY simulate_sensors.py clean_readings.py evaluate_spikes.py ./

RUN mkdir -p /output

CMD ["sh", "-c", "cd /output && python /app/simulate_sensors.py && python /app/clean_readings.py && python /app/evaluate_spikes.py"]