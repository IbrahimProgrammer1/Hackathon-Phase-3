FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=user src ./src
COPY --chown=user main.py .
COPY --chown=user prompts ./prompts

USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Hugging Face Spaces expect port 7860
EXPOSE 7860

# Use PORT env var (default 7860 for Hugging Face)
CMD ["python", "-c", "import os; port = int(os.getenv('PORT', '7860')); import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=port)"]
