"""AI service abstraction layer for AccessAI."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AIProviderError(Exception):
    """Raised when AI provider fails."""
    pass


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def analyze_text(self, text: str, mode: str = 'simple') -> Dict[str, Any]:
        """Analyze and simplify text."""
        pass

    @abstractmethod
    def analyze_digital_service(self, content: str) -> Dict[str, Any]:
        """Analyze digital service content (forms, notices, instructions)."""
        pass

    @abstractmethod
    def analyze_image_description(self, image_description: str, prompt: str) -> Dict[str, Any]:
        """Analyze image based on description or OCR."""
        pass

    @abstractmethod
    def analyze_audio_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze audio transcript."""
        pass


class DemoAIProvider(BaseAIProvider):
    """Demo/mock AI provider for testing without real API keys."""

    def _base_response(self, subject: str) -> Dict[str, Any]:
        """Build a base response structure."""
        return {
            'summary': f'{subject} has been analyzed and structured for accessibility.',
            'simplified_explanation': 'The content has been broken down into clear, understandable language.',
            'important_information': [
                'Key details have been identified and prioritized.',
                'Required actions are presented in plain language.',
                'Important dates, deadlines, and warnings are highlighted.'
            ],
            'actions': [
                'Review the important information section first.',
                'Check for any deadlines or required documents.',
                'Follow the action items in the order presented.'
            ],
            'warnings': [
                'Always verify information from the original source.',
                'Check for legal requirements and conditions.',
                'Confirm all dates and deadlines before proceeding.'
            ],
            'accessible_version': 'The content has been rewritten in accessible language for easier understanding and follow-up.',
            'key_points': ['Content analyzed', 'Structured for clarity', 'Ready for action'],
            'detailed_explanation': 'Demo provider: This response shows how AI analysis structures content for accessibility.'
        }

    def analyze_text(self, text: str, mode: str = 'simple') -> Dict[str, Any]:
        """Analyze and simplify text."""
        if not text.strip():
            raise AIProviderError('Text is empty.')

        base = self._base_response('The text')

        if mode == 'step_by_step':
            return {
                **base,
                'summary': 'The content has been broken into simple step-by-step instructions.',
                'simplified_explanation': 'Step 1: Understand what is being asked. Step 2: Check what you need to do. Step 3: Complete each step in order.',
                'actions': [
                    '1. Read and understand the main request',
                    '2. Identify required documents or information',
                    '3. Check deadlines and important dates',
                    '4. Complete required steps in order'
                ],
                'accessible_version': 'Step-by-step guide: This information has been simplified into clear numbered steps.'
            }
        elif mode == 'very_simple':
            return {
                **base,
                'summary': 'The most important information has been extracted into very simple language.',
                'simplified_explanation': 'This is important. Here is what you need to do. Check for deadlines. Complete the task.',
                'actions': [
                    'Understand the main point',
                    'Check for deadlines',
                    'Get required documents',
                    'Do what is needed'
                ],
                'accessible_version': 'Very simple version: The key information is above. Follow the action items.'
            }

        return {
            **base,
            'summary': 'The text has been analyzed and simplified.',
            'simplified_explanation': 'Complex information has been explained in clearer language.'
        }

    def analyze_digital_service(self, content: str) -> Dict[str, Any]:
        """Analyze digital service content."""
        if not content.strip():
            raise AIProviderError('Content is empty.')

        return {
            **self._base_response('This digital service'),
            'summary': 'This appears to be a form, notice, or instruction from a public service.',
            'simplified_explanation': 'The service is asking you to complete an application or task. Here are the key steps.',
            'required_documents': [
                'Check the original document for required documents.',
                'Gather all necessary identification and proof documents.',
                'Have copies ready before starting.'
            ],
            'deadlines': [
                'Look for specific dates mentioned in the document.',
                'Mark important deadlines in your calendar.',
                'Start early to avoid missing the deadline.'
            ],
            'service_type': 'Government or public service (demo)',
            'actions': [
                'Identify what service or application this is',
                'List all required documents',
                'Note all important deadlines',
                'Follow the steps in order'
            ]
        }

    def analyze_image_description(self, image_description: str, prompt: str) -> Dict[str, Any]:
        """Analyze image based on description."""
        return {
            **self._base_response('This image'),
            'summary': 'The image has been analyzed for important content and text.',
            'simplified_explanation': 'The image contains text and information that should be read carefully. The important parts are described below.',
            'important_information': [
                'Text elements in the image should be read in order.',
                'Any buttons, links, or interactive elements are marked.',
                'Important warnings or deadlines are highlighted.'
            ],
            'actions': [
                'Read all visible text carefully',
                'Note any dates or deadlines',
                'Identify what action is needed',
                'Follow instructions in order'
            ],
            'warnings': ['Do not infer information not visible in the image.'],
            'accessible_version': 'Image description: A screenshot or document with text, instructions, and action items that need to be reviewed.'
        }

    def analyze_audio_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze audio transcript."""
        if not transcript.strip():
            raise AIProviderError('Transcript is empty.')

        return {
            **self._base_response('This audio'),
            'summary': 'The audio has been transcribed and analyzed into key points.',
            'simplified_explanation': 'A message was recorded and has been converted to text. Here are the main points.',
            'important_information': [
                'The recording contains important information or instructions.',
                'Key action items have been identified.',
                'Important dates or deadlines should be confirmed.'
            ],
            'actions': [
                'Review the full transcript carefully',
                'Check for any time-sensitive instructions',
                'Identify the main action required',
                'Confirm deadlines before proceeding'
            ],
            'warnings': ['Audio can be unclear; verify information from the original source.'],
            'accessible_version': 'Transcript summary: A recorded message has been converted to text with key action points identified.'
        }


class AIService:
    """Main AI service that uses a provider backend."""

    def __init__(self, provider: BaseAIProvider | None = None):
        """Initialize with a provider (defaults to demo).
        
        Args:
            provider: AI provider instance. Defaults to DemoAIProvider.
        """
        self.provider = provider or DemoAIProvider()

    def analyze_text(self, text: str, mode: str = 'simple') -> Dict[str, Any]:
        """Analyze and simplify text.
        
        Args:
            text: Text to analyze
            mode: Analysis mode (simple, very_simple, step_by_step)
            
        Returns:
            Structured analysis response
        """
        return self.provider.analyze_text(text, mode)

    def analyze_digital_service(self, content: str) -> Dict[str, Any]:
        """Analyze digital service content.
        
        Args:
            content: Digital service content
            
        Returns:
            Structured analysis response
        """
        return self.provider.analyze_digital_service(content)

    def analyze_image(self, image_description: str, prompt: str = '') -> Dict[str, Any]:
        """Analyze image.
        
        Args:
            image_description: Description or OCR of image
            prompt: Optional custom analysis prompt
            
        Returns:
            Structured analysis response
        """
        return self.provider.analyze_image_description(image_description, prompt)

    def analyze_audio(self, transcript: str) -> Dict[str, Any]:
        """Analyze audio transcript.
        
        Args:
            transcript: Audio transcript text
            
        Returns:
            Structured analysis response
        """
        return self.provider.analyze_audio_transcript(transcript)
