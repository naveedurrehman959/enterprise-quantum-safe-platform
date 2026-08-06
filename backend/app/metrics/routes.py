# backend/app/metrics/routes.py

from flask import Response
from flask import Blueprint

from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

from .services import MetricsService


metrics_bp = Blueprint(
    "metrics",
    __name__
)


@metrics_bp.route(
    "/metrics",
    methods=["GET"]
)
def metrics():

    MetricsService.update_metrics()

    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

