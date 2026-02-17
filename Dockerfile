FROM python:3.10-slim

LABEL maintainer="Jeferson F Silva <jeferson0993@gmail.com>"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ncbi-blast+ \
    cd-hit \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ /app/

# Create output folders
RUN mkdir -p /app/data /app/results

ENTRYPOINT ["python", "pipeline.py"]
