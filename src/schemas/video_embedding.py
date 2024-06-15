from src.schemas.base import BaseEmbeddingSchema


class VideoEmbeddingSchema(BaseEmbeddingSchema):
    video_url: str
    text: str
    collection: str
