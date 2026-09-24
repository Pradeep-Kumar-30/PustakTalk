import subprocess
import tempfile
from pathlib import Path

from app.core.exceptions import ServiceUnavailableError
from app.speech.tts.base import TextToSpeechProvider


class PiperTextToSpeechProvider(TextToSpeechProvider):
    """Piper is launched without a shell; text is supplied on stdin, never as an argument."""

    def __init__(self, voice: str, hindi_voice: str, data_dir: str | None = None) -> None:
        self._voice = voice
        self._hindi_voice = hindi_voice
        self._data_dir = data_dir

    def synthesize(self, text: str, language: str | None = None) -> bytes:
        voice = self._hindi_voice if language == "hi" else self._voice
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as output:
            output_path = Path(output.name)
        try:
            command = ["piper", "--model", voice, "--output_file", str(output_path)]
            if self._data_dir:
                command.extend(["--data-dir", self._data_dir])
            try:
                subprocess.run(
                    command, input=text.encode("utf-8"), check=True, timeout=90, capture_output=True
                )
            except (
                FileNotFoundError,
                subprocess.CalledProcessError,
                subprocess.TimeoutExpired,
            ) as error:
                raise ServiceUnavailableError(
                    "Local text-to-speech is unavailable. Set INSTALL_AI=true "
                    "and rebuild the API image."
                ) from error
            return output_path.read_bytes()
        finally:
            output_path.unlink(missing_ok=True)
