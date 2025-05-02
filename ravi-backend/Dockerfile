# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system deps: Tesseract + Urdu pack (if you’re using Tesseract)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      tesseract-ocr tesseract-ocr-urd && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy Python dependency files
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose port
EXPOSE 8000

# By default, point at config.yaml in /app
ENV CONFIG_PATH=/app/config.yaml

# Run the uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]