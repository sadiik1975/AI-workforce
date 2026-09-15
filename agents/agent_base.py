from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAgent(ABC):
    name = "base_agent"
    description = "Base workload agent"
    capabilities: list[str] = []

    def __init__(self, registry: Optional[Any] = None):
        self.registry = registry

    def validate_input(self, task: Dict[str, Any]) -> str:
        if not isinstance(task, dict):
            raise TypeError("Task payload must be a dictionary.")

        text = str(task.get("description") or task.get("title") or "").strip()
        if not text:
            raise ValueError("Task description is required.")
        return text

    def handle_error(self, task: Dict[str, Any], exc: Exception) -> Dict[str, Any]:
        task_id = task.get("task_id") or task.get("id")
        return {
            "status": "failed",
            "agent": self.name,
            "task_id": task_id,
            "error": str(exc),
        }

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        ...

    def return_result(self, status: str = "completed", result: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> Dict[str, Any]:
        payload = result or {}
        response = {
            "status": status,
            "agent": self.name,
            "result": payload,
        }
        if error:
            response["error"] = error
        return response
