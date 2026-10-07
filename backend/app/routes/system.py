"""Health check and system routes."""

from fastapi import APIRouter
from app.config import APP_NAME, APP_ENV
from app.models.schemas import HealthCheckResponse

router = APIRouter(prefix='/api/v1', tags=['system'])


@router.get('/health', response_model=HealthCheckResponse)
def health_check():
    """Check API health status."""
    return {
        'status': 'ok',
        'service': APP_NAME,
        'version': '0.1.0'
    }


@router.get('/info')
def api_info():
    """Get API information."""
    return {
        'name': APP_NAME,
        'version': '0.1.0',
        'environment': APP_ENV,
        'description': 'AI-powered accessibility assistant for digital information',
        'endpoints': {
            'text': '/api/v1/text',
            'digital_service': '/api/v1/digital-service',
            'image': '/api/v1/image',
            'audio': '/api/v1/audio',
            'health': '/api/v1/health'
        }
    }
