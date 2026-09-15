# Been Ventures AI Workforce

This project is a working local workforce for Been Ventures Inc. It coordinates business tasks, delegates to specialist agents, maintains a task lifecycle, enforces approval gates for risky actions, and logs operational events.

## What the workforce does

- routes user requests to the right specialist agent
- creates and tracks tasks in SQLite
- reports status and errors clearly
- requires approval before external, risky actions
- records operational logs for review and debugging
- supports a terminal-based user workflow without pretending external integrations are configured

## Agents

The workforce includes these registered agents:

- `business_manager` — coordinates tasks and decides which specialist should handle the work
- `funding` — researches grants and funding options
- `client_finder` — researches prospects and lead opportunities
- `sales` — drafts outreach and sales support content
- `marketing` — prepares campaigns and marketing plans

Legacy compatibility aliases are also supported for older task routing patterns:

- `research`
- `operations`

## Project layout

- `run.py` — CLI entry point
- `workforce/` — core workforce behavior and registry
- `agents/` — agent implementations
- `core/` — utility/configuration helpers
- `data/` — SQLite task storage
- `logs/` — operational logs
- `tests/` — automated tests
- `.env.example` — environment variable template

## Installation

```bash
cd /home/deek/projects/ai-workforce/been-ventures-workforce
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

## Environment variables

Create a local `.env` file from `.env.example` when you want to enable external integrations.

```bash
cp .env.example .env
```

Required variables:

- `SEARCH_API_KEY` — Tavily API key used by funding and prospect research tasks
- `EMAIL_API_KEY` — reserved for outbound email integrations
- `DATABASE_URL` — defaults to a local SQLite database
- `DEBUG` — optional debug flag

If these values are missing, the system keeps running and reports the exact missing configuration instead of pretending the task succeeded.

Install the search integration before running live funding research:

```bash
python3 -m pip install -r requirements.txt
```

## CLI usage

```bash
python3 run.py --help
python3 run.py status
python3 run.py agents
python3 run.py tasks
python3 run.py task "Find grant opportunities for Been Ventures"
python3 run.py approvals
python3 run.py approve TASK_ID
python3 run.py reject TASK_ID
python3 run.py logs
python3 run.py chat
python3 run.py stop
```

## Interactive mode

```bash
python3 run.py chat
```

Example session:

```text
Been Ventures AI Workforce
==========================
How can I help?

> Find grants for Been Ventures
```

The Business Manager routes the request to the correct agent and returns a structured result.

## Browser interface

Start the local funding dashboard with:

```bash
.venv/bin/python web.py
```

Then open `http://127.0.0.1:8000` in a browser. The Tavily key remains server-side in `.env`; it is never sent to the page.

## Task model

Tasks are stored in SQLite and include:

- `task_id`
- `description`
- `status`
- `assigned_agent`
- `priority`
- `result`
- `error`
- `approval_required`

Supported task states include:

- `pending`
- `running`
- `waiting_approval`
- `completed`
- `failed`
- `cancelled`

## Approval workflow

The approval system is enforced for externally consequential actions such as:

- emails or outbound messaging
- grant submissions
- publishing content
- spending money
- irreversible changes

Pending approvals are listed with:

```bash
python3 run.py approvals
```

And approved or rejected with:

```bash
python3 run.py approve TASK_ID
python3 run.py reject TASK_ID
```

## Logging

Operational events are written to:

- `logs/workforce.log`

The logger records task creation, status changes, approvals, and failures without writing secrets or credentials.

## Testing

```bash
cd /home/deek/projects/ai-workforce/been-ventures-workforce
source .venv/bin/activate
python3 -m unittest discover -s tests -v
```

## Troubleshooting

- If a research task fails with `SEARCH_API_KEY is not configured`, set the variable in `.env` and rerun the task.
- If a task is `failed`, inspect `logs/workforce.log` and the task output for the specific error.
- If an approval is required, run `python3 run.py approvals` and then approve or reject the task.

## Notes

This local implementation keeps functionality simple and reliable. It does not pretend that external research or sending services have succeeded unless their configuration is present and the operation actually completes.
