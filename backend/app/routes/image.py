"""Routes for image analysis."""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ImageAnalysisRequest, AccessibilityResponse
from app.services.ai_service import AIService, AIProviderError

router = APIRouter(prefix='/api/v1/image', tags=['image'])
ai_service = AIService()


@router.post('/analyze', response_model=AccessibilityResponse)
def analyze_image(request: ImageAnalysisRequest):
    """Analyze image for accessibility.
    
    In Phase 2, this accepts image descriptions or OCR text.
    In later phases, will accept actual image files and perform vision analysis.
    """
    try:
        if not request.prompt or not request.prompt.strip():
            raise ValueError('Image description or OCR text is required.')

        result = ai_service.analyze_image(request.prompt)
        return result

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except AIProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail='Unable to analyze the image. Please try again.'
        )


@router.get('/supported-formats')
def get_supported_image_formats():
    """Get supported image formats."""
    return {
        'formats': ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'],
        'max_size_mb': 10,
        'note': 'Phase 2 analyzes descriptions. Phase 3 will support direct image upload.'
    }
