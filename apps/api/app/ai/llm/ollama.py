import httpx

from app.ai.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    def generate(self, system: str, user: str) -> str:
        response = httpx.post(
            f"{self._base_url}/api/chat",
            json={
                "model": self._model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "options": {"temperature": 0.2},
            },
            timeout=120,
        )
        response.raise_for_status()
        return str(response.json()["message"]["content"]).strip()

    def health_check(self) -> bool:
        try:
            return httpx.get(f"{self._base_url}/api/tags", timeout=3).is_success
        except httpx.HTTPError:
            return False
