from abc import ABC, abstractmethod


class SpeechToTextProvider(ABC):
    @abstractmethod
    def transcribe(self, audio: bytes, filename: str, language: str | None = None) -> str: ...
