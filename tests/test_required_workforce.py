import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from workforce.app import WorkforceApp


class RequiredWorkforceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.app = WorkforceApp(data_dir=self.root / "data", logs_dir=self.root / "logs")

    def tearDown(self):
        self.tempdir.cleanup()

    def test_expected_agents_register(self):
        names = {agent["name"] for agent in self.app.registry.list_agents()}
        for expected in ["business_manager", "funding", "client_finder", "sales", "marketing"]:
            self.assertIn(expected, names)

    def test_business_manager_routes_to_specialists(self):
        routes = {
            "Find grants for Been Ventures": "funding",
            "Find HVAC companies in Atlanta": "client_finder",
            "Write an email to a prospect": "sales",
            "Create a marketing campaign": "marketing",
            "What should Been Ventures work on today?": "business_manager",
        }
        for text, expected in routes.items():
            self.assertEqual(self.app.registry.resolve_for_task(text), expected)

    def test_task_lifecycle_runs_and_records_errors(self):
        task_id = self.app.create_task("Research market opportunities", assigned_agent="business_manager")
        self.app.update_task_status(task_id, "running")
        self.app.update_task_status(task_id, "completed", result=json.dumps({"summary": "done"}))
        task = self.app.get_task(task_id)
        self.assertEqual(task["status"], "completed")
        self.assertIn("done", task["result"])

        fail_id = self.app.create_task("Bad task", assigned_agent="funding")
        self.app.record_failure(fail_id, "SEARCH_API_KEY is not configured.")
        failed = self.app.get_task(fail_id)
        self.assertEqual(failed["status"], "failed")
        self.assertIn("SEARCH_API_KEY", failed["error"])

    def test_approval_states_are_supported(self):
        task_id = self.app.create_task("Send outreach email", assigned_agent="sales")
        self.app.request_approval(task_id, "Requires owner approval before sending")
        pending = self.app.get_task(task_id)
        self.assertIn(pending["status"], {"waiting_approval", "awaiting_approval"})

        self.app.approve_task(task_id)
        approved = self.app.get_task(task_id)
        self.assertEqual(approved["status"], "completed")
        self.assertEqual(approved["approval_required"], 0)

    def test_cli_commands_work(self):
        root = Path(__file__).resolve().parents[1]
        commands = [
            [sys.executable, "run.py", "--help"],
            [sys.executable, "run.py", "status"],
            [sys.executable, "run.py", "agents"],
            [sys.executable, "run.py", "tasks"],
            [sys.executable, "run.py", "approvals"],
            [sys.executable, "run.py", "logs"],
        ]
        for command in commands:
            result = subprocess.run(command, cwd=str(root), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=f"Command failed: {' '.join(command)}\n{result.stderr}")


if __name__ == "__main__":
    unittest.main()
