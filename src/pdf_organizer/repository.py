from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3

from .workspace import normalize_workspace_pdf_path, resolve_workspace_pdf_path


@dataclass(slots=True)
class PdfRecord:
    id: int
    title: str
    description: str
    relative_path: str
    tags: list[str]
    file_exists: bool

    @property
    def status(self) -> str:
        return "Available" if self.file_exists else "Missing"


class PdfRepository:
    def __init__(self, connection: sqlite3.Connection, workspace_root: Path):
        self.connection = connection
        self.workspace_root = workspace_root.resolve()

    def add_pdf(self, file_path: str | Path) -> PdfRecord:
        relative_path = normalize_workspace_pdf_path(file_path, self.workspace_root)
        title = Path(relative_path).stem
        cursor = self.connection.execute(
            "INSERT INTO pdf_records (title, relative_path) VALUES (?, ?)",
            (title, relative_path.as_posix()),
        )
        self.connection.commit()
        return self.get_record(cursor.lastrowid)

    def list_records(self, search: str = "", include_missing: bool = True) -> list[PdfRecord]:
        search_term = f"%{search.strip().lower()}%"
        rows = self.connection.execute(
            """
            SELECT DISTINCT r.id, r.title, r.description, r.relative_path
            FROM pdf_records r
            LEFT JOIN record_tags rt ON rt.record_id = r.id
            LEFT JOIN tags t ON t.id = rt.tag_id
            WHERE (
                ? = '%%'
                OR lower(r.title) LIKE ?
                OR lower(r.description) LIKE ?
                OR lower(COALESCE(t.name, '')) LIKE ?
            )
            ORDER BY lower(r.title), r.id
            """,
            (search_term, search_term, search_term, search_term),
        ).fetchall()
        records = [self._row_to_record(row) for row in rows]
        if include_missing:
            return records
        return [record for record in records if record.file_exists]

    def get_record(self, record_id: int) -> PdfRecord:
        row = self.connection.execute(
            "SELECT id, title, description, relative_path FROM pdf_records WHERE id = ?",
            (record_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"Record {record_id} not found")
        return self._row_to_record(row)

    def update_record(self, record_id: int, title: str, description: str) -> PdfRecord:
        self.connection.execute(
            "UPDATE pdf_records SET title = ?, description = ? WHERE id = ?",
            (title.strip(), description.strip(), record_id),
        )
        self.connection.commit()
        return self.get_record(record_id)

    def delete_record(self, record_id: int) -> None:
        self.connection.execute("DELETE FROM pdf_records WHERE id = ?", (record_id,))
        self.connection.commit()

    def create_tag(self, name: str) -> list[str]:
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("Tag name cannot be empty.")
        self.connection.execute("INSERT INTO tags (name) VALUES (?)", (cleaned,))
        self.connection.commit()
        return self.list_tags()

    def list_tags(self) -> list[str]:
        rows = self.connection.execute(
            "SELECT name FROM tags ORDER BY lower(name), id"
        ).fetchall()
        return [row["name"] for row in rows]

    def delete_tag(self, name: str) -> list[str]:
        self.connection.execute("DELETE FROM tags WHERE lower(name) = lower(?)", (name,))
        self.connection.commit()
        return self.list_tags()

    def set_record_tags(self, record_id: int, tag_names: list[str]) -> PdfRecord:
        cleaned_names = sorted({name.strip() for name in tag_names if name.strip()}, key=str.lower)
        self.connection.execute("DELETE FROM record_tags WHERE record_id = ?", (record_id,))
        for name in cleaned_names:
            tag_row = self.connection.execute(
                "SELECT id FROM tags WHERE lower(name) = lower(?)", (name,)
            ).fetchone()
            if tag_row is None:
                cursor = self.connection.execute("INSERT INTO tags (name) VALUES (?)", (name,))
                tag_id = cursor.lastrowid
            else:
                tag_id = tag_row["id"]
            self.connection.execute(
                "INSERT OR IGNORE INTO record_tags (record_id, tag_id) VALUES (?, ?)",
                (record_id, tag_id),
            )
        self.connection.commit()
        return self.get_record(record_id)

    def _row_to_record(self, row: sqlite3.Row) -> PdfRecord:
        tags = self._record_tags(row["id"])
        resolved_path = resolve_workspace_pdf_path(row["relative_path"], self.workspace_root)
        return PdfRecord(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            relative_path=row["relative_path"],
            tags=tags,
            file_exists=resolved_path.exists(),
        )

    def _record_tags(self, record_id: int) -> list[str]:
        rows = self.connection.execute(
            """
            SELECT t.name
            FROM tags t
            INNER JOIN record_tags rt ON rt.tag_id = t.id
            WHERE rt.record_id = ?
            ORDER BY lower(t.name), t.id
            """,
            (record_id,),
        ).fetchall()
        return [row["name"] for row in rows]

