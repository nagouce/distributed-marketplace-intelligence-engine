-- Ingestion & Processing Pipeline Tables

CREATE TABLE IF NOT EXISTS fila_postagem (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    posicao         INTEGER NOT NULL,
    marketplace     TEXT NOT NULL,
    produto_id      TEXT NOT NULL,
    titulo          TEXT NOT NULL,
    preco_atual     REAL NOT NULL,
    preco_original  REAL,
    desconto_pct    REAL DEFAULT 0,
    comissao_pct    REAL DEFAULT 0,
    comissao_reais  REAL DEFAULT 0,
    score           REAL DEFAULT 0,
    imagem_url      TEXT,
    url_afiliado    TEXT,
    status          TEXT DEFAULT 'pendente',
    data_fila       TEXT DEFAULT (date('now','localtime')),
    enviado_em      TEXT,
    criado_em       TEXT DEFAULT (datetime('now','localtime')),
    corredor        TEXT,
    ala             TEXT,
    marca           TEXT,
    UNIQUE(produto_id, marketplace, data_fila)
);

CREATE TABLE IF NOT EXISTS historico_disparos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    marketplace     TEXT NOT NULL,
    produto_id      TEXT NOT NULL,
    titulo          TEXT NOT NULL,
    modelo_hash     TEXT NOT NULL,
    enviado_em      TEXT DEFAULT (datetime('now','localtime')),
    comunidade_jid  TEXT
);

CREATE TABLE IF NOT EXISTS status_diario (
    data               TEXT PRIMARY KEY,
    total_enviados     INTEGER DEFAULT 0,
    shopee_enviados    INTEGER DEFAULT 0,
    ml_enviados        INTEGER DEFAULT 0,
    amazon_enviados    INTEGER DEFAULT 0,
    pausado            INTEGER DEFAULT 0,
    ultima_atualizacao TEXT DEFAULT (datetime('now','localtime'))
);

-- Strategic Composite Indexes for Sub-millisecond Daemon Polling
CREATE INDEX IF NOT EXISTS idx_fila_status ON fila_postagem(status, data_fila);
CREATE INDEX IF NOT EXISTS idx_fila_posicao ON fila_postagem(posicao, data_fila);
CREATE INDEX IF NOT EXISTS idx_hist_modelo ON historico_disparos(modelo_hash, enviado_em);
CREATE INDEX IF NOT EXISTS idx_hist_produto ON historico_disparos(produto_id, marketplace, enviado_em);
