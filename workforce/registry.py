from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AgentDefinition:
    name: str
    description: str
    capabilities: List[str]
    enabled: bool = True
    available: bool = True


class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, AgentDefinition] = {}
        self._register_default_agents()

    def _register_default_agents(self):
        defaults = [
            ("business_manager", "Central coordinator for the workforce", ["orchestration", "task_management", "delegation", "prioritization"]),
            ("funding", "Researches grants and funding opportunities relevant to Been Ventures", ["grants", "funding_research", "eligibility_analysis"]),
            ("client_finder", "Researches prospects and lead opportunities in target markets", ["prospect_research", "lead_generation", "website_analysis"]),
            ("sales", "Supports outreach, qualification, and email/message drafting", ["outreach", "sales_support", "objection_handling"]),
            ("marketing", "Creates marketing plans and campaign content", ["marketing", "content_strategy", "seo_ideas"]),
            ("research", "Compatibility research agent for legacy task routing", ["research", "analysis", "market_study"]),
            ("operations", "Compatibility operations agent for workflow tracking", ["operations", "workflow", "task_tracking"]),
        ]
        for name, description, capabilities in defaults:
            self.register(name, description, capabilities)

    def register(self, name: str, description: str, capabilities: List[str], enabled: bool = True, available: bool = True):
        self._agents[name] = AgentDefinition(name=name, description=description, capabilities=capabilities, enabled=enabled, available=available)

    def get_agent(self, name: str) -> Optional[AgentDefinition]:
        return self._agents.get(name)

    def list_agents(self):
        return [
            {
                "name": agent.name,
                "description": agent.description,
                "capabilities": agent.capabilities,
                "enabled": agent.enabled,
                "available": agent.available,
            }
            for agent in self._agents.values()
        ]

    def resolve_for_task(self, task_text: str):
        text = (task_text or "").lower()

        if any(k in text for k in ["what should", "what should i do next", "work on today", "next steps", "help me"]):
            return "business_manager"
        if any(k in text for k in ["grant", "funding", "loan", "budget", "donor", "scholarship"]):
            return "funding"
        if any(k in text for k in ["sales", "outreach", "email", "sms", "message", "pitch", "follow up", "follow-up"]):
            return "sales"
        if any(k in text for k in ["hvac", "plumber", "electrician", "contractor", "prospect", "lead", "customer", "company"]):
            return "client_finder"
        if any(k in text for k in ["marketing", "campaign", "social", "content", "brand", "seo", "google business profile"]):
            return "marketing"
        if any(k in text for k in ["research", "market", "analysis", "study", "industry"]):
            return "research"
        if any(k in text for k in ["operations", "workflow", "task", "schedule"]):
            return "operations"
        return "business_manager"
