# ==============================================================================
# Advanced AI Medical Intelligence Platform - Production Dockerfile
# ==============================================================================
FROM python:3.11-slim

# Prevent Python from writing bytecode files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies required for OpenCV, PyTorch, and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code and application files
COPY . .

# Ensure upload and XAI output directories exist
RUN mkdir -p data/uploads models/checkpoints models/xai

# Expose ports for FastAPI backend (8000) and Streamlit dashboard (8501)
EXPOSE 8000 8501

# Run backend and frontend services via honcho
CMD ["honcho", "start", "-f", "Procfile.docker"]
