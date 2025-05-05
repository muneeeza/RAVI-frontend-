FROM pytorch/pytorch:2.2.1-cuda11.8-cudnn8-runtime

# Install system dependencies (Tesseract + Urdu support)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        tesseract-ocr tesseract-ocr-urd curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]