-- Tabela principal de conteúdo
CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    metadata TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS splitted_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER,
    content TEXT NOT NULL,
    collection TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE
);

-- Tabela de embeddings
CREATE TABLE IF NOT EXISTS embeddings (
    splitted_content_id INTEGER,
    embedding TEXT NOT NULL,
    FOREIGN KEY (splitted_content_id) REFERENCES splitted_content(id) ON DELETE CASCADE
);

-- Tabela virtual FTS5 para busca textual apenas em 'content'
CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
    content,
    content='content',
    content_rowid='id'
);
