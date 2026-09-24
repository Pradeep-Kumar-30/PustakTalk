from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class VectorRecord:
    id: UUID
    vector: list[float]
    payload: dict[str, str | int | float | bool | None]


@dataclass(frozen=True, slots=True)
class VectorMatch:
    id: UUID
    score: float
    payload: dict[str, str | int | float | bool | None]


class VectorStore(ABC):
    @abstractmethod
    def upsert(self, records: list[VectorRecord]) -> None: ...

    @abstractmethod
    def search(self, vector: list[float], workspace_id: UUID, limit: int) -> list[VectorMatch]: ...
