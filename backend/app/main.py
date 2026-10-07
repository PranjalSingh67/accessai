from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import APP_NAME, APP_ENV, CORS_ORIGINS
from app.models.schemas import TextAnalysisRequest, ImageAnalysisRequest, AudioAnalysisRequest, GenericAIResponse
from app.services.ai_service import AIService
from app.utils.validation import validate_text_input, validate_file_type, validate_image_size, sanitize_user_text, ALLOWED_IMAGE_TYPES, SUPPORTED_AUDIO_TYPES

app = FastAPI(title=APP_NAME, version='0.1.0', description='AccessAI backend foundation')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

ai_service = AIService()

@app.get('/health')
def health_check():
    return {'status': 'ok', 'app': APP_NAME, 'environment': APP_ENV}

@app.get('/api/v1/health')
def health_check_v1():
    return {'status': 'ok', 'service': APP_NAME}

@app.post('/api/v1/demo/text', response_model=GenericAIResponse)
def analyze_text(payload: TextAnalysisRequest):
    try:
        cleaned = validate_text_input(payload.text)
        result = ai_service.analyze_text(cleaned, payload.mode)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail='Unable to process the text right now. Please try again later.') from exc

@app.post('/api/v1/demo/image', response_model=GenericAIResponse)
def analyze_image(payload: ImageAnalysisRequest):
    try:
        result = ai_service.analyze_image(payload.prompt)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail='Unable to analyze the image right now. Please try again later.') from exc

@app.post('/api/v1/demo/audio', response_model=GenericAIResponse)
def analyze_audio(payload: AudioAnalysisRequest):
    try:
        cleaned = validate_text_input(payload.transcript)
        result = ai_service.analyze_audio(cleaned)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail='Unable to summarize the audio right now. Please try again later.') from exc

@app.post('/api/v1/upload/image')
def upload_image(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise ValueError('A file is required.')
        content_type = file.content_type or 'application/octet-stream'
        validate_file_type(content_type, ALLOWED_IMAGE_TYPES)
        data = file.file.read()
        validate_image_size(len(data), 10)
        return {'status': 'accepted', 'filename': file.filename, 'size_bytes': len(data), 'message': 'Image validation passed. AI processing is ready to be connected in later phases.'}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail='File upload failed. Please try a valid image file.') from exc

@app.post('/api/v1/upload/audio')
def upload_audio(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise ValueError('A file is required.')
        content_type = file.content_type or 'application/octet-stream'
        validate_file_type(content_type, SUPPORTED_AUDIO_TYPES)
        data = file.file.read()
        validate_image_size(len(data), 25)
        return {'status': 'accepted', 'filename': file.filename, 'size_bytes': len(data), 'message': 'Audio validation passed. Speech-to-text integration will be added in later phases.'}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail='Audio upload failed. Please try a supported file format.') from exc

@app.exception_handler(400)
async def validation_exception_handler(_, exc):
    return JSONResponse(status_code=400, content={'detail': 'The request is invalid. Please check your input and try again.'})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
