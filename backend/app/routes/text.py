"""Routes for text analysis and simplification."""

from fastapi import APIRouter, HTTPException
from app.models.schemas import TextAnalysisRequest, AccessibilityResponse
from app.services.ai_service import AIService, AIProviderError
from app.utils.validation import validate_text_input, sanitize_text

router = APIRouter(prefix='/api/v1/text', tags=['text'])
ai_service = AIService()


@router.post('/analyze', response_model=AccessibilityResponse)
def analyze_text(request: TextAnalysisRequest):
    """Analyze and simplify text.
    
    Accepts text in different analysis modes:
    - simple: Clear explanation
    - very_simple: Shortest possible explanation
    - step_by_step: Numbered steps
    """
    try:
        text = validate_text_input(request.text)
        text = sanitize_text(text)

        if request.mode not in ['simple', 'very_simple', 'step_by_step']:
            raise ValueError(f"Invalid mode '{request.mode}'. Use: simple, very_simple, or step_by_step")

        result = ai_service.analyze_text(text, request.mode)
        return result

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except AIProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail='Unable to analyze text. Please try again.'
        )


@router.get('/modes')
def get_text_modes():
    """Get available text analysis modes."""
    return {
        'modes': [
            {
                'key': 'simple',
                'label': 'Simple',
                'description': 'Clear explanation with important information highlighted.'
            },
            {
                'key': 'very_simple',
                'label': 'Very Simple',
                'description': 'Shortest possible explanation, ideal for quick understanding.'
            },
            {
                'key': 'step_by_step',
                'label': 'Step by Step',
                'description': 'Numbered steps to reduce cognitive load.'
            }
        ]
    }
