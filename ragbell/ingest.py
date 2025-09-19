from pathlib import Path

from langchain.schema import Document

from ragbell import get_loader
from ragbell.loadyaml import load_yaml


def loaders_instructions(yaml_path: str):

    if not Path(yaml_path).is_file():
        raise FileNotFoundError(f"{yaml_path} not found.")

    instructions = load_yaml(yaml_path)

    loaders = instructions.get("loaders", None)
    if loaders is None:
        raise ValueError("No loaders found in loaders.yaml")
    if not isinstance(loaders, list):
        raise ValueError("Loaders should be a list in loaders.yaml")
    return loaders


def load_docs(yaml_path: str):

    loaders = loaders_instructions(yaml_path)

    docs = []
    for loader in loaders:
        loader_type = loader.get("type", None)
        if loader_type is None:
            raise ValueError("Loader type is required in loaders.yaml")
        params = loader.get("params", None)
        if params is None:
            raise ValueError("Loader params are required in loaders.yaml")
        loader_instance = get_loader(loader_type, **params)
        doc = loader_instance.load()
        docs.extend(doc)
    return docs


def persist_docs(docs: list[Document], db: IContentDB):
    try:
        for doc in docs:
            metadata = doc.metadata if doc.metadata else {}
            db.insert(doc.page_content, metadata)
    finally:
        db.close()
    print(f"Persisted {len(docs)} documents.")
