from pydantic import BaseModel, Field


class TranscriptionResponse(BaseModel):
    transcript: str


class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12_000)
    language: str | None = Field(default=None, pattern="^(en|hi)?$")
