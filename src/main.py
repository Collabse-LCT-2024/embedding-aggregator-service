from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import events
from src.cli import cli
from src.core.config import settings
from src.core.tracing import configure_tracing
from src.dependencies.main import setup_dependencies


def create_app() -> FastAPI:
    if settings.enable_tracer:
        configure_tracing()
    app = FastAPI(
        title=settings.project_name,
        description=settings.description,
        docs_url="/api/events/openapi",
        openapi_url="/api/events/openapi.json",
        default_response_class=ORJSONResponse,
        version=settings.version
    )

    if settings.enable_tracer:

        @app.middleware("http")
        async def before_request(request: Request, call_next):
            response = await call_next(request)
            request_id = request.headers.get("X-Request-Id")
            if not request_id:
                return ORJSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"detail": "X-Request-Id is required"},
                )
            return response

        FastAPIInstrumentor.instrument_app(app)

    app.include_router(events.router, prefix="/api/v1/events", tags=["События"])

    setup_dependencies(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


@app.exception_handler(Exception)
def custom_exception_handler(_: Request, exc: Exception):
    return ORJSONResponse(content={"detail": str(exc)})


if __name__ == "__main__":
    cli()
