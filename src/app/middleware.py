import time
from collections.abc import Awaitable, Callable

import structlog
from fastapi import Request
from fastapi.responses import Response
from prometheus_client import Histogram
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)

request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        request_duration.labels(method=request.method, endpoint=request.url.path).observe(duration)

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Safely get client IP, defaulting to None if not available
        client_ip = request.client.host if request.client else None

        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            client_ip=client_ip,
        )

        try:
            response = await call_next(request)
            logger.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
            )
            return response
        except Exception as e:
            logger.error(
                "request_failed",
                method=request.method,
                path=request.url.path,
                error=str(e),
            )
            raise
