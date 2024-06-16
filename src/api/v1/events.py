from fastapi import APIRouter, Depends

from src.core.config import settings
from src.database.base import DBClientABC
from src.embedding_merger import EmbeddingMergerABC
from src.models.video_properties import VideoProperties
from src.schemas.video_embedding import VideoEmbeddingSchema

router = APIRouter()


@router.post(
    "/embeddings",
    summary="Отправить событие о помещении сведений об услуге в закладки",
    description="Отправка события в брокер сообщений",
    tags=["События"]
)
async def send_bookmarked_event(
        video: VideoEmbeddingSchema,
        db_service: DBClientABC = Depends(),
        embedding_merger: EmbeddingMergerABC = Depends(),
) -> None:
    db_service.save_embedding(
        embedding=video.embedding,
        properties=VideoProperties(
            external_id=video.video_id,
            link=video.video_url,
            text=video.text,
            valid=video.valid,
            description=video.description
        ),
        collection_name=video.collection
    )

    if video.collection == settings.QDRANT_COLLECTION_NAMES["TAGS_COLLECTION"]:
        return

    existing_embedding = embedding_merger.find_embedding(video.collection, video.embedding, video.video_id)

    if existing_embedding:
        merged_embedding = embedding_merger.merge_embeddings(existing_embedding)
        db_service.save_embedding(
            embedding=merged_embedding,
            properties=VideoProperties(
                external_id=video.video_id,
                link=video.video_url,
                text=video.text,
                valid=video.valid,
                description=video.description
            ),
            collection_name=settings.MERGED_COLLECTION_NAME
        )
