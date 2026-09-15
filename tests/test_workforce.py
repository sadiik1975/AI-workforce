import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from workforce.app import WorkforceApp


class WorkforceAppTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.app = WorkforceApp(data_dir=self.root / "data", logs_dir=self.root / "logs")

    def tearDown(self):
        self.tempdir.cleanup()

    def test_startup_registers_agents(self):
        agents = self.app.registry.list_agents()
        names = {agent["name"] for agent in agents}
        self.assertIn("business_manager", names)
        self.assertIn("research", names)
        self.assertIn("operations", names)

    def test_task_creation_and_assignment(self):
        task_id = self.app.create_task("Research HVAC opportunities in Atlanta", assigned_agent="research")
        task = self.app.get_task(task_id)
        self.assertEqual(task["description"], "Research HVAC opportunities in Atlanta")
        self.assertEqual(task["assigned_agent"], "research")
        self.assertEqual(task["status"], "pending")

    def test_task_status_update_and_completion(self):
        task_id = self.app.create_task("Draft marketing plan", assigned_agent="marketing")
        self.app.update_task_status(task_id, "running")
        self.app.update_task_status(task_id, "completed", result="Marketing plan prepared")
        task = self.app.get_task(task_id)
        self.assertEqual(task["status"], "completed")
        self.assertIn("Marketing plan prepared", task["result"])

    def test_failed_task_is_recorded(self):
        task_id = self.app.create_task("Research data", assigned_agent="research")
        self.app.record_failure(task_id, "External service unavailable")
        task = self.app.get_task(task_id)
        self.assertEqual(task["status"], "failed")
        self.assertIn("External service unavailable", task["error"])

    def test_approval_workflow(self):
        task_id = self.app.create_task("Send outbound sales outreach", assigned_agent="sales")
        self.app.request_approval(task_id, "Send SMS campaign")
        self.app.approve_task(task_id)
        task = self.app.get_task(task_id)
        self.assertEqual(task["status"], "completed")
        self.assertEqual(task["approval_required"], 0)

    def test_logging_contains_events(self):
        task_id = self.app.create_task("Create local SEO plan", assigned_agent="seo")
        self.app.log_event("task_started", f"task={task_id}")
        logfile = self.root / "logs" / "workforce.log"
        self.assertTrue(logfile.exists())
        with logfile.open("r", encoding="utf-8") as fh:
            content = fh.read()
        self.assertIn("task_started", content)

    def test_duplicate_task_handling(self):
        first = self.app.create_task("Find HVAC leads in Atlanta", assigned_agent="client_finder")
        second = self.app.create_task("Find HVAC leads in Atlanta", assigned_agent="client_finder")
        self.assertNotEqual(first, second)

    def test_shutdown(self):
        self.app.shutdown()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
