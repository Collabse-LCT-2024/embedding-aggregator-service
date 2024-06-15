from typing import List
from uuid import UUID

from pydantic import BaseModel


class BaseEmbeddingSchema(BaseModel):
    video_id: UUID
    embedding: List[float]
