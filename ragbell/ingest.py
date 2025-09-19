from pathlib import Path
from typing import Any

from langchain.schema import Document

from ragbell.loaders import get_loader
from ragbell.loadyaml import load_yaml
from ragbell.splitters import get_splitter
from ragbell.sql_interface import IContentDB
from ragbell.sqlitedb.sqliteembdb import ISplittedContentDB, SQLiteContentDB


def get_config(yaml_path: str, type_: str) -> list[dict]:

    if not Path(yaml_path).is_file():
        raise FileNotFoundError(f"{yaml_path} not found.")

    config = load_yaml(yaml_path)

    config_list = config.get(type_, None)

    if config_list is None:
        raise ValueError(f"No {type_} found in loaders.yaml")
    if not isinstance(config_list, list):
        raise ValueError(f"{type_.capitalize()} should be a list in loaders.yaml")
    return config_list


def iter_config_list(config_list: list[dict], extra_key: str | None = None):

    for config in config_list:
        proc_type = config.get("type", None)
        if proc_type is None:
            raise ValueError("Processor type is required in config")
        params = config.get("params", None)
        if params is None:
            raise ValueError("Processor params are required in config")
        extra_key = config.get(extra_key, None)

        yield proc_type, params, extra_key


# -------------- LOADERS -------------------------


def load_docs(yaml_path: str):

    loaders = get_config(yaml_path, "loaders")

    docs = []
    for loader_type, params, _ in iter_config_list(loaders):
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


# -------------- SPLITTERS -------------------------


def split_docs(
    yaml_path: str, db: ISplittedContentDB, metadata_key: str, metadata_value: Any
):

    splitters = get_config(yaml_path, "splitters")

    docs = db.read_by_metadata(metadata_key, metadata_value)

    for splitter_type, params, collection in iter_config_list(splitters, "collection"):
        splitter_instance = get_splitter(splitter_type, **params)

        for doc_id, content in docs:
            splitted_docs = splitter_instance.split_text(content)
            for splitted_doc in splitted_docs:
                db.insert(doc_id, splitted_doc, collection)
