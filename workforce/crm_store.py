from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path
from typing import Any, Dict, List


class CRMStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS crm_records (
                    record_id TEXT PRIMARY KEY,
                    record_type TEXT NOT NULL,
                    company TEXT NOT NULL,
                    contact_name TEXT,
                    website TEXT,
                    industry TEXT,
                    location TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    sales_stage TEXT NOT NULL DEFAULT 'NEW LEAD',
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_record(
        self,
        company: str,
        record_type: str = "company",
        contact_name: str | None = None,
        website: str | None = None,
        industry: str | None = None,
        location: str | None = None,
        notes: str | None = None,
    ) -> Dict[str, Any]:
        company = str(company).strip()
        if not company:
            raise ValueError("Company name is required.")
        record_id = f"crm-{uuid.uuid4().hex[:8]}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO crm_records
                (record_id, record_type, company, contact_name, website, industry, location, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """,
                (record_id, record_type, company, contact_name, website, industry, location, notes),
            )
            conn.commit()
        return self.get_record(record_id)

    def get_record(self, record_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM crm_records WHERE record_id = ?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(f"CRM record not found: {record_id}")
        return self._row_to_record(row)

    def list_records(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM crm_records ORDER BY created_at DESC").fetchall()
        return [self._row_to_record(row) for row in rows]

    @staticmethod
    def _row_to_record(row: tuple) -> Dict[str, Any]:
        keys = [
            "record_id", "record_type", "company", "contact_name", "website",
            "industry", "location", "status", "sales_stage", "notes",
            "created_at", "updated_at",
        ]
        return dict(zip(keys, row))