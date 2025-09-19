import pytest

from ragbell import SQLiteContentDB, load_docs, persist_docs


@pytest.fixture
def get_db():

    db = SQLiteContentDB(":memory:")
    yield db


yaml_loaders_path = "tests/loaders.yaml"


def test_ingest_content(get_db):

    db = get_db

    docs = load_docs(yaml_loaders_path)
    persist_docs(docs, db)

    count = db.count()

    assert count == 42

    content = db.read_by_metadata("source", "./tests/data/es.pdf")

    assert len(content) == 40
