from app.core.config import Settings
from app.modules.voice import service


class FakeTextToSpeechProvider:
    def synthesize(self, text: str, language: str | None = None) -> bytes:
        return f"{language}:{text}".encode()


class FakeSpeechToTextProvider:
    def transcribe(self, audio: bytes, filename: str, language: str | None = None) -> str:
        return f"{filename}:{language}:{audio.decode()}"


def test_synthesis_does_not_initialize_speech_to_text(monkeypatch) -> None:
    def unexpected_stt(*_args):
        raise AssertionError("TTS must not load the Whisper provider")

    monkeypatch.setattr(service, "get_stt_provider", unexpected_stt)
    monkeypatch.setattr(service, "get_tts_provider", lambda: FakeTextToSpeechProvider())

    audio = service.VoiceService(Settings()).synthesize("hello", "en")

    assert audio == b"en:hello"


def test_transcription_loads_speech_to_text_only_when_requested(monkeypatch) -> None:
    captured: dict[str, tuple[str, str, str]] = {}

    def get_provider(model: str, device: str, compute_type: str) -> FakeSpeechToTextProvider:
        captured["settings"] = (model, device, compute_type)
        return FakeSpeechToTextProvider()

    monkeypatch.setattr(service, "get_stt_provider", get_provider)

    transcript = service.VoiceService(Settings()).transcribe(b"audio", "clip.webm", "hi")

    assert transcript == "clip.webm:hi:audio"
    assert captured["settings"] == ("small", "cpu", "int8")
