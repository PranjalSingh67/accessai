"""Routes for audio analysis."""

from fastapi import APIRouter, HTTPException
from app.models.schemas import AudioAnalysisRequest, AccessibilityResponse
from app.services.ai_service import AIService, AIProviderError
from app.utils.validation import validate_text_input

router = APIRouter(prefix='/api/v1/audio', tags=['audio'])
ai_service = AIService()


@router.post('/analyze', response_model=AccessibilityResponse)
def analyze_audio(request: AudioAnalysisRequest):
    """Analyze audio transcript.
    
    Accepts a transcript (text) from speech-to-text conversion.
    Summarizes and extracts key actions, deadlines, and information.
    """
    try:
        transcript = validate_text_input(request.transcript)

        result = ai_service.analyze_audio(transcript)
        return result

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except AIProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail='Unable to analyze the audio transcript. Please try again.'
        )


@router.get('/supported-formats')
def get_supported_audio_formats():
    """Get supported audio formats."""
    return {
        'formats': ['audio/mp3', 'audio/wav', 'audio/ogg', 'video/mp4'],
        'max_size_mb': 25,
        'note': 'Phase 2 analyzes transcripts. Phase 3 will support speech-to-text conversion.'
    }
