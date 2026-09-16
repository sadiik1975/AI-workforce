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
                    phone TEXT,
                    email TEXT,
                    website TEXT,
                    industry TEXT,
                    location TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    sales_stage TEXT NOT NULL DEFAULT 'NEW LEAD',
                    notes TEXT,
                    source TEXT NOT NULL DEFAULT 'manual entry (unverified)',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            columns = {row[1] for row in conn.execute("PRAGMA table_info(crm_records)")}
            for name, definition in {
                "phone": "TEXT",
                "email": "TEXT",
                "source": "TEXT NOT NULL DEFAULT 'manual entry (unverified)'",
            }.items():
                if name not in columns:
                    conn.execute(f"ALTER TABLE crm_records ADD COLUMN {name} {definition}")
            conn.execute("UPDATE crm_records SET status = 'unverified' WHERE source IS NULL OR source = 'manual entry (unverified)'")
            conn.commit()

    def add_record(
        self,
        company: str,
        record_type: str = "company",
        contact_name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        website: str | None = None,
        industry: str | None = None,
        location: str | None = None,
        notes: str | None = None,
        source: str = "manual entry (unverified)",
    ) -> Dict[str, Any]:
        company = str(company).strip()
        if not company:
            raise ValueError("Company name is required.")
        record_id = f"crm-{uuid.uuid4().hex[:8]}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO crm_records
                (record_id, record_type, company, contact_name, phone, email, website, industry, location, status, notes, source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'unverified', ?, ?, datetime('now'), datetime('now'))
                """,
                (record_id, record_type, company, contact_name, phone, email, website, industry, location, notes, source),
            )
            conn.commit()
        return self.get_record(record_id)

    def get_record(self, record_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT record_id, record_type, company, contact_name, phone, email, website,
                       industry, location, status, sales_stage, notes, created_at, updated_at, source
                FROM crm_records WHERE record_id = ?
                """,
                (record_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"CRM record not found: {record_id}")
        return self._row_to_record(row)

    def list_records(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT record_id, record_type, company, contact_name, phone, email, website,
                       industry, location, status, sales_stage, notes, created_at, updated_at, source
                FROM crm_records ORDER BY created_at DESC
                """
            ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def update_record(self, record_id: str, **fields: Any) -> Dict[str, Any]:
        allowed = {
            "record_type", "company", "contact_name", "phone", "email", "website",
            "industry", "location", "status", "sales_stage", "notes", "source",
        }
        updates = {name: value for name, value in fields.items() if name in allowed}
        if "company" in updates:
            updates["company"] = str(updates["company"]).strip()
            if not updates["company"]:
                raise ValueError("Company name is required.")
        if not updates:
            return self.get_record(record_id)
        assignments = ", ".join(f"{name} = ?" for name in updates)
        values = list(updates.values()) + [record_id]
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                f"UPDATE crm_records SET {assignments}, updated_at = datetime('now') WHERE record_id = ?",
                values,
            )
            if cursor.rowcount == 0:
                raise KeyError(f"CRM record not found: {record_id}")
            conn.commit()
        return self.get_record(record_id)

    def delete_record(self, record_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM crm_records WHERE record_id = ?", (record_id,))
            if cursor.rowcount == 0:
                raise KeyError(f"CRM record not found: {record_id}")
            conn.commit()

    @staticmethod
    def _row_to_record(row: tuple) -> Dict[str, Any]:
        keys = [
            "record_id", "record_type", "company", "contact_name", "phone", "email", "website",
            "industry", "location", "status", "sales_stage", "notes", "created_at", "updated_at", "source",
        ]
        return dict(zip(keys, row))