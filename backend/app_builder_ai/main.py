from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_builder_ai.api.routes import router
from app_builder_ai.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Agentic AI codebase generation platform with Pydantic tool validation.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name}

    app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
