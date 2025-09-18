from typing import Any

from langchain_community.embeddings import HuggingFaceEmbeddings

from ..interfaces import IEmbeddingModel


class HuggingFaceModel(IEmbeddingModel):

    def __init__(self, model_name: str, **model_kwargs: Any):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name, model_kwargs=model_kwargs
        )

    def execute(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
