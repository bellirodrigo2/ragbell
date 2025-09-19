import json
import os
import sqlite3

from dotenv import load_dotenv

from ..interfaces import IContentDB, IEmbeddingDB, ISplittedContentDB


def get_create_statement():
    load_dotenv()
    sql_path = os.getenv("SQLITE_CREATE_PATH", "src/sqlitedb/sqlitecreate.sql")

    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    return sql_script


class SQLiteContentDB(IContentDB):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._create_tables()

    def _create_tables(self):
        sql_script = get_create_statement()
        self.conn.executescript(sql_script)
        self.conn.commit()

    def insert(self, content: str, metadata: dict):
        """
        Insere um registro na tabela 'content' e atualiza a FTS.
        """
        metadata_text = json.dumps(metadata)

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO content (content, metadata) VALUES (?, ?)",
            (content, metadata_text),
        )
        row_id = cursor.lastrowid

        # Atualiza a tabela FTS
        cursor.execute(
            "INSERT INTO content_fts(rowid, content) VALUES (?, ?)",
            (row_id, content),
        )
        cursor.close()
        self.conn.commit()
        return row_id

    def search_fts(self, query: str, limit: int = 10):
        """
        Busca registros usando FTS apenas no campo 'content'.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT c.id, c.content, c.metadata
            FROM content c
            JOIN content_fts f ON c.id = f.rowid
            WHERE f MATCH ?
            LIMIT ?
            """,
            (query, limit),
        )
        results = cursor.fetchall()
        cursor.close()
        return [
            {
                "id": r[0],
                "content": r[1],
                "metadata": json.loads(r[2]),
            }
            for r in results
        ]

    def close(self):
        self.conn.close()


class SQLiteSplittedContentDB(ISplittedContentDB):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._create_tables()

    def _create_tables(self):
        sql_script = get_create_statement()
        self.conn.executescript(sql_script)
        self.conn.commit()

    def insert(self, content_id: int, content: str, collection: str):
        """
        Insere um registro na tabela 'splitted_content'.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO splitted_content (content_id, content, collection) VALUES (?, ?, ?)",
            (content_id, content, collection),
        )
        row_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return row_id

    def get_all(self, content_id: int = None, collection: str = None):
        """
        Retorna registros de splitted_content filtrados por content_id ou collection.
        """
        cursor = self.conn.cursor()
        query = (
            "SELECT id, content_id, content, collection FROM splitted_content WHERE 1=1"
        )
        params = []

        if content_id is not None:
            query += " AND content_id = ?"
            params.append(content_id)

        if collection is not None:
            query += " AND collection = ?"
            params.append(collection)

        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()

        return [
            {
                "id": r[0],
                "content_id": r[1],
                "content": r[2],
                "collection": r[3],
            }
            for r in results
        ]

    def close(self):
        self.conn.close()


class SQLiteEmbeddingDB(IEmbeddingDB):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._create_tables()

    def _create_tables(self):
        sql_script = get_create_statement()
        self.conn.executescript(sql_script)
        self.conn.commit()

    def insert(self, splitted_content_id: int, embedding: list):
        """
        Insere um embedding associado a um splitted_content_id.
        """
        embedding_text = json.dumps(embedding)

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO embeddings (splitted_content_id, embedding) VALUES (?, ?)",
            (splitted_content_id, embedding_text),
        )
        row_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return row_id

    def get_embeddings(self, splitted_content_id: int = None):
        """
        Retorna embeddings filtrados opcionalmente por splitted_content_id.
        """
        cursor = self.conn.cursor()
        query = "SELECT splitted_content_id, embedding FROM embeddings WHERE 1=1"
        params = []

        if splitted_content_id is not None:
            query += " AND splitted_content_id = ?"
            params.append(splitted_content_id)

        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()

        return [
            {
                "splitted_content_id": r[0],
                "embedding": json.loads(r[1]),
            }
            for r in results
        ]

    def close(self):
        self.conn.close()
