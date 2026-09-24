from uuid import UUID

from qdrant_client import QdrantClient, models

from app.infrastructure.vectorstore.base import VectorMatch, VectorRecord, VectorStore


class QdrantVectorStore(VectorStore):
    def __init__(self, url: str, collection: str, dimension: int) -> None:
        self._client = QdrantClient(url=url)
        self._collection = collection
        self._dimension = dimension

    def ensure_collection(self) -> None:
        if not self._client.collection_exists(self._collection):
            self._client.create_collection(
                collection_name=self._collection,
                vectors_config=models.VectorParams(
                    size=self._dimension, distance=models.Distance.COSINE
                ),
            )
            self._client.create_payload_index(
                self._collection, "workspace_id", models.PayloadSchemaType.KEYWORD
            )

    def upsert(self, records: list[VectorRecord]) -> None:
        if not records:
            return
        self.ensure_collection()
        self._client.upsert(
            collection_name=self._collection,
            points=[
                models.PointStruct(id=str(record.id), vector=record.vector, payload=record.payload)
                for record in records
            ],
            wait=True,
        )

    def search(self, vector: list[float], workspace_id: UUID, limit: int) -> list[VectorMatch]:
        self.ensure_collection()
        results = self._client.query_points(
            collection_name=self._collection,
            query=vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="workspace_id", match=models.MatchValue(value=str(workspace_id))
                    )
                ]
            ),
            limit=limit,
        ).points
        return [
            VectorMatch(id=UUID(str(item.id)), score=item.score, payload=item.payload)
            for item in results
        ]
