import re
from typing import Tuple

ALLOWED_IMAGE_TYPES = {'image/png', 'image/jpeg', 'image/webp'}
SUPPORTED_AUDIO_TYPES = {'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/ogg', 'audio/webm', 'video/mp4', 'video/webm'}


def validate_text_input(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError('Input text is empty. Please provide content to analyze.')
    if len(cleaned) > 25000:
        raise ValueError('Input text is too long. Please reduce it before submitting.')
    return cleaned


def validate_file_type(content_type: str, allowed_types: set[str]) -> None:
    if content_type not in allowed_types:
        raise ValueError(f'Unsupported file type: {content_type}. Please upload a supported file.')


def validate_image_size(size_bytes: int, max_mb: int = 10) -> None:
    max_bytes = max_mb * 1024 * 1024
    if size_bytes <= 0:
        raise ValueError('The uploaded file is empty.')
    if size_bytes > max_bytes:
        raise ValueError(f'File is too large. Maximum allowed size is {max_mb} MB.')


def sanitize_user_text(value: str) -> str:
    value = value.replace('\x00', '')
    value = re.sub(r'\s+', ' ', value).strip()
    return value
