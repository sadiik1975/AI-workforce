from __future__ import annotations

from typing import Any, Dict

from .agent_base import BaseAgent


class BusinessManagerAgent(BaseAgent):
    name = "business_manager"
    description = "Routes tasks, prioritizes work, and coordinates the workforce."
    capabilities = [
        "orchestration",
        "task_management",
        "delegation",
        "status_reporting",
        "prioritization",
    ]

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        text = self.validate_input(task)
        lowered = text.lower()

        if any(keyword in lowered for keyword in ["what should", "work on today", "what should i do next", "next steps", "help"]):
            return self.return_result(
                result={
                    "summary": "The Business Manager recommends focusing on immediate revenue, lead generation, and approval-sensitive work.",
                    "priorities": [
                        "Review active tasks and pending approvals.",
                        "Identify the highest-priority prospecting or funding opportunity.",
                        "Prepare outreach or marketing content only after approval where required.",
                    ],
                    "route": "business_manager",
                }
            )

        route = self.registry.resolve_for_task(text) if self.registry else "business_manager"
        summary = f"Business Manager selected {route} for this request."
        next_steps = [
            "Create or update the task record.",
            "Delegate to the selected specialist agent.",
            "Validate the result and present it back to the user.",
        ]
        if route == "funding":
            next_steps = [
                "Check for relevant grant or funding announcements.",
                "Review eligibility and application requirements.",
                "Summarize opportunities with source links and next steps.",
            ]
        elif route == "client_finder":
            next_steps = [
                "Identify target service businesses by market and service category.",
                "Review website quality and likely digital-service need.",
                "Rank prospects by fit and conversion potential.",
            ]
        elif route == "sales":
            next_steps = [
                "Qualify the prospect or lead.",
                "Draft outreach messaging aligned to the offer.",
                "Require approval before sending externally.",
            ]
        elif route == "marketing":
            next_steps = [
                "Define the campaign objective and target audience.",
                "Draft positioning, content, and offer language.",
                "Review options and approval points before publishing.",
            ]

        return self.return_result(
            result={
                "summary": summary,
                "route": route,
                "next_steps": next_steps,
            }
        )
