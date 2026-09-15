from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    assigned_agent: Optional[str] = None
    priority: str = "normal"
    result: Optional[Any] = None
    error: Optional[str] = None
    approval_required: bool = False


class TaskManager:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def create_task(self, title: str, description: str, assigned_agent: Optional[str] = None, priority: str = "normal") -> Task:
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task = Task(
            id=task_id,
            title=title,
            description=description,
            assigned_agent=assigned_agent,
            priority=priority,
        )
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def update_task(self, task_id: str, *, status: Optional[str] = None, result: Optional[Any] = None, error: Optional[str] = None, approval_required: Optional[bool] = None, assigned_agent: Optional[str] = None) -> Task:
        task = self._tasks[task_id]
        if status is not None:
            task.status = status
        if result is not None:
            task.result = result
        if error is not None:
            task.error = error
        if approval_required is not None:
            task.approval_required = approval_required
        if assigned_agent is not None:
            task.assigned_agent = assigned_agent
        task.updated_at = datetime.now(timezone.utc).isoformat()
        return task

    def pending_approvals(self) -> List[Task]:
        return [task for task in self._tasks.values() if task.status in {"waiting_approval", "awaiting_approval"}]
