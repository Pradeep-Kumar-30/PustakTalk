from functools import lru_cache

from app.core.config import Settings
from app.core.exceptions import ServiceUnavailableError
from app.speech.stt.base import SpeechToTextProvider
from app.speech.tts.base import TextToSpeechProvider
from app.speech.tts.factory import get_tts_provider


@lru_cache
def get_stt_provider(model: str, device: str, compute_type: str) -> SpeechToTextProvider:
    # faster-whisper loads native inference dependencies.  Import it only when
    # transcription is requested so normal API startup does not depend on it.
    try:
        from app.speech.stt.faster_whisper import FasterWhisperProvider
    except ModuleNotFoundError as error:
        raise ServiceUnavailableError(
            "Local speech dependencies are not installed. Set INSTALL_AI=true "
            "and rebuild the API image."
        ) from error

    return FasterWhisperProvider(model, device, compute_type)


class VoiceService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def transcribe(self, audio: bytes, filename: str, language: str | None) -> str:
        provider = get_stt_provider(
            self._settings.whisper_model,
            self._settings.whisper_device,
            self._settings.whisper_compute_type,
        )
        return provider.transcribe(audio, filename, language)

    def synthesize(self, text: str, language: str | None) -> bytes:
        provider: TextToSpeechProvider = get_tts_provider()
        return provider.synthesize(text, language)
