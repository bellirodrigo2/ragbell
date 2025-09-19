from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings

EMBEDDING_MAP = {
    "openai": OpenAIEmbeddings,
    "huggingface": HuggingFaceEmbeddings,
}


def get_embedding_model(embedding_type: str, **kwargs):
    embedding_class = EMBEDDING_MAP.get(embedding_type)
    if not embedding_class:
        raise ValueError(f"Embedding type '{embedding_type}' is not supported.")
    return embedding_class(**kwargs)
