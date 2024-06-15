from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.core.config import settings
from src.database.base import DBClientABC


class EmbeddingMergerABC(ABC):
    @abstractmethod
    def find_embedding(self, embedding_id: UUID) -> List[List[float]]:
        ...

    @abstractmethod
    def merge_embeddings(self, embeddings: List[List[float]]) -> List[float]:
        ...


class EmbeddingMerger:
    def __init__(self, db_client: DBClientABC, collection_names: List[str] = settings.QDRANT_COLLECTION_NAMES,
                 merged_collection_name: str = settings.MERGED_COLLECTION_NAME):
        self.db_client = db_client
        self.collection_names = collection_names
        self.merged_collection_name = merged_collection_name

    def find_embedding(self, embedding_id: UUID) -> List[List[float]]:
        embeddings = []
        for collection_name in self.collection_names:
            point = self.db_client.find_by_id(embedding_id, collection_name=collection_name)
            if point:
                embeddings.append(point[0].vector)
        if len(embeddings) == len(self.collection_names):
            return embeddings
        return []

    def merge_embeddings(self, embeddings: List[List[float]]) -> List[float]:
        return [sum(x) / len(embeddings) for x in zip(*embeddings)]
