from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system: str, user: str) -> str: ...

    @abstractmethod
    def health_check(self) -> bool: ...
