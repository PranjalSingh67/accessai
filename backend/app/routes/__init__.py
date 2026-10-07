"""Routes package for AccessAI."""

from app.routes.text import router as text_router
from app.routes.digital_service import router as digital_service_router
from app.routes.image import router as image_router
from app.routes.audio import router as audio_router
from app.routes.system import router as system_router

__all__ = [
    'text_router',
    'digital_service_router',
    'image_router',
    'audio_router',
    'system_router'
]
