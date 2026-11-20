FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY simulate_sensors.py clean_readings.py evaluate_spikes.py ./

CMD ["sh", "-c", "python simulate_sensors.py && python clean_readings.py && python evaluate_spikes.py"]