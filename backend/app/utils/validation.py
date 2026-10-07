"""Backend utilities for file validation and input sanitization."""

import re
from typing import Set

ALLOWED_IMAGE_TYPES = {'image/png', 'image/jpeg', 'image/webp', 'image/jpg'}
SUPPORTED_AUDIO_TYPES = {'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/ogg', 'audio/webm', 'video/mp4', 'video/webm'}


def validate_text_input(value: str, max_length: int = 25000) -> str:
    """Validate and clean text input.
    
    Args:
        value: Text to validate
        max_length: Maximum allowed length
        
    Returns:
        Cleaned text
        
    Raises:
        ValueError: If text is empty or too long
    """
    cleaned = value.strip()
    if not cleaned:
        raise ValueError('Input text is empty. Please provide content to analyze.')
    if len(cleaned) > max_length:
        raise ValueError(f'Input text is too long. Maximum {max_length} characters allowed.')
    return cleaned


def validate_file_type(content_type: str, allowed_types: Set[str]) -> None:
    """Validate file MIME type.
    
    Args:
        content_type: MIME type to validate
        allowed_types: Set of allowed MIME types
        
    Raises:
        ValueError: If file type is not allowed
    """
    if content_type not in allowed_types:
        allowed_str = ', '.join(sorted(allowed_types))
        raise ValueError(f'Unsupported file type: {content_type}. Allowed types: {allowed_str}')


def validate_file_size(size_bytes: int, max_mb: int = 10) -> None:
    """Validate file size.
    
    Args:
        size_bytes: File size in bytes
        max_mb: Maximum allowed size in MB
        
    Raises:
        ValueError: If file is empty or too large
    """
    if size_bytes <= 0:
        raise ValueError('The uploaded file is empty.')
    max_bytes = max_mb * 1024 * 1024
    if size_bytes > max_bytes:
        raise ValueError(f'File is too large. Maximum allowed size is {max_mb} MB.')


def sanitize_text(value: str) -> str:
    """Remove null bytes and normalize whitespace.
    
    Args:
        value: Text to sanitize
        
    Returns:
        Sanitized text
    """
    value = value.replace('\x00', '')
    value = re.sub(r'\s+', ' ', value).strip()
    return value
