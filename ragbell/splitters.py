from typing import Any

from langchain.text_splitter import (
    CharacterTextSplitter,
    NLTKTextSplitter,
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
    SpacyTextSplitter,
    TokenTextSplitter,
)
from langchain_experimental.text_splitter import SemanticChunker


def SemanticSplitter(**kwargs: Any) -> SemanticChunker:

    embedder = kwargs.pop("embedder", None)
    model_name = kwargs.pop("model_name", None)

    if not embedder or not model_name:
        raise ValueError(
            "Both 'embedder' and 'model_name' must be provided for SemanticSplitter."
        )

    embedder = embedder.lower()
    if embedder == "openai":
        from langchain_openai.embeddings import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(model=model_name)
        return SemanticChunker(embeddings=embeddings, **kwargs)

    if embedder == "huggingface":
        from langchain_huggingface_embeddings import HuggingFaceEmbeddings

        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        return SemanticChunker(embeddings=embeddings, **kwargs)

    raise ValueError(f"Embedder '{embedder}' is not supported for SemanticSplitter.")


SPLITTER_MAP = {
    "character": CharacterTextSplitter,
    "recursive": RecursiveCharacterTextSplitter,
    "token": TokenTextSplitter,
    "nltk": NLTKTextSplitter,
    "spacy": SpacyTextSplitter,
    "sentence_transformers": SentenceTransformersTokenTextSplitter,
    "semantic": SemanticSplitter,
}


def get_splitter(splitter_type: str, **kwargs: Any):
    splitter_class = SPLITTER_MAP.get(splitter_type)

    if not splitter_class:
        raise ValueError(f"Splitter type '{splitter_type}' is not supported.")
    return splitter_class(**kwargs)
