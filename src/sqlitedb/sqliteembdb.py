import os
import sqlite3
import json
from .. import IEmbeddingDB
from dotenv import load_dotenv

def get_create_statement():
    load_dotenv()
    sql_path = os.getenv("SQLITE_CREATE_PATH", "src/sqlitedb/sqlite_create.sql")
    
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    return sql_script

class SQLiteEmbDB(IEmbeddingDB):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def _create_tables(self):
        sql_script = get_create_statement()
        self.conn.executescript(sql_script)
        self.conn.commit()

    def insert(self, content: str, metadata: dict, embedding: list, collection: str):
        embedding_text = json.dumps(embedding)
        metadata_text = json.dumps(metadata)

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO embeddings (content, metadata, embedding, collection) VALUES (?, ?, ?, ?)",
            (content, metadata_text, embedding_text, collection)
        )
        row_id = cursor.lastrowid

        # Atualiza a tabela FTS
        cursor.execute(
            "INSERT INTO embeddings_fts(rowid, content, metadata) VALUES (?, ?, ?)",
            (row_id, content, metadata_text)
        )
        cursor.close()
        self.conn.commit()
        return row_id

    def search_fts(self, query: str, limit: int = 10):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT e.id, e.content, e.metadata, e.embedding, e.collection
            FROM embeddings e
            JOIN embeddings_fts f ON e.id = f.rowid
            WHERE f MATCH ?
            LIMIT ?
            """,
            (query, limit)
        )
        results = cursor.fetchall()
        cursor.close()
        return [
            {
                "id": r[0],
                "content": r[1],
                "metadata": json.loads(r[2]),
                "embedding": json.loads(r[3]),
                "collection": r[4]
            }
            for r in results
        ]

    def close(self):
        self.conn.close()
