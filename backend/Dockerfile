FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/naveedurrehman959/enterprise-quantum-safe-platform"

WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5001


CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--chdir", "/app", "wsgi:app"]
