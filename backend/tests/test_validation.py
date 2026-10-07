"""Tests for input validation utilities."""

import pytest
from app.utils.validation import (
    validate_text_input,
    validate_file_type,
    validate_file_size,
    sanitize_text,
    ALLOWED_IMAGE_TYPES,
    SUPPORTED_AUDIO_TYPES
)


class TestTextValidation:
    """Test text input validation."""

    def test_valid_text(self):
        """Test valid text input."""
        result = validate_text_input('This is valid text.')
        assert result == 'This is valid text.'

    def test_empty_text_raises(self):
        """Test empty text raises error."""
        with pytest.raises(ValueError):
            validate_text_input('')

    def test_whitespace_only_raises(self):
        """Test whitespace-only text raises error."""
        with pytest.raises(ValueError):
            validate_text_input('   \n\t  ')

    def test_text_too_long_raises(self):
        """Test text exceeding max length raises error."""
        long_text = 'a' * 25001
        with pytest.raises(ValueError):
            validate_text_input(long_text)

    def test_text_trimmed(self):
        """Test text is trimmed of whitespace."""
        result = validate_text_input('  text with spaces  ')
        assert result == 'text with spaces'


class TestFileTypeValidation:
    """Test file type validation."""

    def test_valid_image_type(self):
        """Test valid image MIME type."""
        validate_file_type('image/png', ALLOWED_IMAGE_TYPES)

    def test_invalid_image_type_raises(self):
        """Test invalid image type raises error."""
        with pytest.raises(ValueError):
            validate_file_type('image/gif', ALLOWED_IMAGE_TYPES)

    def test_valid_audio_type(self):
        """Test valid audio MIME type."""
        validate_file_type('audio/mp3', SUPPORTED_AUDIO_TYPES)

    def test_invalid_audio_type_raises(self):
        """Test invalid audio type raises error."""
        with pytest.raises(ValueError):
            validate_file_type('audio/flac', SUPPORTED_AUDIO_TYPES)


class TestFileSizeValidation:
    """Test file size validation."""

    def test_valid_file_size(self):
        """Test valid file size."""
        validate_file_size(5 * 1024 * 1024, 10)

    def test_empty_file_raises(self):
        """Test empty file raises error."""
        with pytest.raises(ValueError):
            validate_file_size(0, 10)

    def test_oversized_file_raises(self):
        """Test oversized file raises error."""
        with pytest.raises(ValueError):
            validate_file_size(15 * 1024 * 1024, 10)

    def test_exact_max_size_valid(self):
        """Test file exactly at max size is valid."""
        max_bytes = 10 * 1024 * 1024
        validate_file_size(max_bytes, 10)


class TestTextSanitization:
    """Test text sanitization."""

    def test_sanitize_removes_null_bytes(self):
        """Test null byte removal."""
        result = sanitize_text('text\x00with\x00nulls')
        assert '\x00' not in result

    def test_sanitize_normalizes_whitespace(self):
        """Test whitespace normalization."""
        result = sanitize_text('text  with   multiple    spaces')
        assert result == 'text with multiple spaces'

    def test_sanitize_trims_edges(self):
        """Test edge trimming."""
        result = sanitize_text('  text  ')
        assert result == 'text'

    def test_sanitize_handles_newlines(self):
        """Test newline handling."""
        result = sanitize_text('text\nwith\nnewlines')
        assert '\n' not in result
        assert 'text' in result and 'with' in result and 'newlines' in result
