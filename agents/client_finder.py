from __future__ import annotations

from typing import Any, Dict

from core.config import get_config
from core.tavily_search import SearchProviderError, search_web
from .agent_base import BaseAgent


class ClientFinderAgent(BaseAgent):
    name = "client_finder"
    description = "Finds and evaluates prospects such as HVAC, plumbing, electrical, and contractor businesses."
    capabilities = [
        "prospect_research",
        "lead_generation",
        "website_analysis",
        "business_research",
        "market_mapping",
    ]

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        text = self.validate_input(task)
        config = get_config()
        if not config.get("search_api_key"):
            return self.return_result(
                status="failed",
                error="Client research unavailable: SEARCH_API_KEY is not configured.",
                result={
                    "title": "Prospect research request",
                    "description": text,
                    "source": "No configured external search provider",
                    "relevance": "The system cannot verify live businesses without a search API key.",
                    "next_steps": [
                        "Set SEARCH_API_KEY to enable live business lookup.",
                        "Run the task again to fetch candidate prospects by geography and service category.",
                    ],
                },
            )

        try:
            prospects = search_web(
                f"{text}. Find current local businesses and prospects. Include company name, location, website, and useful source details.",
                config["search_api_key"],
            )
        except SearchProviderError as exc:
            return self.return_result(
                status="failed",
                error=str(exc),
                result={
                    "title": "Prospect research request",
                    "description": text,
                    "source": "Tavily",
                    "next_steps": ["Check Tavily configuration and rerun the prospect search."],
                },
            )

        return self.return_result(
            result={
                "title": "Prospect research results",
                "description": text,
                "source": "Tavily",
                "opportunities": prospects,
                "count": len(prospects),
                "next_steps": [
                    "Review each prospect and verify contact details before outreach.",
                    "Prepare outreach content only after reviewing the relevant source.",
                ],
            }
        )
