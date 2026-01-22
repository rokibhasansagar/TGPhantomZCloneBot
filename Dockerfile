# Base image
FROM python:3.13-slim

# Envs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Rclone via apt (stable)
RUN apt-get update && apt-get install -y rclone \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /data/app

# Install Deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Code
COPY . .

# Run
CMD ["python", "main.py"]
