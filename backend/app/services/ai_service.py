from __future__ import annotations

from typing import Any, Dict, List

class AIProviderError(RuntimeError):
    pass


class BaseAIProvider:
    def analyze_text(self, text: str, mode: str = 'simple') -> Dict[str, Any]:
        raise NotImplementedError

    def analyze_image(self, prompt: str) -> Dict[str, Any]:
        raise NotImplementedError

    def analyze_audio(self, transcript: str) -> Dict[str, Any]:
        raise NotImplementedError


class DemoAIProvider(BaseAIProvider):
    def _base_response(self, subject: str) -> Dict[str, Any]:
        return {
            'summary': f'{subject} has been reviewed for accessibility and converted into clear, brief guidance.',
            'simplified_explanation': 'The main idea is presented in plain language so it is easier to understand and act on.',
            'important_information': [
                'Key details are extracted and prioritized.',
                'Required actions are written in plain language.',
                'Important dates, deadlines, and warnings are highlighted.'
            ],
            'actions': ['Review the essential information', 'Follow the stated next step', 'Check for dates, warnings, and required documents'],
            'warnings': ['Do not rely on assumptions when the original content is unclear.', 'Always verify deadlines and conditions from the source document.'],
            'accessible_version': 'The content has been rewritten in a clearer format for easier reading and follow-up.',
            'key_points': ['Clear explanation', 'Structured summary', 'Accessible action guidance'],
            'detailed_explanation': 'This is a demonstration response designed to show the structured accessibility workflow.'
        }

    def analyze_text(self, text: str, mode: str = 'simple') -> Dict[str, Any]:
        cleaned = text.strip()
        if not cleaned:
            raise AIProviderError('Text is empty. Please provide content to analyze.')
        if mode == 'step_by_step':
            return {
                **self._base_response('The text'),
                'summary': 'The information has been simplified into a step-by-step explanation to reduce cognitive load.',
                'actions': ['Read the problem statement first.', 'Identify the most important action required.', 'Check for dates, requirements, and consequences.'],
                'simplified_explanation': 'Break the content into short steps. Focus on what must happen first, then what happens next.',
                'accessible_version': 'Step 1: Understand the request. Step 2: Check requirements. Step 3: Complete the required action before the deadline.'
            }
        elif mode == 'very_simple':
            return {
                **self._base_response('The text'),
                'summary': 'This content is explained in very simple language with a short summary for quick understanding.',
                'actions': ['Read the short summary.', 'Look for deadlines or required documents.', 'Complete the action as soon as possible.'],
                'simplified_explanation': 'The text is shortened into simple points so the most important information is easier to remember.',
                'accessible_version': 'This is important. Check the deadline. Gather any required documents. Complete the required task.'
            }
        return {
            **self._base_response('The text'),
            'summary': 'The text was simplified into a clear accessibility-first summary.',
            'important_information': ['The text was structured into plain-language guidance.', 'Key requirements, deadlines, and actions were identified.'],
            'accessible_version': 'The content is written in accessible plain language with the most important points highlighted.'
        }

    def analyze_image(self, prompt: str) -> Dict[str, Any]:
        return {
            'summary': 'The image was reviewed for key visual content and essential information.',
            'simplified_explanation': 'This image appears to contain information that should be read carefully. The highest-priority details are described below.',
            'important_information': ['The image likely contains important instructions or labels.', 'Text elements should be checked and read in sequence.'],
            'actions': ['Read the visible text carefully.', 'Note any dates, actions, or warnings.', 'Use the accessible summary for follow-up.'],
            'warnings': ['Do not infer missing information that is not visible.'],
            'accessible_version': 'Image description: A visual screen or document contains instructions, important text, and actions that should be reviewed carefully.',
            'key_points': ['Visual content identified', 'Text extracted for review', 'Clear action guidance'],
            'detailed_explanation': 'This is the demo accessibility workflow for image interpretation.'
        }

    def analyze_audio(self, transcript: str) -> Dict[str, Any]:
        return {
            'summary': 'The audio transcript was summarized into short, actionable key points.',
            'simplified_explanation': 'The spoken content was turned into readable text and organized into key action points.',
            'important_information': ['The transcript contains instructions or information that should be reviewed.', 'Important deadlines or actions should be confirmed in the original source.'],
            'actions': ['Review the transcript carefully.', 'Check for any time-sensitive instructions.', 'Confirm the required task before acting.'],
            'warnings': ['Audio can be unclear; check the transcript for missing details.'],
            'accessible_version': 'Transcript summary: a spoken message provides instructions, information, and follow-up actions that should be reviewed in writing.',
            'key_points': ['Audio converted to text', 'Summary generated', 'Action points extracted'],
            'detailed_explanation': 'This demo response shows how spoken content can be turned into clear accessible text.'
        }


class AIService:
    def __init__(self, provider: BaseAIProvider | None = None):
        self.provider = provider or DemoAIProvider()

    def analyze_text(self, text: str, mode: str = 'simple') -> Dict[str, Any]:
        return self.provider.analyze_text(text, mode)

    def analyze_image(self, prompt: str) -> Dict[str, Any]:
        return self.provider.analyze_image(prompt)

    def analyze_audio(self, transcript: str) -> Dict[str, Any]:
        return self.provider.analyze_audio(transcript)
