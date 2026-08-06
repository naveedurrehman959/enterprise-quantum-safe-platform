# backend/app/metrics/prometheus_metrics.py

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram


# ---------------------------------
# API Metrics
# ---------------------------------

API_REQUESTS = Counter(
    "enterprise_api_requests_total",
    "Total API requests"
)

API_ERRORS = Counter(
    "enterprise_api_errors_total",
    "Total API errors"
)


# ---------------------------------
# Quantum Safe Metrics
# ---------------------------------

QUANTUM_READINESS_SCORE = Gauge(
    "quantum_readiness_score",
    "Quantum readiness score"
)

TOTAL_ALGORITHMS = Gauge(
    "total_algorithms",
    "Total cryptographic algorithms"
)

SAFE_ALGORITHMS = Gauge(
    "safe_algorithms",
    "Quantum safe algorithms"
)

VULNERABLE_ALGORITHMS = Gauge(
    "vulnerable_algorithms",
    "Quantum vulnerable algorithms"
)


# ---------------------------------
# System Metrics
# ---------------------------------

CPU_USAGE = Gauge(
    "cpu_usage_percent",
    "CPU usage percentage"
)

MEMORY_USAGE = Gauge(
    "memory_usage_percent",
    "Memory usage percentage"
)

DISK_USAGE = Gauge(
    "disk_usage_percent",
    "Disk usage percentage"
)


# ---------------------------------
# Request Duration
# ---------------------------------

REQUEST_DURATION = Histogram(
    "request_duration_seconds",
    "HTTP request duration"
)
