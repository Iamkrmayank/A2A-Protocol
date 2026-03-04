# OpenFang Agent OS — Product Walkthrough Report

**Prepared by:** Kumar Mayank
**Date:** March 4, 2026
**Version:** 0.2.7
**Environment:** Local (Windows 11, `http://127.0.0.1:50051`)
**Default Model:** OpenAI `gpt-4o-mini`

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Database & Persistence](#3-database--persistence)
4. [Memory System](#4-memory-system)
5. [Dashboard — Tab-by-Tab Walkthrough](#5-dashboard--tab-by-tab-walkthrough)
   - 5.1 [Overview](#51-overview)
   - 5.2 [Chat (Agents)](#52-chat-agents)
   - 5.3 [Analytics](#53-analytics)
   - 5.4 [Logs & Audit Trail](#54-logs--audit-trail)
   - 5.5 [Sessions & Memory](#55-sessions--memory)
   - 5.6 [Execution Approvals](#56-execution-approvals)
   - 5.7 [Agent Comms](#57-agent-comms)
   - 5.8 [Workflows](#58-workflows)
   - 5.9 [Scheduler](#59-scheduler)
   - 5.10 [Channels](#510-channels)
   - 5.11 [Skills](#511-skills)
   - 5.12 [Hands](#512-hands)
   - 5.13 [Settings → Providers](#513-settings--providers)
6. [Security Architecture](#6-security-architecture)
7. [Deployment Considerations](#7-deployment-considerations)
8. [Key Observations & Recommendations](#8-key-observations--recommendations)
9. [References](#9-references)

---

## 1. Project Overview

**OpenFang** is an open-source **Agent Operating System (Agent OS)** written in Rust. It provides a unified runtime for deploying, managing, and orchestrating AI agents across multiple LLM providers and messaging platforms.

| Property | Value |
|----------|-------|
| Language | Rust (14 crates, workspace) |
| Version | 0.2.7 |
| License | Open-source |
| Config file | `~/.openfang/config.toml` |
| Default API | `http://127.0.0.1:50051` |
| CLI binary | `target/release/openfang.exe` |
| Dashboard | Alpine.js SPA (`/static/index_body.html`) |

### Crate Structure
```
openfang/
├── crates/
│   ├── openfang-api         # REST API + WebSocket server
│   ├── openfang-cli         # CLI binary (start, chat, status)
│   ├── openfang-kernel      # Core agent runtime & orchestration
│   ├── openfang-runtime     # LLM execution, embedding driver
│   ├── openfang-memory      # Memory substrate (SQLite)
│   ├── openfang-channels    # 40+ messaging platform adapters
│   ├── openfang-skills      # Skill registry & loader
│   ├── openfang-hands       # Pre-configured autonomous agents
│   ├── openfang-types       # Shared types (AgentManifest, etc.)
│   ├── openfang-migrate     # Database migrations
│   └── ...
```

---

## 2. System Architecture

### High-Level Architecture
```
External Platforms (Telegram, Discord, Slack, WhatsApp, etc.)
              ↓
     Channel Adapters (openfang-channels)
              ↓
       BridgeManager + AgentRouter
              ↓
     OpenFang Kernel (openfang-kernel)
              ↓
     LLM Providers (OpenAI, Anthropic, Groq, etc.)
              ↓
     Memory Substrate (SQLite via openfang-memory)
```

### Key Architectural Patterns
- **`KernelHandle` trait** — avoids circular dependencies between runtime and kernel
- **`AppState`** in `server.rs` — bridges kernel to API routes
- **`ChannelBridgeHandle` trait** — kernel's interface to messaging channels
- **`AgentRouter`** — priority-based message routing to agents
- New routes must be registered in `server.rs` router AND implemented in `routes.rs`

---

## 3. Database & Persistence

OpenFang uses **SQLite** (via `rusqlite` crate) as its primary database.

**Database file location:** `~/.openfang/openfang.db`

### Tables

| Table | Data Stored |
|-------|------------|
| `agents` | Agent entries, manifests, state, identity |
| `memories` | Semantic + structured memory fragments |
| `sessions` | Conversation history per agent |
| `knowledge` | Long-term knowledge store entries |
| `audit_log` | Tamper-evident cryptographic audit chain |

### SQLite Limitations for Production
SQLite is a **file-based, single-process database** — this creates challenges for cloud deployment:

| Problem | Impact |
|---------|--------|
| Container restart | Database file lost (ephemeral disk) |
| Horizontal scaling | Each container has its own `.db` — no shared state |
| Multiple replicas | Cannot share a single SQLite file safely across containers |
| ECS/Kubernetes | Stateless containers + SQLite = data loss on redeploy |

**Recommendation:** For production cloud deployment (AWS ECS, Kubernetes), replace SQLite with **PostgreSQL** or **AWS RDS**. The `openfang-memory` crate would need a pluggable backend (SQLite for local dev, Postgres for prod).

---

## 4. Memory System

OpenFang implements a **4-layer memory architecture** inside `openfang-memory`:

| Store | File | Purpose | How agents use it |
|-------|------|---------|-------------------|
| **Structured** | `structured.rs` | Key-value pairs | `memory_store` / `memory_recall` |
| **Semantic** | `semantic.rs` | Natural language + vector embeddings | `remember` / `recall` (meaning-based search) |
| **Session** | `session.rs` | Full conversation history | Auto-saved per conversation |
| **Knowledge** | `knowledge.rs` | Long-term facts and documents | `knowledge_add` |

### Memory Consolidation
A background **Consolidation Engine** (`consolidation.rs`) runs every 24 hours. It automatically decays and merges low-confidence or stale memories based on `decay_rate` set in config:

```toml
[memory]
decay_rate = 0.05
```

### Embedding Driver
OpenFang uses OpenAI's embedding API to generate vector embeddings for semantic memory. Warning at boot:
> "Embedding driver configured to send data to external API — text content will leave this machine"

---

## 5. Dashboard — Tab-by-Tab Walkthrough

### 5.1 Overview

The landing page of the OpenFang dashboard provides a real-time system health snapshot.

**Getting Started Wizard (4/5 complete):**

| Step | Status |
|------|--------|
| Configure an LLM provider | ✓ Done |
| Create your first agent | ✓ Done |
| Send your first message | ✓ Done |
| Connect a messaging channel | ✓ Done |
| Browse or install a skill | ○ Pending |

**Live Stats at time of walkthrough:**

| Metric | Value |
|--------|-------|
| Agents Running | 2 |
| Tokens Used | 0 |
| Total Cost | $0.00 |
| Uptime | ~6 minutes |
| Channels | 6 configured |
| Skills | 1 installed |
| MCP Servers | 0 |
| Tool Calls | 0 |
| LLM Providers | 2 / 30 configured |

**System Health:**
- Status: `ok`
- Version: `0.2.7`
- Provider: `openai`
- Model: `gpt-4o-mini`

**Quick Actions available from Overview:**
New Agent, Browse Skills, Add Channel, Create Workflow, Settings

---

### 5.2 Chat (Agents)

The Chat tab is the primary interface for creating and interacting with agents.

#### Currently Running Agents
| Agent | Model | Status |
|-------|-------|--------|
| General Assistant | gpt-4o-mini | Running |
| API Designer | gpt-4o-mini | Running |
| my-assistant | gpt-4o-mini | Running (spawned during walkthrough) |

These agents persist across daemon restarts via SQLite.

#### Pre-defined Agent Templates (10)
| Template | Category | Purpose |
|----------|----------|---------|
| General Assistant | General | Everyday tasks, Q&A |
| Code Helper | Development | Code writing, review, debugging |
| Researcher | Research | Topic analysis, summaries |
| Writer | Writing | Drafting, editing, content |
| Data Analyst | Development | Datasets, queries, statistics |
| DevOps Engineer | Development | CI/CD, Docker, infrastructure |
| Customer Support | Business | Customer inquiry handling |
| Tutor | General | Step-by-step educational explanations |
| API Designer | Development | REST API, OpenAPI specifications |
| Meeting Notes | Business | Meeting transcripts → structured notes |

#### Custom Agent TOML Format
Agents can be defined as `.toml` files at `~/.openfang/agents/<name>/agent.toml`:

```toml
name = "my-assistant"
version = "0.1.0"
description = "My custom assistant agent"
author = "yourname"
module = "builtin:chat"

[model]
provider = "openai"
model = "gpt-4o-mini"
max_tokens = 4096
temperature = 0.7
system_prompt = """
You are a helpful assistant. Answer clearly and concisely.
"""

[resources]
max_cost_per_day_usd = 2.0
max_llm_tokens_per_hour = 100000

[capabilities]
tools = ["file_read", "web_search", "memory_store", "memory_recall"]
network = ["*"]
memory_read = ["*"]
memory_write = ["self.*"]
agent_spawn = false
```

**Key manifest fields:**
- `module` — `builtin:chat` for standard LLM agents
- `schedule` — `Reactive` | `Periodic` | `Proactive` | `Continuous`
- `profile` — shortcut presets: `Minimal`, `Coding`, `Research`, `Messaging`, `Automation`, `Full`
- `fallback_models` — chain of backup models if primary fails
- `resources` — token, cost, and CPU limits per agent
- `capabilities` — fine-grained tool and network permissions

**30 bundled agent templates** are compiled into the binary (analyst, architect, coder, debugger, devops-lead, researcher, writer, tutor, etc.)

---

### 5.3 Analytics

Real-time cost and usage tracking across all agents and models.

**Sub-tabs:**
| Sub-tab | Data |
|---------|------|
| Summary | Total tokens, cost, API calls, tool calls |
| By Model | Token usage broken down per model |
| By Agent | Per-agent token and tool call counts |
| Costs | Spend breakdown: today, projected monthly, avg cost/message |

**At time of walkthrough:** All metrics were $0.00 / 0 tokens — no LLM calls made yet in session.

**Cost tracking granularity:**
- Per agent
- Per model
- Per provider
- Daily trend (last 7 days graph)
- Projected monthly spend

---

### 5.4 Logs & Audit Trail

#### Live Logs
Real-time streaming log viewer with controls: Pause, Clear, Export, Auto-scroll.

**Sample entry observed:**
```
6:33:35 PM  INFO  [AgentSpawn]  name=my-assistant, parent=None
```

#### Audit Trail — Tamper-Evident Logging

Every agent action is recorded in a **cryptographic hash chain** (Merkle-style):

```
Entry 0 → Hash_0
Entry 1 → Hash(Hash_0 + Entry_1)
Entry 2 → Hash(Hash_1 + Entry_2)
...
```

If any entry is altered or deleted, the entire chain becomes invalid.

**Audit entry observed:**
| # | Timestamp | Agent | Action | Detail | Outcome |
|---|-----------|-------|--------|--------|---------|
| 0 | 3/4/2026 6:33:35 PM | my-assistant | Agent Created | name=my-assistant, parent=None | ok |

**Chain tip:** `13225f6bb1adb092...`
**Verify Chain status: VALID ✓**

**Use cases:**
- Compliance and regulatory audit
- Security incident investigation
- Debugging agent behavior timelines
- Exportable for external audit systems

---

### 5.5 Sessions & Memory

#### Sessions
Each conversation with an agent creates a persistent session stored in SQLite.

| Session ID | Agent | Messages | Created |
|------------|-------|----------|---------|
| 50eda898... | my-assistant | 4 | 3/4/2026 6:33 PM |
| 67585805... | my-assistant | 0 | 3/4/2026 6:33 PM |
| c03e9fde... | General Assistant | 2 | 3/4/2026 6:15 PM |
| eb42a986... | General Assistant | 0 | 3/2/2026 5:39 PM |

Sessions from **3/2/2026** (2 days prior) were still present — confirming SQLite persistence across daemon restarts.

Actions per session: **Chat** (resume) or **Delete**.

#### Memory (Key-Value Store)
Each agent has a persistent key-value memory store visible in the dashboard.

- `my-assistant`: 0 keys (empty at time of walkthrough)
- Keys can be added manually via `+ Add Key` or created automatically by agents using `memory_store` tool

**Session vs Memory distinction:**

| | Session | Memory |
|--|---------|--------|
| Stores | Full message history | Key-value pairs |
| Scope | Per conversation | Across all conversations |
| Example | Chat log | "User prefers Python" |
| Lifecycle | Until deleted | Until agent forgets or clears |

---

### 5.6 Execution Approvals

**Human-in-the-loop control** for sensitive agent actions.

When an agent requests permission to perform a sensitive operation, it appears here for human review before execution.

**Filter tabs:** All | Pending | Approved | Rejected

**Status at walkthrough:** No pending approvals.

**Actions that trigger approval requests:**
- `shell_exec` — running system commands
- `file_write` / `file_delete` — modifying files
- Sensitive external API calls
- Agent spawning (if policy requires approval)
- Network requests to restricted domains

**Why it matters:** Prevents autonomous agents from taking irreversible or damaging actions without explicit human consent. Critical safety layer for production deployments.

---

### 5.7 Agent Comms

Agent-to-Agent (A2A) communication interface.

#### Agent Topology
```
my-assistant ←→ General Assistant
      ↕
  API Designer
```
All 3 agents were Running and visible in the topology view.

#### Send Message
Direct agent-to-agent messaging:
- **From Agent** — sending agent
- **To Agent** — receiving agent
- **Message** — content to pass

#### Post Task
Structured task assignment between agents:
- Task description
- Expected output format
- Priority level

#### Live Event Feed
Real-time stream of inter-agent communication events (0 events at walkthrough time).

**Use case — Multi-agent orchestration:**
```
User → General Assistant
    → "Research X and send findings to Coder"
    → General Assistant sends task to Researcher
    → Researcher sends result to Coder
    → Coder produces output
```

---

### 5.8 Workflows

Multi-step agent pipelines where each step's output becomes the next step's input.

**Create Workflow fields:**
| Field | Description |
|-------|-------------|
| Name | Workflow identifier |
| Description | What the pipeline does |
| Steps | Each step: step name + agent + execution mode |

**Step template variable:** `{{input}}` — automatically passes previous step's output to next step.

**Execution modes per step:** Sequential (observed), likely Parallel available.

**Example workflow:**
```
Name: research-and-publish

Step #1 → Researcher Agent
  "Research this topic: {{input}}"

Step #2 → Writer Agent
  "Write a blog post based on: {{input}}"

Step #3 → API Designer Agent
  "Format and validate output: {{input}}"
```

**Event Triggers** (visible in Scheduler tab) allow workflows to fire in response to system events:
- Agent lifecycle events (crash, spawn, stop)
- Memory update events
- Custom application events

---

### 5.9 Scheduler

Cron-based and event-driven task automation for agents.

#### Scheduled Jobs (Cron)

| Field | Example | Description |
|-------|---------|-------------|
| Job Name | `daily-report` | Identifier |
| Cron Expression | `0 9 * * 1-5` | When to run |
| Target Agent | `my-assistant` | Who executes |
| Message | `Generate daily status report` | What to send |
| Enabled | Toggle | Active or paused |

**Quick Presets:**
| Preset | Cron |
|--------|------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every 15 minutes | `*/15 * * * *` |
| Every hour | `0 * * * *` |
| Daily at 9am | `0 9 * * *` |
| Weekdays at 9am | `0 9 * * 1-5` |
| Every Monday 9am | `0 9 * * 1` |
| First of month | `0 9 1 * *` |

**Key feature:** Scheduled jobs are stored in SQLite and **survive daemon restarts**.

#### Event Triggers
Fire agents in response to system events (configured via Workflows page, monitored here).

#### Run History
Aggregated log of all past scheduled job runs and trigger fires.

---

### 5.10 Channels

**40 messaging platform adapters** across 5 categories. All 40 available, 0 configured at walkthrough time.

| Category | Count | Platforms |
|----------|-------|-----------|
| Messaging | 12 | Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, LINE, Viber, Messenger, Threema, Keybase |
| Social | 5 | Reddit, Mastodon, Bluesky, LinkedIn, Nostr |
| Enterprise | 10 | Microsoft Teams, Mattermost, Google Chat, Webex, Feishu/Lark, DingTalk, Pumble, Flock, Twist, Zulip |
| Developer | 9 | IRC, XMPP, Gitter, Discourse, Revolt, Guilded, Nextcloud Talk, Rocket.Chat, Twitch |
| Notifications | 4 | ntfy, Gotify, Webhook, Mumble |

**Setup difficulty:**

| Difficulty | Time | Examples |
|------------|------|---------|
| Easy | 1–3 min | Telegram, WhatsApp, Bluesky, Webhook, Pumble |
| Medium | 5–10 min | Slack, Signal, Facebook Messenger, Microsoft Teams |
| Hard | ~15 min | LinkedIn, Google Chat |

**Easiest to set up:** WhatsApp (QR scan, ~1 min), Webhook (~1 min), Bluesky (~1 min).

**Channel message flow:**
```
User message on platform
    ↓ Channel Adapter receives + normalizes
    ↓ AgentRouter picks target agent
    ↓ Kernel sends to LLM
    ↓ Response formatted per ChannelOverrides
    ↓ Adapter sends reply back to platform
```

**Per-channel configuration options (`ChannelOverrides`):**
- Override LLM model per channel
- Custom system prompt per channel
- DM policy (Respond / Ignore)
- Group message policy
- Rate limit per user
- Threading mode
- Output format (Markdown / Plain / Code)
- Typing indicator mode

---

### 5.11 Skills

Skills extend agent capabilities. Three types supported:

| Type | Description | Example |
|------|-------------|---------|
| **Prompt-only** | Injects context/instructions into system prompt | `nano-pdf`, `code-review-guide` |
| **Python / Node.js** | Executable tools agents can call | CLI wrappers, scripts |
| **MCP Servers** | External tools via Model Context Protocol | GitHub, filesystem, databases |

#### Installed Skills (1)
```
nano-pdf  v0.1.0  (Prompt-only, OpenClaw)
"Edit PDFs with natural-language instructions using the nano-pdf CLI"
```

#### ClawHub Marketplace (3,000+ community skills)

**Top trending skills:**

| Skill | Downloads | Stars | Description |
|-------|-----------|-------|-------------|
| Gog | 81.4K | 622 | Google Workspace — Gmail, Drive, Calendar, Sheets, Docs |
| Summarize | 73.0K | 336 | Summarize URLs, PDFs, images, audio, YouTube |
| Github | 66.4K | 224 | GitHub CLI — issues, PRs, CI runs, API |
| Weather | 56.5K | 191 | Weather forecasts (no API key required) |
| Nano Pdf | 35.5K | 81 | PDF editing via natural language |
| Notion | 38.7K | 142 | Notion pages and databases |
| Nano Banana Pro | 33.3K | 152 | Image generation (Gemini 3 Pro) |
| Obsidian | 33.5K | 138 | Obsidian vault management |
| Openai Whisper | 30.3K | 159 | Local speech-to-text |
| Himalaya | 22.1K | 44 | Email via IMAP/SMTP CLI |

**Skill categories:** Coding & IDEs, Git & GitHub, Web & Frontend, DevOps & Cloud, Browser & Automation, Search & Research, AI & LLMs, Data & Analytics, Productivity, Communication, Media & Streaming, Notes & PKM, Security, CLI Utilities, Marketing & Sales, Finance, Smart Home & IoT, PDF & Documents.

#### MCP Servers (0 configured)
Config example:
```toml
[[mcp_servers]]
name = "filesystem"
timeout_secs = 30

[mcp_servers.transport]
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
```

#### Quick Start Skills (1-click, no code)
| Skill | Injects |
|-------|---------|
| `code-review-guide` | Code review best practices checklist |
| `writing-style` | Configurable writing style guide |
| `api-design` | REST API design patterns and conventions |
| `security-checklist` | OWASP-aligned security review checklist |

---

### 5.12 Hands

**Hands** are pre-configured autonomous agent packages with tuned system prompts, bundled tools, and custom metrics dashboards. Unlike regular agents (reactive, conversation-driven), Hands operate autonomously in the background.

| | Regular Agent (Chat) | Hand |
|--|----------------------|------|
| Setup | Manual configuration | Pre-configured |
| Interaction | User initiates | Autonomous |
| Tools | User selects | Pre-bundled |
| Dashboard | Basic | Custom metrics |
| Mode | Reactive | Autonomous / set-and-forget |

#### 7 Available Hands

| Hand | Tools | Metrics | Requirements | Status |
|------|-------|---------|--------------|--------|
| 🌐 Browser Hand | 18 | 3 | Python 3 + Playwright | Ready |
| 🎬 Clip Hand | 7 | 5 | FFmpeg + yt-dlp | Ready |
| 🔍 Collector Hand | 15 | 4 | None | Ready |
| 📊 Lead Hand | 14 | 4 | None | Ready |
| 🔮 Predictor Hand | 14 | 4 | None | Ready |
| 🧪 Researcher Hand | 15 | 4 | None | Ready |
| 𝕏 Twitter Hand | 15 | 4 | Twitter API Bearer Token | Setup needed |

**Hand descriptions:**
- **Browser Hand** — Autonomous web navigation: fills forms, clicks buttons, completes multi-step web tasks (with user approval for purchases)
- **Clip Hand** — Converts long-form video into viral short clips with captions and thumbnails
- **Collector Hand** — Continuously monitors any target with change detection and knowledge graphs
- **Lead Hand** — Discovers, enriches, and delivers qualified leads on a schedule
- **Predictor Hand** — Collects signals, builds reasoning chains, makes calibrated predictions, tracks accuracy
- **Researcher Hand** — Exhaustive investigation, cross-referencing, fact-checking, structured reports
- **Twitter Hand** — Content creation, scheduled posting, engagement, performance tracking

---

### 5.13 Settings → Providers

OpenFang supports **30 LLM providers** out of the box with a total of **150+ models**.

#### Provider Status at Walkthrough

| Status | Providers |
|--------|-----------|
| **Configured** | OpenAI ✓, OpenAI Codex ✓ |
| **No Key Needed (Local)** | Ollama, vLLM, LM Studio, Claude Code |
| **Not Configured** | 24 others |

#### All 30 Providers

| Provider | Models | Key Required | Notes |
|----------|--------|-------------|-------|
| Anthropic | 7 | Yes | `ANTHROPIC_API_KEY` |
| OpenAI | 16 | Yes ✓ | `OPENAI_API_KEY` (configured) |
| Google Gemini | 10 | Yes | `GEMINI_API_KEY` |
| DeepSeek | 4 | Yes | `DEEPSEEK_API_KEY` |
| Groq | 10 | Yes | `GROQ_API_KEY` |
| OpenRouter | 10 | Yes | `OPENROUTER_API_KEY` |
| Mistral AI | 6 | Yes | `MISTRAL_API_KEY` |
| Together AI | 8 | Yes | `TOGETHER_API_KEY` |
| Fireworks AI | 5 | Yes | `FIREWORKS_API_KEY` |
| Ollama | 7 | No | Local — `localhost:11434` |
| vLLM | 1 | No | Local — `localhost:8000` |
| LM Studio | 1 | No | Local — `localhost:1234` |
| Perplexity AI | 4 | Yes | `PERPLEXITY_API_KEY` |
| Cohere | 4 | Yes | `COHERE_API_KEY` |
| AI21 Labs | 3 | Yes | `AI21_API_KEY` |
| Cerebras | 4 | Yes | `CEREBRAS_API_KEY` |
| SambaNova | 3 | Yes | `SAMBANOVA_API_KEY` |
| Hugging Face | 3 | Yes | `HF_API_KEY` |
| xAI (Grok) | 6 | Yes | `XAI_API_KEY` |
| Replicate | 3 | Yes | `REPLICATE_API_TOKEN` |
| GitHub Copilot | 2 | Yes | `GITHUB_TOKEN` |
| Qwen (Alibaba) | 6 | Yes | `DASHSCOPE_API_KEY` |
| MiniMax | 4 | Yes | `MINIMAX_API_KEY` |
| Zhipu AI (GLM) | 4 | Yes | `ZHIPU_API_KEY` |
| Zhipu CodeGeeX | 1 | Yes | `ZHIPU_API_KEY` |
| Moonshot (Kimi) | 3 | Yes | `MOONSHOT_API_KEY` |
| Baidu Qianfan | 3 | Yes | `QIANFAN_API_KEY` |
| AWS Bedrock | 8 | Yes | `AWS_ACCESS_KEY_ID` |
| OpenAI Codex | 2 | Yes ✓ | Shares `OPENAI_API_KEY` |
| Claude Code | 3 | No | Local — `npm install -g @anthropic-ai/claude-code` |

**Other Settings sub-tabs (not fully explored):**
Models, Config, Tools, Security, Network, Budget, System, Migration.

---

## 6. Security Architecture

OpenFang runs **9 defense-in-depth security systems** simultaneously:

| System | What It Does |
|--------|-------------|
| **Merkle Audit** | Tamper-proof cryptographic hash chain for all agent actions |
| **Taint Tracking** | Marks and tracks untrusted data flowing through the system |
| **WASM Sandbox** | Agent tools run in isolated WebAssembly sandbox |
| **GCRA Rate Limit** | Token-bucket rate limiting to prevent abuse and spam |
| **Ed25519 Signing** | Cryptographic signing of messages/events |
| **SSRF Protection** | Blocks agents from making requests to internal network addresses |
| **Secret Zeroize** | Sensitive data (API keys) wiped from memory after use |
| **Loop Guard** | Detects and terminates infinite agent execution loops |
| **Session Repair** | Automatically recovers crashed or corrupted agent sessions |

Additionally:
- **Execution Approvals** — human-in-the-loop for sensitive actions
- **Tool allowlist/blocklist** — per-agent fine-grained tool permissions
- **Resource quotas** — per-agent CPU, memory, token, and cost limits
- **Network capability declarations** — agents must declare which domains they can reach

---

## 7. Deployment Considerations

### Current Setup (Local Dev)
```
Single machine
└── openfang.exe (daemon)
    └── ~/.openfang/openfang.db (SQLite)
    └── ~/.openfang/config.toml
    └── http://127.0.0.1:50051
```

### Cloud Deployment Challenges (AWS ECS)

| Challenge | Root Cause | Solution |
|-----------|-----------|---------|
| Data loss on restart | SQLite is file-based | Migrate to PostgreSQL / AWS RDS |
| Cannot scale horizontally | SQLite not shareable across containers | External DB with connection pooling |
| No shared agent state | Each container has own `.db` | Centralized database |
| Session routing | User session may hit different container | Sticky sessions or external session store |

### Recommended Production Architecture
```
Load Balancer
    ↓
ECS Containers (stateless openfang)
    ↓
AWS RDS PostgreSQL (shared state)
AWS ElastiCache (session caching)
AWS S3 (agent workspace files)
```

**Required code change:** Add pluggable backend to `openfang-memory` crate — SQLite for local dev, PostgreSQL for production.

---

## 8. Key Observations & Recommendations

### Strengths
1. **Comprehensive provider support** — 30 LLM providers, 150+ models, local + cloud
2. **40 messaging channels** — widest platform coverage seen in open-source agent platforms
3. **Strong security posture** — 9 layered security systems including WASM sandbox and tamper-evident audit trail
4. **Persistent memory** — 4-layer memory (structured, semantic, session, knowledge) with auto-consolidation
5. **Human-in-the-loop** — Execution Approvals prevent unchecked autonomous actions
6. **Scheduler** — Cron + event-driven automation built-in
7. **Skills ecosystem** — 3,000+ ClawHub skills, MCP server support, Python/Node.js tools
8. **Hands** — ready-made autonomous agents for common use cases (research, lead gen, browser, clips)
9. **Audit trail** — cryptographic hash chain suitable for compliance requirements
10. **Agent manifest system** — fine-grained control over capabilities, resources, and permissions per agent

### Areas for Improvement / Recommendations

| Area | Issue | Recommendation |
|------|-------|---------------|
| **Database** | SQLite — not suitable for cloud/ECS | Add PostgreSQL backend option |
| **Channels** | 0/40 configured at walkthrough | Set up at least Telegram/Webhook for demo |
| **Skills** | Only 1 installed (nano-pdf) | Install high-value skills: Gog, Github, Weather |
| **MCP Servers** | 0 configured | Configure filesystem or GitHub MCP |
| **Providers** | Only OpenAI configured | Add Groq (fast, free tier) for testing |
| **Twitter Hand** | Setup needed (API token required) | Obtain Twitter API Bearer Token |
| **Hands** | None activated | Activate Researcher Hand for demo |
| **Analytics** | All zeros — no LLM calls made | Run test messages to populate cost data |

---

## 9. References

### Codebase Locations
| Component | Path |
|-----------|------|
| Agent manifest types | `crates/openfang-types/src/agent.rs` |
| Kernel boot + agent lifecycle | `crates/openfang-kernel/src/kernel.rs` |
| API routes | `crates/openfang-api/src/routes.rs` |
| API server + AppState | `crates/openfang-api/src/server.rs` |
| Channel adapters | `crates/openfang-channels/src/` |
| Channel bridge + router | `crates/openfang-channels/src/bridge.rs`, `router.rs` |
| Memory substrate | `crates/openfang-memory/src/substrate.rs` |
| Semantic memory | `crates/openfang-memory/src/semantic.rs` |
| Session store | `crates/openfang-memory/src/session.rs` |
| Knowledge store | `crates/openfang-memory/src/knowledge.rs` |
| Memory consolidation | `crates/openfang-memory/src/consolidation.rs` |
| DB migrations | `crates/openfang-memory/src/migration.rs` |
| Bundled agents (30) | `crates/openfang-cli/src/bundled_agents.rs` |
| Hands registry | `crates/openfang-hands/src/registry.rs` |
| Config types | `crates/openfang-types/src/config.rs` |
| Dashboard UI | `static/index_body.html` |

### Configuration
| File | Purpose |
|------|---------|
| `~/.openfang/config.toml` | Main system configuration |
| `~/.openfang/agents/<name>/agent.toml` | Custom agent definitions |
| `~/.openfang/skills/` | User-installed skills |
| `~/.openfang/openfang.db` | SQLite database |
| `~/.openfang/workspaces/` | Agent workspace directories |

### External References
| Resource | URL |
|----------|-----|
| OpenFang Repository | `D:\openfang` (local) |
| ClawHub Skills Marketplace | Referenced in dashboard at `/skills` |
| Model Context Protocol (MCP) | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| OpenAI API | [platform.openai.com](https://platform.openai.com) |
| Ollama (local models) | [ollama.ai](https://ollama.ai) |
| rusqlite (SQLite for Rust) | [crates.io/crates/rusqlite](https://crates.io/crates/rusqlite) |

### Walkthrough Session Details
| Property | Value |
|----------|-------|
| Walkthrough date | March 4, 2026 |
| Daemon version | 0.2.7 |
| OS | Windows 11 |
| Build type | Release (`target/release/openfang.exe`) |
| LLM used | OpenAI gpt-4o-mini |
| Agents created during walkthrough | `my-assistant` |
| Dashboard URL | `http://127.0.0.1:50051/` |

---

*Report generated after a complete walkthrough of all dashboard tabs: Overview, Chat, Analytics, Logs, Audit Trail, Sessions, Memory, Execution Approvals, Agent Comms, Workflows, Scheduler, Channels, Skills, Hands, and Settings → Providers.*
