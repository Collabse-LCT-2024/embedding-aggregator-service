from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

import numpy as np

from src.core.config import settings
from src.database.base import DBClientABC


class EmbeddingMergerABC(ABC):
    @abstractmethod
    def find_embedding(self, actual_collection: str, actual_embedding: List[float], embedding_id: UUID) -> List[dict]:
        ...

    @abstractmethod
    def merge_embeddings(self, embeddings: List[dict]) -> List[float]:
        ...


class EmbeddingMerger:
    def __init__(self, db_client: DBClientABC, collection_names: dict = settings.QDRANT_COLLECTION_NAMES,
                 merged_collection_name: str = settings.MERGED_COLLECTION_NAME):
        self.db_client = db_client
        self.collection_names = collection_names
        self.merged_collection_name = merged_collection_name

    def find_embedding(self, actual_collection: str, actual_embedding: List[float], embedding_id: UUID) -> List[dict]:
        embeddings = []
        processed = 0
        for collection_type, collection_name in self.collection_names.items():
            if collection_name == actual_collection:
                embeddings.append({collection_type: actual_embedding})
                processed += 1
                continue
            point = self.db_client.find_by_id(embedding_id, collection_name=collection_name)
            if point:
                if "valid" in point[0].payload and point[0].payload["valid"]:
                    embeddings.append({collection_type: point[0].vector})
                    processed += 1
                if "valid" in point[0].payload and not point[0].payload["valid"]:
                    processed += 1
        if processed == len(self.collection_names):
            return embeddings
        return []

    def merge_embeddings(self, embeddings: List[dict]) -> List[float]:
        if len(embeddings) == 1:
            if "VIDEO_COLLECTION" in embeddings[0]:
                return embeddings[0]["VIDEO_COLLECTION"]
            elif "AUDIO_COLLECTION" in embeddings[0]:
                return embeddings[0]["AUDIO_COLLECTION"]
            elif "TAGS_COLLECTION" in embeddings[0]:
                return embeddings[0]["TAGS_COLLECTION"]

        video_embedding = None
        audio_embedding = None
        tags_embedding = None

        for embedding in embeddings:
            if "VIDEO_COLLECTION" in embedding:
                video_embedding = embedding["VIDEO_COLLECTION"]
            elif "AUDIO_COLLECTION" in embedding:
                audio_embedding = embedding["AUDIO_COLLECTION"]
            elif "TAGS_COLLECTION" in embedding:
                tags_embedding = embedding["TAGS_COLLECTION"]

        if video_embedding and tags_embedding and not audio_embedding:
            print("Merging video and tags")
            weights = [0.45, 0.55]
            embeddings = [video_embedding, tags_embedding]
        elif video_embedding and audio_embedding and not tags_embedding:
            print("Merging video and audio")
            weights = [0.65, 0.35]
            embeddings = [video_embedding, audio_embedding]
        else:
            print("Merging all")
            weights = [0.4, 0.2, 0.4]
            embeddings = [video_embedding, audio_embedding, tags_embedding]

        merged_embedding = np.average(embeddings, axis=0, weights=weights)

        return merged_embedding
