from typing import Protocol


class IEmbeddingDB(Protocol):

    def insert(
        self, content: str, metadata: dict, embedding: list, collection: str
    ): ...

    def search_fts(self, query: str, limit: int = 10): ...

    def close(self): ...


class ISplitter(Protocol):

    def execute(self, text: str) -> list[str]: ...


class ILoader(Protocol):

    def execute(self, path: str) -> list[dict]: ...


class IEmbeddingModel(Protocol):

    def execute(self, text: str) -> list[float]: ...
