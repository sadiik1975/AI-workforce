import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agents.funding import FundingAgent
from agents.client_finder import ClientFinderAgent
from agents.research import ResearchAgent
from core.tavily_search import SearchProviderError, search_grants
from workforce.app import WorkforceApp


class FakeTavilyClient:
    def __init__(self, response=None):
        self.response = {"results": []} if response is None else response
        self.calls = []

    def search(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class FundingTests(unittest.TestCase):
    def test_dotenv_key_is_loaded_into_config(self):
        with tempfile.TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text("SEARCH_API_KEY=dotenv-key\n", encoding="utf-8")
            with patch("core.config.ENV_PATH", env_path), patch.dict(os.environ, {}, clear=True):
                from core.config import get_config

                self.assertEqual(get_config()["search_api_key"], "dotenv-key")

    def test_search_grants_normalizes_results(self):
        client = FakeTavilyClient(
            {"results": [{"title": "Grant", "url": "https://grants.gov/x", "content": "Details"}]}
        )
        with patch("core.tavily_search._get_client", return_value=client):
            results = search_grants("Find grants for Been Ventures", "test-key")

        self.assertEqual(results[0]["title"], "Grant")
        self.assertEqual(results[0]["url"], "https://grants.gov/x")
        self.assertEqual(len(client.calls), 1)

    def test_search_grants_rejects_invalid_response(self):
        with patch("core.tavily_search._get_client", return_value=FakeTavilyClient({})):
            with self.assertRaises(SearchProviderError):
                search_grants("Find grants", "test-key")

    def test_search_grants_rejects_placeholder_key(self):
        with self.assertRaisesRegex(SearchProviderError, "placeholder"):
            search_grants("Find grants", "your_key_here")

    def test_funding_agent_returns_live_results(self):
        client = FakeTavilyClient(
            {"results": [{"title": "Grant", "url": "https://grants.gov/x", "content": "Details"}]}
        )
        with patch.dict(os.environ, {"SEARCH_API_KEY": "test-key"}), patch(
            "core.tavily_search._get_client", return_value=client
        ):
            response = FundingAgent().execute({"description": "Find grants for Been Ventures"})

        self.assertEqual(response["status"], "completed")
        self.assertEqual(response["result"]["count"], 1)

    def test_funding_task_records_provider_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            app = WorkforceApp(data_dir=Path(directory) / "data", logs_dir=Path(directory) / "logs")
            with patch.dict(os.environ, {"SEARCH_API_KEY": "test-key"}), patch(
                "core.tavily_search._get_client", side_effect=SearchProviderError("provider down")
            ):
                task_id = app.create_task("Find grants for Been Ventures", assigned_agent="funding")
                response = app.execute_agent_task(task_id, "funding")

            self.assertEqual(response["status"], "failed")
            self.assertEqual(app.get_task(task_id)["status"], "failed")
            self.assertIn("provider down", app.get_task(task_id)["error"])

    def test_market_research_alias_executes(self):
        client = FakeTavilyClient(
            {"results": [{"title": "Market source", "url": "https://example.com/market", "content": "Findings"}]}
        )
        with patch.dict(os.environ, {"SEARCH_API_KEY": "test-key"}), patch(
            "core.tavily_search._get_client", return_value=client
        ):
            response = ResearchAgent().execute({"description": "Research my market"})

        self.assertEqual(response["status"], "completed")
        self.assertEqual(response["result"]["count"], 1)

    def test_client_finder_returns_live_results(self):
        client = FakeTavilyClient(
            {"results": [{"title": "HVAC company", "url": "https://example.com/hvac", "content": "Atlanta"}]}
        )
        with patch.dict(os.environ, {"SEARCH_API_KEY": "test-key"}), patch(
            "core.tavily_search._get_client", return_value=client
        ):
            response = ClientFinderAgent().execute({"description": "Find HVAC prospects in Atlanta"})

        self.assertEqual(response["status"], "completed")
        self.assertEqual(response["result"]["count"], 1)


if __name__ == "__main__":
    unittest.main()