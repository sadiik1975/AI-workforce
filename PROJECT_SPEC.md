# Been Ventures AI Workforce Project Specification

## Purpose

The workforce is designed to support Been Ventures Inc. by coordinating business work, routing tasks to specialist agents, tracking task state, enforcing approval gates for risky actions, and producing useful logs and summaries for the owner.

## Operating principles

- preserve working functionality before redesigning anything
- do not fabricate external findings or fake completion states
- require explicit approval before risky external actions
- keep the implementation understandable and maintainable
- rely on local standard-library tools unless external integrations are explicitly configured
- fail clearly when required credentials are missing

## Architectural goals

1. The Business Manager decides which specialist should handle a request.
2. Each task is created, assigned, and tracked in a persistent SQLite store.
3. Agents validate input, perform the task, and return structured results or clear failures.
4. Approval is required before sending or publishing externally impactful content.
5. Logs record the important lifecycle changes for debugging and review.
6. The system remains usable as a local command-line workforce without unnecessary complexity.

## Required agent model

Expected registered agents:

- `business_manager`
- `funding`
- `client_finder`
- `sales`
- `marketing`

Compatibility aliases retained for historical compatibility:

- `research`
- `operations`

Each agent is expected to support the following behavior:

- receive a task
- validate its input
- execute the operation
- return structured results
- report errors cleanly
- participate in the task lifecycle
- be routed by the Business Manager when appropriate

## Task model

Each task includes:

- `task_id`
- `description`
- `status`
- `priority`
- `assigned_agent`
- `created_at`
- `updated_at`
- `result`
- `error`
- `approval_required`

Supported task statuses:

- `pending`
- `running`
- `waiting_approval`
- `completed`
- `failed`
- `cancelled`

A task is never marked complete unless the assigned operation actually succeeded.

## Routing rules

The Business Manager routes based on the user request:

- grant or funding request -> `funding`
- HVAC, prospect, or contractor search -> `client_finder`
- outreach, email, or phone sales content -> `sales`
- marketing, campaign, or content direction -> `marketing`
- general business guidance -> `business_manager`

## Approval triggers

Approval is required for actions that could have legal, financial, reputational, or operational risk, including:

- sending outreach emails or SMS
- publishing or submitting content externally
- spending money or making commitments
- submitting grant applications
- deleting or altering important data

## Configuration

The workforce uses environment variables for sensitive configuration.

Supported variables:

- `SEARCH_API_KEY`
- `EMAIL_API_KEY`
- `DATABASE_URL`
- `DEBUG`

The `.env.example` file documents the required settings without including secrets.

## CLI behavior

The current CLI provides the terminal interface:

```bash
python3 run.py status
python3 run.py agents
python3 run.py tasks
python3 run.py task "Find grants for Been Ventures"
python3 run.py approvals
python3 run.py approve TASK_ID
python3 run.py reject TASK_ID
python3 run.py logs
python3 run.py chat
```

## Logging

The system writes operational logs to `logs/workforce.log` and records task creation, status changes, approval states, and failures without logging credentials or secrets.

## Acceptance criteria

The project is considered functional when:

- the workforce starts without crashing
- the expected agents are registered
- tasks can be created and executed
- lifecycle updates record status correctly
- approvals are respected
- logs are written
- CLI commands succeed
- tests pass
- research tasks fail clearly when API credentials are missing instead of pretending success

## Current implementation status

The project is implemented as a reliable local workforce using Python and SQLite only. It is operational for local use and intentionally surfaces missing external-config errors clearly rather than fabricating results.
