import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .api import health, views
from .config import settings
from .middleware import LoggingMiddleware, MetricsMiddleware

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.APP_DEBUG
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(LoggingMiddleware)

    # Routers
    app.include_router(health.router)
    app.include_router(views.router)

    # Telemetry
    FastAPIInstrumentor.instrument_app(app)

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENVIRONMENT,
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.APP_LOG_LEVEL.lower(),
    )
