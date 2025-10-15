# Use an official Python base image
FROM python:3.10-slim

# Install system deps for vosk and ffmpeg (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install (cache this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port used by uvicorn
EXPOSE 8080

# Start the server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]