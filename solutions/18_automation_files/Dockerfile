# Reference Dockerfile for the Module 17 pipeline
FROM python:3.12-slim

WORKDIR /app

# Dependencies first: this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then the code
COPY . .

CMD ["python", "run.py", "--raw", "data/onboard_charges_raw.csv", "--guests", "data/guests.csv", "--db", "output/onboard.db", "--rejected", "output/rejected.csv"]
