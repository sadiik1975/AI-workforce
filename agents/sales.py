from __future__ import annotations

from typing import Any, Dict

from .agent_base import BaseAgent


class SalesAgent(BaseAgent):
    name = "sales"
    description = "Supports outreach, qualification, and email drafting while requiring explicit approval for sending."
    capabilities = [
        "prospect_qualification",
        "outreach_strategy",
        "email_drafting",
        "follow_up_suggestions",
        "objection_handling",
    ]

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        text = self.validate_input(task)
        lower = text.lower()
        if any(keyword in lower for keyword in ["send", "email", "sms", "message", "campaign"]):
            return self.return_result(
                status="waiting_approval",
                result={
                    "title": "Sales action prepared",
                    "description": text,
                    "approval_required": True,
                    "next_steps": [
                        "Review the drafted sales message.",
                        "Approve before sending externally.",
                    ],
                },
            )

        return self.return_result(
            result={
                "title": "Sales support prepared",
                "description": text,
                "recommendation": "Qualify the target, position the offer clearly, and ask for a focused next step.",
                "next_steps": [
                    "Identify the buyer and pain point.",
                    "Write a short outreach message.",
                    "Request approval prior to any external sending action.",
                ],
            }
        )
