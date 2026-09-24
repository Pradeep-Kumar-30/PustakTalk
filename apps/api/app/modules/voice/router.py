from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile

from app.core.config import Settings, get_settings
from app.modules.auth.dependencies import CurrentUser
from app.modules.voice.schemas import SpeechRequest, TranscriptionResponse
from app.modules.voice.service import VoiceService

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(
    audio: Annotated[UploadFile, File()],
    user: CurrentUser,  # noqa: ARG001
    settings: Annotated[Settings, Depends(get_settings)],
    language: str | None = None,
) -> TranscriptionResponse:
    if audio.content_type not in {
        "audio/webm",
        "audio/wav",
        "audio/mpeg",
        "audio/mp4",
        "audio/ogg",
    }:
        raise HTTPException(status_code=415, detail="Unsupported audio format")
    content = await audio.read(25 * 1024 * 1024)
    transcript = VoiceService(settings).transcribe(
        content, audio.filename or "recording.webm", language
    )
    return TranscriptionResponse(transcript=transcript)


@router.post("/speak")
def speak(
    payload: SpeechRequest,
    user: CurrentUser,  # noqa: ARG001
    settings: Annotated[Settings, Depends(get_settings)],
) -> Response:
    audio = VoiceService(settings).synthesize(payload.text, payload.language)
    return Response(audio, media_type="audio/wav", headers={"Cache-Control": "no-store"})
