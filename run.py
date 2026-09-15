#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workforce.app import WorkforceApp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Been Ventures AI Workforce")
    parser.add_argument("command", nargs="?", default="status", help="status, tasks, task, agents, logs, approvals, approve, reject, stop, chat")
    parser.add_argument("value", nargs="*", help="task text or task id")
    return parser


def format_task(task: dict) -> str:
    return (
        f"Task: {task['task_id']}\n"
        f"Status: {task['status']}\n"
        f"Agent: {task['assigned_agent'] or 'unassigned'}\n"
        f"Description: {task['description']}\n"
        f"Result: {task['result'] or 'n/a'}\n"
        f"Error: {task['error'] or 'n/a'}\n"
        f"Approval required: {task['approval_required']}"
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    app = WorkforceApp()
    command = args.command.lower()

    if command == "status":
        print(app.render_status())
        return 0

    if command == "tasks":
        tasks = app.list_tasks()
        if not tasks:
            print("No tasks found.")
            return 0
        for task in tasks:
            print(format_task(task))
            print("-" * 60)
        return 0

    if command == "task":
        text = " ".join(args.value)
        if not text:
            print("Usage: python run.py task \"Find HVAC companies in Atlanta\"")
            return 1
        routed = app.registry.resolve_for_task(text)
        task_id = app.create_task(text, assigned_agent=routed)
        result = app.execute_agent_task(task_id, routed)
        print(f"Task created: {task_id}")
        print(f"Assigned agent: {routed}")
        print(json.dumps(result, indent=2, default=str))
        return 0

    if command == "agents":
        for agent in app.registry.list_agents():
            print(f"{agent['name']}: {agent['description']} | capabilities={agent['capabilities']}")
        return 0

    if command == "logs":
        output = app.read_logs()
        print(output if output else "No log entries yet.")
        return 0

    if command == "approvals":
        items = app.list_pending_approvals()
        if not items:
            print("No pending approvals.")
            return 0
        for item in items:
            print(format_task(item))
            print("-" * 60)
        return 0

    if command == "approve":
        task_id = " ".join(args.value)
        if not task_id:
            print("Usage: python run.py approve TASK_ID")
            return 1
        app.approve_task(task_id)
        print(f"Approved task {task_id}")
        return 0

    if command == "reject":
        task_id = " ".join(args.value)
        if not task_id:
            print("Usage: python run.py reject TASK_ID")
            return 1
        app.reject_task(task_id)
        print(f"Rejected task {task_id}")
        return 0

    if command == "agent":
        if len(args.value) < 2:
            print("Usage: python run.py agent <agent_name> \"Task description\"")
            return 1
        name = args.value[0]
        text = " ".join(args.value[1:])
        task_id = app.create_task(text, assigned_agent=name)
        result = app.execute_agent_task(task_id, name)
        print(json.dumps(result, indent=2, default=str))
        return 0

    if command == "chat":
        print("Been Ventures AI Workforce")
        print("==========================")
        print("How can I help?")
        while True:
            try:
                user_input = input("\n> ")
            except EOFError:
                print("\nExiting chat.")
                break
            if not user_input.strip():
                continue
            if user_input.strip().lower() in {"exit", "quit", "stop"}:
                print("Exiting chat.")
                break
            routed = app.registry.resolve_for_task(user_input)
            task_id = app.create_task(user_input, assigned_agent=routed)
            result = app.execute_agent_task(task_id, routed)
            print(f"Business Manager → {routed.title()}")
            print(json.dumps(result, indent=2, default=str))
        return 0

    if command == "stop":
        app.shutdown()
        print("Workforce stopped cleanly.")
        return 0

    print(app.render_status())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
