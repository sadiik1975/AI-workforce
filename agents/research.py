from __future__ import annotations

from typing import Any, Dict

from core.config import get_config
from core.tavily_search import SearchProviderError, search_web
from .agent_base import BaseAgent


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Researches markets, industries, competitors, and business opportunities."
    capabilities = ["market_research", "industry_analysis", "competitor_research", "source_summary"]

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        text = self.validate_input(task)
        config = get_config()
        try:
            sources = search_web(
                f"{text}. Provide current market research with credible sources and practical findings.",
                config.get("search_api_key", ""),
            )
        except SearchProviderError as exc:
            return self.return_result(
                status="failed",
                error=str(exc),
                result={"title": "Market research request", "description": text, "source": "Tavily"},
            )

        return self.return_result(
            result={
                "title": "Market research results",
                "description": text,
                "source": "Tavily",
                "opportunities": sources,
                "count": len(sources),
                "next_steps": ["Review each source and validate findings before making business decisions."],
            }
        )