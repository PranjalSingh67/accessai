"""Routes for digital service analysis."""

from fastapi import APIRouter, HTTPException
from app.models.schemas import DigitalServiceRequest, DigitalServiceResponse
from app.services.ai_service import AIService, AIProviderError
from app.utils.validation import validate_text_input, sanitize_text

router = APIRouter(prefix='/api/v1/digital-service', tags=['digital-service'])
ai_service = AIService()


@router.post('/analyze', response_model=DigitalServiceResponse)
def analyze_digital_service(request: DigitalServiceRequest):
    """Analyze digital service content.
    
    Accepts content from forms, notices, instructions, applications, etc.
    Extracts: required documents, deadlines, actions, and important warnings.
    """
    try:
        content = validate_text_input(request.content)
        content = sanitize_text(content)

        result = ai_service.analyze_digital_service(content)
        return result

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except AIProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail='Unable to analyze the content. Please try again.'
        )


@router.get('/examples')
def get_digital_service_examples():
    """Get example digital service types."""
    return {
        'examples': [
            'Scholarship application form',
            'Bank notification',
            'Government website instruction',
            'Job application',
            'Insurance claim form',
            'College portal notice',
            'Public service deadline',
            'Tax filing instruction'
        ]
    }
