FROM python:3.12-slim

LABEL maintainer="Team Parallax"
LABEL description="Parallax — AI Co-Pilots That See Work From Every Angle"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default: run the API server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
