from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class TaskStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    assigned_agent TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    approval_required INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            conn.commit()

    def create_task(self, task_id: str, description: str, assigned_agent: str = None, priority: str = "normal") -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO tasks (task_id, description, status, priority, assigned_agent, created_at, updated_at, result, error, approval_required)
                VALUES (?, ?, 'pending', ?, ?, datetime('now'), datetime('now'), '', '', 0)
                """,
                (task_id, description, priority, assigned_agent),
            )
            conn.commit()
        return self.get_task(task_id)

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT task_id, description, status, priority, assigned_agent, created_at, updated_at, result, error, approval_required FROM tasks WHERE task_id = ?",
                (task_id,),
            ).fetchone()
        if row is None:
            return None
        return {
            "task_id": row[0],
            "description": row[1],
            "status": row[2],
            "priority": row[3],
            "assigned_agent": row[4],
            "created_at": row[5],
            "updated_at": row[6],
            "result": row[7],
            "error": row[8],
            "approval_required": row[9],
        }

    def list_tasks(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT task_id, description, status, priority, assigned_agent, created_at, updated_at, result, error, approval_required FROM tasks ORDER BY created_at DESC"
            ).fetchall()
        return [
            {
                "task_id": row[0],
                "description": row[1],
                "status": row[2],
                "priority": row[3],
                "assigned_agent": row[4],
                "created_at": row[5],
                "updated_at": row[6],
                "result": row[7],
                "error": row[8],
                "approval_required": row[9],
            }
            for row in rows
        ]

    def update_status(self, task_id: str, status: str, result: str = None, error: str = None, approval_required: int = None):
        with sqlite3.connect(self.db_path) as conn:
            if result is not None:
                conn.execute("UPDATE tasks SET result = ?, updated_at = datetime('now') WHERE task_id = ?", (result, task_id))
            if error is not None:
                conn.execute("UPDATE tasks SET error = ?, updated_at = datetime('now') WHERE task_id = ?", (error, task_id))
            if approval_required is not None:
                conn.execute("UPDATE tasks SET approval_required = ?, updated_at = datetime('now') WHERE task_id = ?", (approval_required, task_id))
            conn.execute("UPDATE tasks SET status = ?, updated_at = datetime('now') WHERE task_id = ?", (status, task_id))
            conn.commit()

    def assign_agent(self, task_id: str, assigned_agent: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE tasks SET assigned_agent = ?, updated_at = datetime('now') WHERE task_id = ?", (assigned_agent, task_id))
            conn.commit()

    def delete_task(self, task_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            conn.commit()
