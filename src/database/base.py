from typing import List
from uuid import UUID
from abc import ABC, abstractmethod

from src.models.video_properties import VideoProperties


class DBClientABC(ABC):
    @abstractmethod
    def find_by_id(self, item_id: UUID, collection_name: str) -> list:
        ...

    @abstractmethod
    def save_embedding(self, embedding: List[float], properties: VideoProperties, collection_name: str) -> None:
        ...
