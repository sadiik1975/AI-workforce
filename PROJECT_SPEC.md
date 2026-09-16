# BEEN VENTURES AI WORKFORCE
# EXISTING SYSTEM PROTECTION + UPGRADE INSTRUCTIONS

IMPORTANT:

This is an EXISTING, FUNCTIONING Been Ventures AI Workforce.

DO NOT rebuild it from scratch.

DO NOT replace it with a new application.

DO NOT delete, overwrite, disable, or remove existing working functionality.

DO NOT reset existing data.

DO NOT create duplicate agents, dashboards, databases, task systems, approval systems, or CLI commands when those already exist.

The existing Been Ventures AI Workforce is the source of truth.

==================================================
STEP 1 — INSPECT BEFORE CHANGING ANYTHING
==================================================

Before making any changes, inspect the complete existing project.

Identify and understand:

- Existing application structure
- Existing agents
- Business Manager
- Agent registry
- Dashboard
- CLI
- Tasks
- Approvals
- Projects
- Existing file handling
- Existing database/storage
- Existing configuration
- Existing API integrations
- Existing environment variables
- Existing tests
- Existing startup commands

Do not make changes until the existing architecture is understood.

==================================================
STEP 2 — PRESERVE EXISTING FUNCTIONALITY
==================================================

Everything that already works must continue working.

Specifically preserve:

- Business Manager
- Existing agents
- Existing agent registry
- Existing dashboard
- Existing CLI
- Existing tasks
- Existing approvals
- Existing projects
- Existing research functionality
- Existing integrations
- Existing data
- Existing startup process

Do not replace functioning components merely because another implementation is possible.

==================================================
STEP 3 — EXTEND, DON'T REBUILD
==================================================

The new specification that follows this instruction is an UPGRADE specification.

It must be applied to the existing Been Ventures workforce.

Use this model:

EXISTING FUNCTIONAL SYSTEM
+
NEW REQUIRED FEATURES
=
UPGRADED FUNCTIONAL SYSTEM

NOT:

EXISTING SYSTEM
→ DELETE
→ REBUILD
→ REPLACE

When an existing component already performs a required function, extend it rather than creating another competing implementation.

==================================================
STEP 4 — CRM
==================================================

Add a real CRM capability to the existing Been Ventures workforce.

DO NOT create a second disconnected CRM application.

Integrate CRM functionality into the existing dashboard and project/task architecture.

The CRM should manage:

- Leads
- Prospects
- Contacts
- Companies
- Opportunities
- Clients
- Conversations
- Follow-ups
- Sales stages
- Notes
- Tasks
- Activity history

Example pipeline:

NEW LEAD
↓
RESEARCHED
↓
CONTACTED
↓
RESPONDED
↓
QUALIFIED
↓
PROPOSAL
↓
NEGOTIATION
↓
WON
↓
LOST

Allow the existing Business Manager and sales/client-finder agents to interact with the CRM.

The CRM must use real persistent data.

Do not create fake contacts or fake companies.

==================================================
STEP 5 — FILE ORGANIZATION
==================================================

Add or improve a centralized file-organization system.

Every important output created by an agent should be associated with:

- Project
- Client, if applicable
- Task
- Agent
- File type
- Date
- Version
- Description

When an agent completes work, the resulting file should automatically be placed into the appropriate project/file organization.

Example:

Projects/
	Client-Website/
		research/
		proposals/
		contracts/
		content/
		assets/
		deliverables/

Another example:

Projects/
	Grant-Application/
		research/
		application/
		documents/
		submissions/

The system should know where an output belongs based on the project and task.

Do not scatter generated files throughout the application.

==================================================
STEP 6 — FILE INDEX
==================================================

Create a searchable file index.

The user should be able to ask:

"Show me the files for this client."

"Where is the proposal?"

"Show me everything created for this project."

"Find the latest version."

"Show me the research."

The system should locate the actual file.

Track:

filename
path
project
client
task
agent
file type
version
created date
modified date

Do not delete files automatically.

==================================================
STEP 7 — CRM + FILES + AGENTS
==================================================

Connect the CRM, project system, task system, and file system.

Example:

User asks:

"Research this HVAC company and prepare a website proposal."

Workflow:

Business Manager
↓
Client Finder
↓
Research
↓
CRM creates/updates company
↓
Task created
↓
Proposal created
↓
Proposal saved to correct project
↓
File indexed
↓
CRM activity updated
↓
Approval requested if needed

The user should be able to see the entire history.

==================================================
STEP 8 — APPROVAL PROTECTION
==================================================

Do not automatically:

- Send emails
- Contact prospects
- Submit proposals
- Sign agreements
- Spend money
- Make external commitments

without user approval.

==================================================
STEP 9 — NO FAKE FUNCTIONALITY
==================================================

Do not use:

- Fake CRM records
- Fake leads
- Fake companies
- Fake research
- Fake APIs
- Fake files
- Placeholder success messages

If something cannot be implemented because an external service is unavailable, clearly identify the missing integration.

==================================================
STEP 10 — TESTING
==================================================

After implementing the upgrade:

1. Start the existing application.
2. Verify the existing dashboard.
3. Verify the existing agents.
4. Verify the existing CLI.
5. Verify existing tasks.
6. Verify existing approvals.
7. Verify CRM.
8. Verify project creation.
9. Verify file creation.
10. Verify automatic file organization.
11. Verify file search.
12. Verify CRM-to-project connections.
13. Verify agent-to-file connections.
14. Verify persistence.
15. Run existing tests.
16. Run new tests.

Do not claim completion until the actual application has been run and tested.

==================================================
FINAL RULE
==================================================

The existing Been Ventures AI Workforce is valuable working software.

PROTECT IT.

EXTEND IT.

DO NOT REBUILD IT.

DO NOT DELETE WORKING FEATURES.

DO NOT DUPLICATE WORKING COMPONENTS.

The next specification is an ADDITIVE specification.

Implement its requirements by integrating them into the existing architecture.

If any requirement would require breaking an existing working feature, stop and report the conflict instead of making the destructive change.

# SPEC KIT — BEEN VENTURES MASTER AI WORKFORCE
# ADDITIVE UPGRADE SPECIFICATION

## PROJECT

Been Ventures AI Workforce

## PURPOSE

Expand the existing Been Ventures AI Workforce into a fully functioning business operating system.

The existing workforce must remain intact.

The system should provide:

- Business management
- Funding research
- Lead generation
- CRM
- Sales
- Marketing
- Client research
- Business research
- Projects
- Tasks
- Approvals
- File organization
- Document generation
- Activity tracking
- Dashboard
- Natural-language interaction

==================================================
1. BUSINESS MANAGER
==================================================

Maintain the existing:

business_manager

It remains the central coordinator.

The user should be able to ask:

"Find me grants."

"Find potential HVAC clients."

"Research this company."

"Add this company to my CRM."

"Create a proposal."

"Follow up with this lead."

"Create a marketing campaign."

"Show me today's tasks."

"Show me everything for this client."

"Organize these files."

The Business Manager routes requests to the appropriate agents.

==================================================
2. EXISTING AGENTS
==================================================

Preserve and improve the existing agents.

Existing capabilities should continue functioning.

Core agents include:

- business_manager
- funding
- client_finder
- sales
- marketing
- research
- operations

Do not create duplicate versions of existing agents.

==================================================
3. FUNDING AGENT
==================================================

Research real:

- Grants
- Government programs
- Corporate grants
- Entrepreneur programs
- Minority-business opportunities
- NY opportunities
- Local opportunities
- Industry-specific opportunities

Store:

Organization
Program
Eligibility
Deadline
Funding amount
Requirements
Official website
Source
Research date
Status

Never fabricate funding opportunities.

==================================================
4. CLIENT FINDER
==================================================

Research potential clients.

Prioritize industries and geographic areas configured by the user.

For each prospect, collect publicly available information such as:

Company
Industry
Location
Website
Services
Public contact information
Potential business need
Source
Research date

Allow prospects to be added to the CRM.

==================================================
5. CRM
==================================================

Create a fully functioning CRM integrated with the existing workforce.

CRM sections:

- Leads
- Prospects
- Contacts
- Companies
- Clients
- Opportunities
- Follow-ups
- Activities
- Notes
- Sales pipeline

Pipeline:

NEW LEAD
↓
RESEARCHED
↓
CONTACTED
↓
RESPONDED
↓
QUALIFIED
↓
PROPOSAL
↓
NEGOTIATION
↓
WON
↓
LOST

Each CRM record should support:

Company
Contact
Website
Industry
Location
Status
Sales stage
Notes
Tasks
Follow-ups
Activity history
Related files
Related project
Source
Created date
Updated date

==================================================
6. SALES AGENT
==================================================

Help with:

- Prospecting
- Lead qualification
- Outreach drafts
- Follow-ups
- Proposals
- Sales planning
- Pipeline management

The Sales Agent can prepare communications but must not send external communications without approval.

==================================================
7. MARKETING AGENT
==================================================

Create:

- Marketing campaigns
- Website copy
- Social media drafts
- Email drafts
- SEO ideas
- Promotional campaigns
- Content calendars
- Advertising concepts

Save completed materials into the correct project/file location.

==================================================
8. RESEARCH AGENT
==================================================

Perform real research.

Support configured search providers.

Research:

- Companies
- Industries
- Competitors
- Markets
- Clients
- Grants
- Business opportunities
- Technology
- Regulations when relevant

Every research result must include its source.

Save research results into the appropriate project.

==================================================
9. OPERATIONS AGENT
==================================================

Manage:

- Projects
- Tasks
- Deadlines
- Workflows
- Internal documents
- Business processes
- File organization
- Status tracking

==================================================
10. PROJECT SYSTEM
==================================================

Create persistent business projects.

Examples:

Projects/
	Client-Website/
	HVAC-Prospects/
	Grant-Application/
	BoroughBuild/
	Marketing/
	Research/
	Sales/

Every project should have:

README.md
project information
tasks
files
research
activity
related CRM records

==================================================
11. FILE ORGANIZATION
==================================================

Every generated business document should automatically be associated with the correct project.

Example:

Projects/
	Client-Website/
		research/
		proposals/
		contracts/
		content/
		assets/
		deliverables/

Grant:

Projects/
	Grant-Application/
		research/
		application/
		documents/
		submissions/

Files must not be randomly scattered throughout the application.

==================================================
12. FILE INDEX
==================================================

Maintain a searchable index of files.

Track:

Filename
Path
Project
Client
CRM record
Task
Agent
File type
Version
Created date
Modified date

The user should be able to ask:

"Find the proposal."

"Show me all files for this client."

"Show me the latest version."

"Show me everything created for this project."

==================================================
13. DOCUMENT GENERATION
==================================================

Allow agents to create real files.

Supported formats may include:

.md
.txt
.pdf
.docx
.csv
.json

Use appropriate libraries and existing project infrastructure.

Never create fake file references.

==================================================
14. TASK MANAGEMENT
==================================================

Tasks must contain:

ID
Project
Agent
Description
Status
Priority
Created date
Updated date
Related CRM record
Related files
Approval requirement
Result

Statuses:

pending
running
completed
failed
waiting_for_approval
cancelled

==================================================
15. APPROVAL SYSTEM
==================================================

Maintain a working approval queue.

Approval is required for actions such as:

- Sending emails
- Contacting prospects
- Sending proposals
- Submitting applications
- Spending money
- Signing agreements
- External commitments

The user remains the final decision maker.

==================================================
16. ACTIVITY HISTORY
==================================================

Track:

Agent actions
Research
CRM changes
Tasks
Projects
Files
Approvals
External actions
Errors

Example:

10:31 AM
Business Manager assigned research task.

10:32 AM
Client Finder found 8 potential companies.

10:34 AM
Research saved to project.

10:35 AM
CRM record created.

10:36 AM
Proposal generated.

==================================================
17. DASHBOARD
==================================================

Create/maintain a working dashboard.

Sections:

Home
Business Manager
CRM
Leads
Clients
Companies
Sales
Funding
Marketing
Research
Projects
Tasks
Approvals
Files
Activity
Settings

Display real data from the existing system.

==================================================
18. DASHBOARD OVERVIEW
==================================================

Home dashboard should show:

Active projects
Open tasks
Pending approvals
New leads
CRM pipeline
Recent research
Recent files
Recent activity
Funding opportunities

Keep the dashboard simple and readable.

==================================================
19. NATURAL LANGUAGE INTERFACE
==================================================

The user should be able to interact naturally.

Examples:

"Find me ten HVAC companies."

"Put those companies into my CRM."

"Research the first five."

"Create a proposal for this prospect."

"Save it to the project."

"Show me everything we've done for this client."

"What's waiting for my approval?"

The Business Manager coordinates the workflow.

==================================================
20. CLI
==================================================

Maintain the existing CLI.

Examples:

python3 run.py status

python3 run.py agents

python3 run.py tasks

python3 run.py approvals

python3 run.py projects

python3 run.py research

python3 run.py files

Add CRM commands if compatible with the existing architecture.

Example:

python3 run.py crm

Do not remove existing commands.

==================================================
21. CONFIGURATION
==================================================

Use environment variables.

Potential variables:

SEARCH_API_KEY
TAVILY_API_KEY
LLM_API_KEY
EMAIL_API_KEY
OTHER_REQUIRED_KEYS

Never hard-code secrets.

Create/maintain:

.env.example

Never commit .env.

==================================================
22. EXTERNAL INTEGRATIONS
==================================================

Design the architecture to support future integrations.

Potential integrations:

- Tavily
- Email
- Telegram
- Discord
- Google services
- Cloud storage
- GitHub
- AWS
- Other business services

Do not create fake integrations.

If an integration is unavailable, clearly identify what is required.

==================================================
23. SECURITY
==================================================

Protect:

API keys
Business information
CRM information
Client information
Credentials

Do not expose secrets in logs.

Do not execute arbitrary commands through the public dashboard.

==================================================
24. PERSISTENCE
==================================================

Persist:

Agents
Projects
Tasks
Approvals
CRM records
Companies
Contacts
Leads
Research
Files
Activity

Existing data must remain intact.

==================================================
25. TESTING
==================================================

Test the existing application before making changes.

Then test the upgraded system.

Required end-to-end test:

USER
↓
BUSINESS MANAGER
↓
CLIENT FINDER
↓
RESEARCH
↓
CRM RECORD
↓
PROJECT
↓
TASK
↓
DOCUMENT
↓
FILE ORGANIZATION
↓
ACTIVITY LOG
↓
APPROVAL

Also test:

Dashboard
Agent registry
CLI
CRM
Projects
Tasks
Research
Funding
Sales
Marketing
Files
Approvals
Persistence

==================================================
26. FAILURE HANDLING
==================================================

If something fails:

Do not fabricate success.

Record:

Agent
Task
Error
Time
Project
Recovery information

Display the actual status.

==================================================
27. DOCUMENTATION
==================================================

Maintain:

README.md
PROJECT_SPEC.md
ARCHITECTURE.md
AGENTS.md
SETUP.md
.env.example

Documentation must reflect the actual implementation.

==================================================
28. FINAL ACCEPTANCE CRITERIA
==================================================

The upgraded Been Ventures AI Workforce must have:

Working dashboard
Working Business Manager
Working existing agents
Working CRM
Working lead management
Working sales pipeline
Working funding research
Working client research
Working projects
Working tasks
Working approvals
Working file organization
Working file search
Working document generation
Working activity history
Working persistence
Working CLI

The existing Been Ventures system must remain functional.

Do not claim completion until the application has actually been run and tested.

Report:

Application status
Agents
CRM status
Projects
Tasks
Approvals
Files
Research
Tests passed
Tests failed
Required configuration
Known limitations

==================================================
FINAL PRINCIPLE
==================================================

This is an UPGRADE to an existing working Been Ventures AI Workforce.

Do not rebuild it.

Do not replace it.

Do not delete working features.

Do not duplicate existing functionality.

Extend the existing system while preserving everything that already works.

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
