# ==============================
# Stage 1: Build dependencies
# ==============================
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==============================
# Stage 2: Production image
# ==============================
FROM python:3.12-slim

# Install runtime PostgreSQL client lib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r django && useradd -r -g django -d /app -s /sbin/nologin django

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy project source
COPY . .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && chown -R django:django /app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Switch to non-root user
USER django

# Expose Gunicorn port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
