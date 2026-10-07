"""Backend tests for AccessAI."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_service import DemoAIProvider, AIProviderError


client = TestClient(app)


class TestHealth:
    """Test health check endpoints."""

    def test_health_check(self):
        """Test basic health check."""
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert 'service' in data
        assert 'version' in data

    def test_api_info(self):
        """Test API info endpoint."""
        response = client.get('/api/v1/info')
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
        assert 'endpoints' in data
        assert 'version' in data


class TestTextAnalysis:
    """Test text analysis endpoints."""

    def test_analyze_text_simple(self):
        """Test simple text analysis."""
        response = client.post(
            '/api/v1/text/analyze',
            json={'text': 'This is a complicated legal document.', 'mode': 'simple'}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data
        assert 'simplified_explanation' in data
        assert 'important_information' in data
        assert 'actions' in data
        assert isinstance(data['important_information'], list)
        assert isinstance(data['actions'], list)

    def test_analyze_text_very_simple(self):
        """Test very simple mode."""
        response = client.post(
            '/api/v1/text/analyze',
            json={'text': 'Complex content here.', 'mode': 'very_simple'}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data
        assert len(data['summary']) > 0

    def test_analyze_text_step_by_step(self):
        """Test step-by-step mode."""
        response = client.post(
            '/api/v1/text/analyze',
            json={'text': 'Some instructions.', 'mode': 'step_by_step'}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'actions' in data
        assert len(data['actions']) > 0

    def test_analyze_text_empty(self):
        """Test empty text validation."""
        response = client.post(
            '/api/v1/text/analyze',
            json={'text': '', 'mode': 'simple'}
        )
        assert response.status_code == 400

    def test_analyze_text_whitespace_only(self):
        """Test whitespace-only text."""
        response = client.post(
            '/api/v1/text/analyze',
            json={'text': '   \n\t  ', 'mode': 'simple'}
        )
        assert response.status_code == 400

    def test_analyze_text_invalid_mode(self):
        """Test invalid mode."""
        response = client.post(
            '/api/v1/text/analyze',
            json={'text': 'Some text', 'mode': 'invalid'}
        )
        assert response.status_code == 400

    def test_text_modes(self):
        """Test modes endpoint."""
        response = client.get('/api/v1/text/modes')
        assert response.status_code == 200
        data = response.json()
        assert 'modes' in data
        assert len(data['modes']) == 3
        mode_keys = [m['key'] for m in data['modes']]
        assert 'simple' in mode_keys
        assert 'very_simple' in mode_keys
        assert 'step_by_step' in mode_keys


class TestDigitalService:
    """Test digital service analysis endpoints."""

    def test_analyze_digital_service(self):
        """Test digital service analysis."""
        response = client.post(
            '/api/v1/digital-service/analyze',
            json={'content': 'Application deadline: 15 November. Required: Aadhaar card and income certificate.'}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data
        assert 'required_documents' in data
        assert 'deadlines' in data
        assert 'service_type' in data
        assert isinstance(data['required_documents'], list)
        assert isinstance(data['deadlines'], list)

    def test_analyze_digital_service_empty(self):
        """Test empty digital service content."""
        response = client.post(
            '/api/v1/digital-service/analyze',
            json={'content': ''}
        )
        assert response.status_code == 400

    def test_digital_service_examples(self):
        """Test examples endpoint."""
        response = client.get('/api/v1/digital-service/examples')
        assert response.status_code == 200
        data = response.json()
        assert 'examples' in data
        assert len(data['examples']) > 0
        assert isinstance(data['examples'], list)


class TestImageAnalysis:
    """Test image analysis endpoints."""

    def test_analyze_image(self):
        """Test image analysis."""
        response = client.post(
            '/api/v1/image/analyze',
            json={'prompt': 'A screenshot of a government website with a form.'}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data
        assert 'accessible_version' in data
        assert 'important_information' in data

    def test_analyze_image_default_prompt(self):
        """Test image analysis with default prompt."""
        response = client.post(
            '/api/v1/image/analyze',
            json={}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data

    def test_analyze_image_empty(self):
        """Test empty image prompt."""
        response = client.post(
            '/api/v1/image/analyze',
            json={'prompt': ''}
        )
        assert response.status_code == 400

    def test_image_supported_formats(self):
        """Test supported formats endpoint."""
        response = client.get('/api/v1/image/supported-formats')
        assert response.status_code == 200
        data = response.json()
        assert 'formats' in data
        assert 'max_size_mb' in data
        assert len(data['formats']) > 0


class TestAudioAnalysis:
    """Test audio analysis endpoints."""

    def test_analyze_audio(self):
        """Test audio transcript analysis."""
        response = client.post(
            '/api/v1/audio/analyze',
            json={'transcript': 'This is a recording of important instructions for your application.'}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data
        assert 'actions' in data
        assert isinstance(data['actions'], list)

    def test_analyze_audio_empty(self):
        """Test empty audio transcript."""
        response = client.post(
            '/api/v1/audio/analyze',
            json={'transcript': ''}
        )
        assert response.status_code == 400

    def test_audio_supported_formats(self):
        """Test supported formats endpoint."""
        response = client.get('/api/v1/audio/supported-formats')
        assert response.status_code == 200
        data = response.json()
        assert 'formats' in data
        assert 'max_size_mb' in data
        assert len(data['formats']) > 0


class TestAIProvider:
    """Test AI provider abstraction."""

    def test_demo_provider_text(self):
        """Test demo provider text analysis."""
        provider = DemoAIProvider()
        result = provider.analyze_text('Sample text')
        assert 'summary' in result
        assert 'simplified_explanation' in result
        assert 'accessible_version' in result

    def test_demo_provider_empty_text(self):
        """Test demo provider with empty text."""
        provider = DemoAIProvider()
        with pytest.raises(AIProviderError):
            provider.analyze_text('')

    def test_demo_provider_digital_service(self):
        """Test demo provider digital service analysis."""
        provider = DemoAIProvider()
        result = provider.analyze_digital_service('Service content')
        assert 'required_documents' in result
        assert 'deadlines' in result
        assert 'service_type' in result

    def test_demo_provider_image(self):
        """Test demo provider image analysis."""
        provider = DemoAIProvider()
        result = provider.analyze_image_description('Image description', '')
        assert 'summary' in result
        assert 'accessible_version' in result
        assert 'important_information' in result

    def test_demo_provider_audio(self):
        """Test demo provider audio analysis."""
        provider = DemoAIProvider()
        result = provider.analyze_audio_transcript('Transcript text')
        assert 'summary' in result
        assert 'actions' in result


class TestResponseStructure:
    """Test response data structure integrity."""

    def test_response_has_all_fields(self):
        """Test that responses have all required fields."""
        response = client.post(
            '/api/v1/text/analyze',
            json={'text': 'Sample text'}
        )
        data = response.json()
        required_fields = ['summary', 'simplified_explanation', 'important_information', 
                          'actions', 'warnings', 'accessible_version', 'key_points']
        for field in required_fields:
            assert field in data, f'Missing field: {field}'

    def test_digital_service_has_extended_fields(self):
        """Test that digital service responses have extended fields."""
        response = client.post(
            '/api/v1/digital-service/analyze',
            json={'content': 'Sample service content'}
        )
        data = response.json()
        assert 'required_documents' in data
        assert 'deadlines' in data
        assert 'service_type' in data
