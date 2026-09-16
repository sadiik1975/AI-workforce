from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List

from agents.business_manager import BusinessManagerAgent
from agents.client_finder import ClientFinderAgent
from agents.funding import FundingAgent
from agents.marketing import MarketingAgent
from agents.research import ResearchAgent
from agents.sales import SalesAgent
from workforce.registry import AgentRegistry
from workforce.logger import WorkforceLogger
from workforce.task_store import TaskStore
from workforce.crm_store import CRMStore


class WorkforceApp:
    def __init__(self, root_dir: Path | None = None, data_dir: Path | None = None, logs_dir: Path | None = None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parent.parent
        self.data_dir = Path(data_dir) if data_dir else self.root_dir / "data"
        self.logs_dir = Path(logs_dir) if logs_dir else self.root_dir / "logs"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.registry = AgentRegistry()
        self.logger = WorkforceLogger(self.logs_dir)
        self.store = TaskStore(self.data_dir / "tasks.db")
        self.crm = CRMStore(self.data_dir / "tasks.db")
        self._agent_classes = {
            "business_manager": BusinessManagerAgent,
            "funding": FundingAgent,
            "client_finder": ClientFinderAgent,
            "sales": SalesAgent,
            "marketing": MarketingAgent,
            "research": ResearchAgent,
        }
        self.logger.log("system_started", "Been Ventures workforce started")

    def _get_agent_instance(self, agent_name: str):
        cls = self._agent_classes.get(agent_name)
        if cls is None:
            return None
        return cls(self.registry)

    def create_task(self, description: str, assigned_agent: str | None = None, priority: str = "normal") -> str:
        if not description or not str(description).strip():
            raise ValueError("Task description is required.")
        if assigned_agent is None:
            assigned_agent = self.registry.resolve_for_task(description)

        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task = self.store.create_task(task_id, description, assigned_agent=assigned_agent, priority=priority)
        self.logger.log("task_created", f"task={task['task_id']} agent={assigned_agent or 'unassigned'}")
        return task["task_id"]

    def log_event(self, event: str, message: str):
        self.logger.log(event, message)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        task = self.store.get_task(task_id)
        if task is None:
            raise KeyError(f"Task not found: {task_id}")
        return task

    def list_tasks(self) -> List[Dict[str, Any]]:
        return self.store.list_tasks()

    def add_crm_record(self, company: str, **fields: Any) -> Dict[str, Any]:
        record = self.crm.add_record(company, **fields)
        self.logger.log("crm_record_created", f"record={record['record_id']} company={record['company']}")
        return record

    def list_crm_records(self) -> List[Dict[str, Any]]:
        return self.crm.list_records()

    def update_task_status(self, task_id: str, status: str, result: str | None = None, error: str | None = None, approval_required: int | None = None):
        self.store.update_status(task_id, status, result=result, error=error, approval_required=approval_required)
        self.logger.log("task_status", f"task={task_id} status={status}")

    def record_failure(self, task_id: str, error: str):
        self.update_task_status(task_id, "failed", error=error)
        self.logger.log("task_failed", f"task={task_id} error={error}")

    def request_approval(self, task_id: str, reason: str):
        task = self.get_task(task_id)
        self.store.update_status(task_id, "waiting_approval", result=(task.get("result") or "Approval requested"), approval_required=1)
        self.logger.log("approval_requested", f"task={task_id} reason={reason}")

    def approve_task(self, task_id: str):
        task = self.get_task(task_id)
        result_text = task.get("result") or "Approved by owner"
        self.store.update_status(task_id, "completed", result=f"Approved by owner: {result_text}", approval_required=0)
        self.logger.log("approval_granted", f"task={task_id}")

    def reject_task(self, task_id: str):
        task = self.get_task(task_id)
        error_text = task.get("error") or "Rejected by owner"
        self.store.update_status(task_id, "failed", error=f"Rejected by owner: {error_text}", approval_required=0)
        self.logger.log("approval_rejected", f"task={task_id}")

    def list_pending_approvals(self):
        return [task for task in self.list_tasks() if task["status"] in {"waiting_approval", "awaiting_approval"}]

    def render_status(self):
        status = ["Been Ventures AI Workforce", "=======================", f"Registered agents: {len(self.registry.list_agents())}", f"Tasks: {len(self.list_tasks())}", "Status: running"]
        return "\n".join(status)

    def execute_agent_task(self, task_id: str, agent_name: str):
        task = self.get_task(task_id)
        agent_name = agent_name or (task.get("assigned_agent") or self.registry.resolve_for_task(task.get("description", "")))
        self.update_task_status(task_id, "running")
        agent = self._get_agent_instance(agent_name)
        if not agent:
            self.record_failure(task_id, f"Unknown agent: {agent_name}")
            return {"status": "failed", "error": f"Unknown agent: {agent_name}"}

        try:
            payload = {
                "task_id": task_id,
                "title": task.get("description") or "unnamed task",
                "description": task.get("description") or "unnamed task",
            }
            response = agent.execute(payload)
            status = str(response.get("status", "completed")).lower()
            result_payload = response.get("result")
            error_message = response.get("error")

            if status == "waiting_approval":
                result_json = json.dumps(result_payload) if result_payload is not None else None
                self.update_task_status(task_id, "waiting_approval", result=result_json, error=error_message, approval_required=1)
                self.logger.log("agent_waiting_approval", f"task={task_id} agent={agent_name}")
                return {"status": "waiting_approval", "task_id": task_id, "agent": agent_name, "result": result_payload}

            if status == "failed":
                self.record_failure(task_id, error_message or "Agent execution failed.")
                return {"status": "failed", "task_id": task_id, "agent": agent_name, "error": error_message or "Agent execution failed."}

            result_json = json.dumps(result_payload) if result_payload is not None else None
            self.update_task_status(task_id, "completed", result=result_json, error=None)
            self.logger.log("agent_completed", f"task={task_id} agent={agent_name}")
            return {"status": "completed", "task_id": task_id, "agent": agent_name, "result": result_payload}
        except Exception as exc:  # pragma: no cover - defensive path
            self.record_failure(task_id, str(exc))
            return {"status": "failed", "task_id": task_id, "agent": agent_name, "error": str(exc)}

    def delegate_task(self, description: str):
        agent_name = self.registry.resolve_for_task(description)
        task_id = self.create_task(description, assigned_agent=agent_name)
        self.log_event("agent_selected", f"task={task_id} agent={agent_name}")
        result = self.execute_agent_task(task_id, agent_name)
        return {"task_id": task_id, "agent": agent_name, "result": result}

    def read_logs(self):
        return self.logger.read()

    def shutdown(self):
        self.logger.log("system_shutdown", "Been Ventures workforce shutting down")

