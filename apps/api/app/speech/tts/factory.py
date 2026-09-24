from functools import lru_cache

from app.core.config import get_settings
from app.speech.tts.base import TextToSpeechProvider
from app.speech.tts.local import PiperTextToSpeechProvider


@lru_cache
def get_tts_provider() -> TextToSpeechProvider:
    settings = get_settings()
    return PiperTextToSpeechProvider(
        settings.piper_voice,
        settings.piper_hindi_voice,
        settings.piper_data_dir,
    )
