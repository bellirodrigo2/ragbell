-- Tabela principal de conteúdo
CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    metadata TEXT NOT NULL
);

-- Conteúdo fragmentado
CREATE TABLE IF NOT EXISTS splitted_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER,
    content TEXT NOT NULL,
    collection TEXT NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE
);

-- Embeddings (1:1 com splitted_content)
CREATE TABLE IF NOT EXISTS embeddings (
    splitted_content_id INTEGER PRIMARY KEY,
    embedding TEXT NOT NULL,
    FOREIGN KEY (splitted_content_id) REFERENCES splitted_content(id) ON DELETE CASCADE
);

-- Busca textual
CREATE VIRTUAL TABLE IF NOT EXISTS splitted_content_fts USING fts5(
    content,
    content='splitted_content',
    content_rowid='id'
);
