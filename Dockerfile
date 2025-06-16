# Stage 1: Build
FROM python:3.9-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.9-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy model files first (these are critical)
COPY spiral_model.keras mri_classifier.keras ./

# Copy application files
COPY . .

# Create uploads and static directories
RUN mkdir -p uploads static

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV TF_CPP_MIN_LOG_LEVEL=2

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 