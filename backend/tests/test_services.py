"""Tests for AI service layer."""

import pytest
from app.services.ai_service import AIService, DemoAIProvider, AIProviderError


class TestAIService:
    """Test AIService wrapper."""

    def test_ai_service_defaults_to_demo_provider(self):
        """Test AIService uses demo provider by default."""
        service = AIService()
        assert isinstance(service.provider, DemoAIProvider)

    def test_ai_service_analyze_text(self):
        """Test AIService.analyze_text."""
        service = AIService()
        result = service.analyze_text('Sample text')
        assert 'summary' in result

    def test_ai_service_analyze_digital_service(self):
        """Test AIService.analyze_digital_service."""
        service = AIService()
        result = service.analyze_digital_service('Service content')
        assert 'required_documents' in result

    def test_ai_service_analyze_image(self):
        """Test AIService.analyze_image."""
        service = AIService()
        result = service.analyze_image('Image description')
        assert 'accessible_version' in result

    def test_ai_service_analyze_audio(self):
        """Test AIService.analyze_audio."""
        service = AIService()
        result = service.analyze_audio('Transcript')
        assert 'summary' in result


class TestDemoProviderModes:
    """Test demo provider different modes."""

    def test_simple_mode(self):
        """Test simple analysis mode."""
        provider = DemoAIProvider()
        result = provider.analyze_text('Text', mode='simple')
        assert 'summary' in result

    def test_very_simple_mode(self):
        """Test very simple analysis mode."""
        provider = DemoAIProvider()
        result = provider.analyze_text('Text', mode='very_simple')
        assert 'summary' in result
        assert 'very simple' in result['summary'].lower() or 'short' in result['summary'].lower()

    def test_step_by_step_mode(self):
        """Test step-by-step analysis mode."""
        provider = DemoAIProvider()
        result = provider.analyze_text('Text', mode='step_by_step')
        assert 'summary' in result
        assert 'step' in result['summary'].lower()
