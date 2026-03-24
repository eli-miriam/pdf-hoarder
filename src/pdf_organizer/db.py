from __future__ import annotations

import sqlite3
from pathlib import Path

from .workspace import database_path, get_workspace_root


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS pdf_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    relative_path TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS record_tags (
    record_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (record_id, tag_id),
    FOREIGN KEY (record_id) REFERENCES pdf_records(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS pdf_records_updated_at
AFTER UPDATE ON pdf_records
FOR EACH ROW
BEGIN
    UPDATE pdf_records
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;
"""


def connect(root: Path | None = None) -> sqlite3.Connection:
    db_path = database_path(root or get_workspace_root())
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection

