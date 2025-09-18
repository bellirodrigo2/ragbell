from ..interfaces import IEmbeddingModel
from .huggingface import HuggingFaceModel
from .openai import OpenAIModel

EMBEDDING_MAP = {
    "openai": OpenAIModel,
    "huggingface": HuggingFaceModel,
}


def get_embedding_model(embedding_type: str, **kwargs) -> IEmbeddingModel:
    embedding_class = EMBEDDING_MAP.get(embedding_type)
    if not embedding_class:
        raise ValueError(f"Embedding type '{embedding_type}' is not supported.")
    return embedding_class(**kwargs)
