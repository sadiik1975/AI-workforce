from __future__ import annotations

from typing import Any, Dict

from core.config import get_config
from core.tavily_search import SearchProviderError, search_grants
from .agent_base import BaseAgent


class FundingAgent(BaseAgent):
    name = "funding"
    description = "Researches funding and grant opportunities relevant to Been Ventures."
    capabilities = [
        "grant_research",
        "funding_opportunity_research",
        "eligibility_analysis",
        "deadline_tracking",
        "opportunity_summary",
    ]

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        text = self.validate_input(task)
        config = get_config()
        if not config.get("search_api_key"):
            return self.return_result(
                status="failed",
                error="Funding research unavailable: SEARCH_API_KEY is not configured.",
                result={
                    "title": "Funding research request",
                    "description": text,
                    "source": "No configured external search provider",
                    "relevance": "No real funding opportunities can be verified without a search API key.",
                    "next_steps": [
                        "Set SEARCH_API_KEY in the environment.",
                        "Rerun the funding task to query live grant opportunities.",
                    ],
                },
            )

        try:
            opportunities = search_grants(text, config["search_api_key"])
        except SearchProviderError as exc:
            return self.return_result(
                status="failed",
                error=str(exc),
                result={
                    "title": "Funding research request",
                    "description": text,
                    "source": "Tavily",
                    "next_steps": [
                        "Check Tavily configuration and network access.",
                        "Rerun the funding task after correcting the reported error.",
                    ],
                },
            )

        return self.return_result(
            result={
                "title": "Grant opportunities for Been Ventures",
                "description": text,
                "source": "Tavily",
                "opportunities": opportunities,
                "count": len(opportunities),
                "next_steps": [
                    "Verify eligibility, deadline, and award terms on each official source.",
                    "Confirm state and city requirements before preparing an application.",
                ],
            }
        )
