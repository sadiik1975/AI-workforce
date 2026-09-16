from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from workforce.app import WorkforceApp
from telegram_bot import run_bot

ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT / "web"


def app_instance() -> WorkforceApp:
    return WorkforceApp()


def task_payload(task: dict) -> dict:
    payload = dict(task)
    if payload.get("result"):
        try:
            payload["result"] = json.loads(payload["result"])
        except (TypeError, json.JSONDecodeError):
            pass
    return payload


def dashboard_payload() -> dict:
    app = app_instance()
    tasks = [task_payload(task) for task in app.list_tasks()]
    return {
        "agents": app.registry.list_agents(),
        "tasks": tasks,
        "crm": app.list_crm_records(),
        "approvals": [task for task in tasks if task["status"] in {"waiting_approval", "awaiting_approval"}],
        "activity": app.read_logs().splitlines()[-30:],
    }


class WorkforceHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json({"status": "ok"})
            return
        if path == "/api/bootstrap":
            self._send_json(dashboard_payload())
            return
        if path == "/api/crm":
            self._send_json({"records": app_instance().list_crm_records()})
            return
        if path.startswith("/api/tasks/"):
            task_id = path.removeprefix("/api/tasks/")
            try:
                self._send_json({"task": task_payload(app_instance().get_task(task_id))})
            except KeyError as exc:
                self._send_json({"status": "failed", "error": str(exc)}, 404)
            return
        if path != "/":
            self.send_error(404)
            return
        body = (WEB_ROOT / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/search":
            self._handle_task()
            return
        if path == "/api/crm":
            self._handle_crm_record()
            return
        if path.startswith("/api/tasks/") and path.endswith("/approve"):
            self._handle_approval(path, approve=True)
            return
        if path.startswith("/api/tasks/") and path.endswith("/reject"):
            self._handle_approval(path, approve=False)
            return
        self.send_error(404)

    def _read_payload(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def _handle_task(self) -> None:
        try:
            payload = self._read_payload()
            query = str(payload.get("query", "")).strip()
            if not query:
                self._send_json({"status": "failed", "error": "Enter a task to get started."}, 400)
                return

            app = app_instance()
            agent = app.registry.resolve_for_task(query)
            task_id = app.create_task(query, assigned_agent=agent)
            threading.Thread(
                target=app.execute_agent_task,
                args=(task_id, agent),
                daemon=True,
            ).start()
            self._send_json({"status": "running", "task_id": task_id, "agent": agent})
        except (ValueError, json.JSONDecodeError) as exc:
            self._send_json({"status": "failed", "error": f"Invalid request: {exc}"}, 400)
        except Exception as exc:
            self._send_json({"status": "failed", "error": str(exc)}, 500)

    def _handle_crm_record(self) -> None:
        try:
            payload = self._read_payload()
            record = app_instance().add_crm_record(
                payload.get("company", ""),
                record_type=str(payload.get("record_type", "company")),
                contact_name=payload.get("contact_name"),
                website=payload.get("website"),
                industry=payload.get("industry"),
                location=payload.get("location"),
                notes=payload.get("notes"),
            )
            self._send_json({"status": "created", "record": record}, 201)
        except (ValueError, json.JSONDecodeError) as exc:
            self._send_json({"status": "failed", "error": str(exc)}, 400)
        except Exception as exc:
            self._send_json({"status": "failed", "error": str(exc)}, 500)

    def _handle_approval(self, path: str, approve: bool) -> None:
        task_id = path.removeprefix("/api/tasks/").removesuffix("/approve").removesuffix("/reject")
        try:
            app = app_instance()
            if approve:
                app.approve_task(task_id)
            else:
                app.reject_task(task_id)
            self._send_json({"status": "completed", "task": task_payload(app.get_task(task_id))})
        except Exception as exc:
            self._send_json({"status": "failed", "error": str(exc)}, 404)

    def log_message(self, format: str, *args) -> None:
        return


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8000"))
    threading.Thread(target=run_bot, name="telegram-bot", daemon=True).start()
    server = ThreadingHTTPServer((host, port), WorkforceHandler)
    print(f"Been Ventures workforce listening on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
