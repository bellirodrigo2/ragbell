-- Tabela principal de embeddings
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    metadata TEXT NOT NULL,
    embedding TEXT NOT NULL,  -- lista de floats convertida para string
    collection TEXT NOT NULL
);

-- Tabela virtual FTS5 para busca textual
CREATE VIRTUAL TABLE IF NOT EXISTS embeddings_fts USING fts5(
    content,
    metadata,
    content='embeddings',
    content_rowid='id'
);
