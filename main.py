from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request as StarletteRequest

from src.api.v0 import create_router as create_api_router


class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: StarletteRequest, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="Lab 2",
        version="0.1.0",
        description="",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": 1,
        },
    )
    app.add_middleware(CustomCORSMiddleware)

    api_router = create_api_router()
    app.include_router(api_router, prefix="/api/v0", tags=["api", "v0"])

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="127.0.0.1", port=8000, log_level="info")
