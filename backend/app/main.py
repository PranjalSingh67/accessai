"""AccessAI FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import APP_NAME, APP_ENV, CORS_ORIGINS
from app.routes import (
    text_router,
    digital_service_router,
    image_router,
    audio_router,
    system_router
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI instance
    """
    app = FastAPI(
        title=APP_NAME,
        version='0.1.0',
        description='AI-powered accessibility assistant for everyday digital services'
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Include routers
    app.include_router(system_router)
    app.include_router(text_router)
    app.include_router(digital_service_router)
    app.include_router(image_router)
    app.include_router(audio_router)

    # Global exception handler
    @app.exception_handler(400)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={'detail': 'Invalid request. Please check your input.'}
        )

    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={'detail': 'Endpoint not found.'}
        )

    @app.exception_handler(500)
    async def server_error_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={'detail': 'Internal server error. Please try again later.'}
        )

    return app


app = create_app()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
