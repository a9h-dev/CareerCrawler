JOBS_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT    NOT NULL UNIQUE,
    title       TEXT    NOT NULL,
    company     TEXT,
    location    TEXT,
    salary      TEXT,
    source      TEXT    NOT NULL,
    posted_at   TEXT,
    crawled_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    is_active   INTEGER NOT NULL DEFAULT 1
);
"""

JOBS_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_jobs_source  ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_crawled ON jobs(crawled_at);
CREATE INDEX IF NOT EXISTS idx_jobs_active  ON jobs(is_active);
"""

CRAWL_RUNS_TABLE = """
CREATE TABLE IF NOT EXISTS crawl_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source      TEXT    NOT NULL,
    started_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT,
    jobs_found  INTEGER DEFAULT 0,
    jobs_new    INTEGER DEFAULT 0,
    status      TEXT    DEFAULT 'running',
    error_msg   TEXT
);
"""

ALL_DDL = [JOBS_TABLE, JOBS_INDEXES, CRAWL_RUNS_TABLE]
