from typing import List
from uuid import UUID

from qdrant_client.http.models import Record

from src.core.config import settings
from src.database.base import DBClientABC
from qdrant_client import QdrantClient
from qdrant_client.http import models

from src.models.video_properties import VideoProperties


class QdrantDBClient(DBClientABC):
    def __init__(self):
        self.qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, grpc_port=settings.QDRANT_GRPC_PORT, prefer_grpc=True)

    def find_by_id(self, item_id: UUID, collection_name: str) -> List[Record]:
        return self.qdrant_client.retrieve(collection_name=collection_name, ids=[str(item_id)], with_vectors=True)

    def save_embedding(self, embedding, properties: VideoProperties, collection_name: str) -> None:
        self.qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(properties.external_id),
                    vector=embedding,
                    payload=properties.to_dict(),
                )
            ],
        )
