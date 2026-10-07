"""Response schemas for AccessAI API."""

from pydantic import BaseModel, Field
from typing import List, Optional


class TextAnalysisRequest(BaseModel):
    """Request model for text analysis."""
    text: str = Field(..., min_length=1, max_length=25000, description='Text content to analyze.')
    mode: str = Field(default='simple', description='Analysis mode: simple, very_simple, or step_by_step')


class DigitalServiceRequest(BaseModel):
    """Request model for digital service analysis."""
    content: str = Field(..., min_length=1, max_length=25000, description='Digital service content to analyze.')


class ImageAnalysisRequest(BaseModel):
    """Request model for image analysis."""
    prompt: str = Field(default='Describe this image for accessibility. Identify important text, UI elements, and key information.', max_length=500)


class AudioAnalysisRequest(BaseModel):
    """Request model for audio analysis."""
    transcript: str = Field(..., min_length=1, max_length=25000, description='Speech-to-text transcript to analyze.')


class AccessibilityResponse(BaseModel):
    """Standard response model for all accessibility analyses."""
    summary: str = Field(..., description='Brief summary of the content')
    simplified_explanation: str = Field(..., description='Content explained in simple language')
    important_information: List[str] = Field(default_factory=list, description='Key facts and information')
    actions: List[str] = Field(default_factory=list, description='Required or recommended actions')
    warnings: List[str] = Field(default_factory=list, description='Important warnings or cautions')
    accessible_version: str = Field(..., description='Full content rewritten for accessibility')
    key_points: List[str] = Field(default_factory=list, description='Most important takeaways')
    detailed_explanation: Optional[str] = Field(default=None, description='Extended explanation if available')


class DigitalServiceResponse(AccessibilityResponse):
    """Extended response for digital service analysis."""
    required_documents: List[str] = Field(default_factory=list, description='Documents needed')
    deadlines: List[str] = Field(default_factory=list, description='Important dates and deadlines')
    service_type: str = Field(default='', description='Type of service identified')


class FileUploadResponse(BaseModel):
    """Response model for file uploads."""
    status: str = Field(..., description='Status of upload (accepted/rejected)')
    filename: str = Field(..., description='Original filename')
    size_bytes: int = Field(..., description='File size in bytes')
    message: str = Field(..., description='Status message')


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description='Service status')
    service: str = Field(..., description='Service name')
    version: str = Field(..., description='API version')
