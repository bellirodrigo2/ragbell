from typing import Protocol


class IEmbeddingDB(Protocol):

    def insert(
        self, content: str, metadata: dict, embedding: list, collection: str
    ): ...

    def search_fts(self, query: str, limit: int = 10): ...

    def close(self): ...


class ISplitter(Protocol):

    def split(self, text: str) -> list[str]: ...


class ILoader(Protocol):

    def load(self, path: str) -> list[dict]: ...

    def _filename(self, path: str) -> str:
        from pathlib import Path

        return Path(path).stem


class IEmbeddingModel(Protocol):

    def embed(self, text: str) -> list[float]: ...
