FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies including Tesseract OCR
RUN apk add --no-cache \
    tesseract-ocr \
    tesseract-ocr-data-eng \
    gcc \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py models.py config.py services.py utils.py ./

# Expose the port the app runs on
EXPOSE 14924

# Command to run the application
CMD ["python", "main.py"]