FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable real-time logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set HuggingFace cache location inside container
ENV HF_HOME=/app/cache
ENV TRANSFORMERS_CACHE=/app/cache

WORKDIR /app

# Install system dependencies needed by scientific libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (for Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch==2.10.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Pre-download embedding model so container doesn't download on startup
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-base-en-v1.5')"

# Open API port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn","backend.app:app","--host","0.0.0.0","--port","8000"]