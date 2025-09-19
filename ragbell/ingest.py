from pathlib import Path

from langchain.schema import Document

from ragbell.loaders import get_loader
from ragbell.loadyaml import load_yaml
from ragbell.sql_interface import IContentDB
from ragbell.sqlitedb.sqliteembdb import SQLiteContentDB


def loaders_config(yaml_path: str):

    if not Path(yaml_path).is_file():
        raise FileNotFoundError(f"{yaml_path} not found.")

    config = load_yaml(yaml_path)

    loaders = config.get("loaders", None)
    if loaders is None:
        raise ValueError("No loaders found in loaders.yaml")
    if not isinstance(loaders, list):
        raise ValueError("Loaders should be a list in loaders.yaml")
    return loaders


def load_docs(yaml_path: str):

    loaders = loaders_config(yaml_path)

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
    for doc in docs:
        metadata = doc.metadata if doc.metadata else {}
        db.insert(doc.page_content, metadata)


def ingest_docs(yaml_path: str, db_path: str | None):

    if db_path is None:
        import os

        from dotenv import load_dotenv

        load_dotenv()
        db_path = os.getenv("SQLITE_DB_PATH", None)
        if db_path is None:
            raise ValueError("SQLITE_DB_PATH not set in .env")

    db = SQLiteContentDB(db_path)
    docs = load_docs(yaml_path)
    persist_docs(docs, db)
    db.close()
