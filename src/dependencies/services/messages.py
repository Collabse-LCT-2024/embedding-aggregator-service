from functools import cache

from fastapi import Depends

from src.database.base import DBClientABC
from src.database.qdrant_client import QdrantDBClient
from src.embedding_merger import EmbeddingMerger, EmbeddingMergerABC
from src.dependencies.registrator import add_factory_to_mapper


@add_factory_to_mapper(DBClientABC)
@cache
def create_db_service() -> QdrantDBClient:
    return QdrantDBClient()


@add_factory_to_mapper(EmbeddingMergerABC)
@cache
def create_embedding_merger(db_client: DBClientABC = Depends()) -> EmbeddingMerger:
    return EmbeddingMerger(db_client=db_client)
