from __future__ import annotations

import base64
import binascii
import mimetypes
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Dict, List


ALLOWED_EXTENSIONS = {
    ".csv", ".tsv", ".xlsx", ".xls", ".ods", ".pdf", ".doc", ".docx",
    ".txt", ".md", ".json", ".xml", ".html", ".png", ".jpg", ".jpeg", ".webp",
}
MAX_FILE_BYTES = 25 * 1024 * 1024


class CRMFileStore:
    def __init__(self, db_path: Path, root_dir: Path):
        self.db_path = Path(db_path)
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS crm_files (
                    file_id TEXT PRIMARY KEY,
                    record_id TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    path TEXT NOT NULL,
                    content_type TEXT,
                    size_bytes INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def save_bytes(self, record_id: str, filename: str, content: bytes) -> Dict[str, Any]:
        safe_name = Path(str(filename)).name
        extension = Path(safe_name).suffix.lower()
        if not safe_name or extension not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file format. Allowed formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
        if not content:
            raise ValueError("The uploaded file is empty.")
        if len(content) > MAX_FILE_BYTES:
            raise ValueError("Files must be 25 MB or smaller.")
        file_id = f"file-{uuid.uuid4().hex[:8]}"
        target_dir = self.root_dir / record_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{file_id}-{safe_name}"
        target.write_bytes(content)
        content_type = mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO crm_files (file_id, record_id, filename, path, content_type, size_bytes, created_at) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))",
                (file_id, record_id, safe_name, str(target), content_type, len(content)),
            )
            conn.commit()
        return self.get_file(file_id)

    def save_base64(self, record_id: str, filename: str, encoded: str) -> Dict[str, Any]:
        try:
            content = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("Invalid base64 file content.") from exc
        return self.save_bytes(record_id, filename, content)

    def get_file(self, file_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM crm_files WHERE file_id = ?", (file_id,)).fetchone()
        if row is None:
            raise KeyError(f"CRM file not found: {file_id}")
        return self._row_to_file(row)

    def list_files(self, record_id: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM crm_files WHERE record_id = ? ORDER BY created_at DESC", (record_id,)).fetchall()
        return [self._row_to_file(row) for row in rows]

    @staticmethod
    def _row_to_file(row: tuple) -> Dict[str, Any]:
        keys = ["file_id", "record_id", "filename", "path", "content_type", "size_bytes", "created_at"]
        return dict(zip(keys, row))