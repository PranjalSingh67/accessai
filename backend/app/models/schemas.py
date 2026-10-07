from pydantic import BaseModel, Field
from typing import List, Optional

class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, description='Text content to simplify or analyze.')
    mode: str = Field(default='simple', description='One of: simple, very_simple, step_by_step')

class ImageAnalysisRequest(BaseModel):
    prompt: str = Field(default='Describe the image for accessibility and note important information.', max_length=500)

class AudioAnalysisRequest(BaseModel):
    transcript: str = Field(..., min_length=1, description='Speech-to-text transcript to summarize.')

class GenericAIResponse(BaseModel):
    summary: str
    simplified_explanation: str
    important_information: List[str] = Field(default_factory=list)
    actions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    accessible_version: str
    key_points: List[str] = Field(default_factory=list)
    detailed_explanation: Optional[str] = None
