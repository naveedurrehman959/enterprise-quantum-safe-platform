FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/naveedurrehman959/enterprise-quantum-safe-platform"

WORKDIR /app

# Update Debian packages
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Create non-root application user
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home appuser

# Install Python dependencies
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    setuptools \
    wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Application ownership
RUN chown -R appuser:appgroup /app

# Run as non-root
USER appuser
 

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--chdir", "/app", "wsgi:app"]
