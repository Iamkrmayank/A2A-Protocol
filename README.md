# A2A Protocol — ResearchAgent

A production-ready implementation of Google's **Agent-to-Agent (A2A) protocol** using the **Agno** agent framework and **Azure OpenAI GPT-5**. Includes a fully streaming A2A server, a typed client, and interactive debug tooling — all from scratch.

---

## What This Is

The A2A protocol is an open standard by Google (launched April 2025) that lets AI agents talk to each other across frameworks, languages, and platforms using JSON-RPC 2.0 over HTTP + Server-Sent Events.

This project shows you:

- How to wrap any agent into a compliant A2A server
- How to build a typed A2A client that streams token-by-token responses
- How every message, task, event, and artifact flows through the protocol
- How to run both in one terminal with full color-coded debug output

---

## Project Structure

```
A2A-Protocol/
├── agent.py          # Agno ResearchAgent definition (Azure OpenAI GPT-5)
├── server.py         # A2A server — AgentExecutor + FastAPI + SSE streaming
├── client.py         # A2A client — ClientFactory, all 5 demo operations
├── test_live.py      # Live test: shows every A2A event with labels
├── test_debug.py     # Debug test: server + client in ONE terminal, colored
├── .env              # Azure OpenAI credentials (never commit this)
└── requirements.txt  # Python dependencies
```

---

## Prerequisites

- Python 3.10+
- Azure OpenAI deployment (GPT-4 or GPT-5)

---

## Setup

**1. Clone / create the project folder**

```bash
mkdir A2A-Protocol && cd A2A-Protocol
```

**2. Install dependencies**

```bash
pip install agno a2a-sdk openai fastapi "uvicorn[standard]" httpx httpx-sse python-dotenv
```

**3. Create your `.env` file**

```env
AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.cognitiveservices.azure.com
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

> **Never commit `.env` to version control.** Add it to `.gitignore`.

---

## Running

### Option A — Two terminals (server + client separately)

**Terminal 1 — Start the server**

```bash
python server.py
```

Output:
```
============================================================
  A2A ResearchAgent Server
============================================================
  Agent Card :  http://localhost:8000/.well-known/agent-card.json
  JSON-RPC   :  POST http://localhost:8000/
  Streaming  :  POST http://localhost:8000/ (SSE)
============================================================
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 — Run the client demos**

```bash
python client.py
```

Runs 5 demos: agent discovery, streaming message, conversation resume, JSON DataPart, and GET task by ID.

---

### Option B — One terminal with full debug trace

```bash
python test_debug.py
```

Starts the server as a subprocess, then runs client requests — everything interleaved with color tags:

| Tag | Color | Meaning |
|-----|-------|---------|
| `[SERVER]` | Green | Uvicorn HTTP logs + AgentExecutor steps |
| `[CLIENT]` | Cyan | What the client sends + final summary |
| `[EVENT ]` | Yellow | Every A2A event (status updates, artifact open/close) |
| `[CHUNK ]` | Grey | Every raw token as `repr()` — exactly what the LLM streamed |

---

### Option C — Labeled live test (no subprocess)

```bash
# Start server first
python server.py

# Then in another terminal
python test_live.py
```

Shows events with section headers per test, chunk counts, and conversation history.

---

### Option D — Test the agent directly (no A2A)

```bash
python agent.py
```

Calls the Agno agent directly, bypassing the A2A layer. Useful for testing prompt/instruction changes.

---

## How the Protocol Works

### Discovery — AgentCard

Every A2A server exposes its identity at a well-known URL:

```
GET /.well-known/agent-card.json
```

```json
{
  "name": "ResearchAgent",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "defaultInputModes": ["text/plain", "text/markdown", "application/json"],
  "defaultOutputModes": ["text/markdown"],
  "skills": [
    { "id": "research",    "name": "Research & Q&A" },
    { "id": "code_review", "name": "Code Review" },
    { "id": "summarize",   "name": "Summarization" }
  ]
}
```

### Sending a Message

All requests are JSON-RPC 2.0 posted to `POST /`:

```json
{
  "jsonrpc": "2.0",
  "id": "req-1",
  "method": "message/stream",
  "params": {
    "message": {
      "role": "user",
      "messageId": "uuid",
      "parts": [
        { "kind": "text", "text": "What is the A2A protocol?" }
      ]
    },
    "configuration": {
      "blocking": false,
      "historyLength": 5,
      "acceptedOutputModes": ["text/markdown"]
    }
  }
}
```

### What the Client Can Send

| Field | Type | Purpose |
|-------|------|---------|
| `message.parts` | `TextPart \| FilePart \| DataPart \| ArtifactPart` | The actual payload |
| `message.context_id` | string | Groups messages into a conversation/session |
| `message.task_id` | string | Attaches to an existing in-progress task |
| `message.message_id` | string | Deduplication / idempotency key |
| `message.reference_task_ids` | string[] | Related task IDs for cross-task context |
| `message.metadata` | dict | Arbitrary key→value passed to the server |
| `configuration.blocking` | bool | `true` = wait for terminal state before returning |
| `configuration.history_length` | int | How many prior messages server returns |
| `configuration.accepted_output_modes` | string[] | MIME types the client can handle |
| `configuration.push_notification_config` | object | Webhook URL for async delivery |

### Task Lifecycle

Every request creates (or resumes) a Task that moves through states:

```
submitted
    │
    ▼
 working ──────────────────────────────┐
    │                                  │
    ▼                                  ▼
input-required             auth-required
    │
    ▼
completed  ──  failed  ──  canceled  ──  rejected
```

### Streaming Events (SSE)

The server sends a stream of Server-Sent Events. Each SSE `data` field is a complete JSON-RPC response:

```
TaskStatusUpdateEvent     → state change (working, completed, failed...)
TaskArtifactUpdateEvent   → token chunk (last_chunk=false) or final (last_chunk=true)
```

Token chunks arrive with `last_chunk: false` until the stream closes:

```
chunk[001] "The"
chunk[002] " A2A"
chunk[003] " protocol"
...
chunk[080] "."        last_chunk: true  ← stream closed
```

### 11 Protocol Operations

| Method | What it does |
|--------|-------------|
| `message/send` | Send message, wait for response (blocking or immediate) |
| `message/stream` | Send message, receive SSE stream of events |
| `tasks/get` | Retrieve a task by ID |
| `tasks/list` | Paginated task list (filter by context, status, time) |
| `tasks/cancel` | Request task cancellation |
| `tasks/resubscribe` | Re-open SSE stream on an existing task |
| `tasks/pushNotificationConfig/set` | Register a webhook |
| `tasks/pushNotificationConfig/get` | Retrieve webhook config |
| `tasks/pushNotificationConfig/list` | List all webhooks for a task |
| `tasks/pushNotificationConfig/delete` | Remove a webhook |
| `agent/authenticatedExtendedCard` | Get auth-gated AgentCard |

---

## How Token Streaming Works

The core challenge: Agno's generator is **synchronous**, but A2A's `execute()` is **async**.

```
Thread (Agno generator)                  Async event loop (A2A server)
───────────────────────                  ──────────────────────────────
agent.run(text,                          async def execute(context, event_queue):
  stream=True,                               chunk_queue = asyncio.Queue()
  stream_events=True)                        loop.run_in_executor(None, _run_agent)
       │                                          │
RunContentEvent("The ")  ──────────────►  chunk_queue  ──►  TaskArtifactUpdateEvent
RunContentEvent("A2A ")  ──────────────►  chunk_queue  ──►  TaskArtifactUpdateEvent
RunContentEvent("prot")  ──────────────►  chunk_queue  ──►  TaskArtifactUpdateEvent
("done", None)           ──────────────►  chunk_queue  ──►  TaskArtifactUpdateEvent(last_chunk=True)
                                                            TaskStatusUpdateEvent(completed)
```

The bridge is `asyncio.Queue` + `loop.call_soon_threadsafe()` — the only safe way to push from a blocking thread into an async event loop.

---

## Agno Agent Configuration

The `Agent` class in `agent.py` accepts these key parameters:

| Parameter | Purpose |
|-----------|---------|
| `model` | The LLM backend — `AzureOpenAI`, `OpenAI`, `Anthropic`, etc. |
| `name` | Display name used in logs and context |
| `description` | One-line summary (appears in AgentCard) |
| `instructions` | System prompt — accepts `str` or `list[str]` |
| `markdown` | Format all responses in Markdown |
| `tools` | List of callable tools the agent can invoke |
| `memory_manager` | Cross-session memory storage |
| `knowledge` | RAG knowledge base |
| `add_datetime_to_context` | Auto-inject current date/time |
| `stream` | Default streaming mode |
| `debug_mode` | Print detailed internal logs |
| `tool_call_limit` | Max tool calls per run |
| `reasoning` | Enable step-by-step reasoning |

---

## Key Limitations

| Limitation | Detail |
|-----------|--------|
| In-memory task store | `InMemoryTaskStore` — all tasks lost on restart. Swap for Redis/PostgreSQL in production |
| No auth enforcement | `security_schemes` are declared in AgentCard but not enforced by this server |
| No push notifications | `capabilities.pushNotifications = false` — webhooks not implemented |
| Agno telemetry | Agno sends anonymous run telemetry to `os-api.agno.com` — disable with `telemetry=False` in `Agent()` |
| Windows encoding | Python 3.10 on Windows defaults to CP1252 — wrap stdout with `io.TextIOWrapper(..., encoding='utf-8')` |

---

## A2A Error Codes

| Error | When it occurs |
|-------|---------------|
| `TaskNotFoundError` | Task ID expired, invalid, or not in store |
| `TaskNotCancelableError` | Task already in terminal state |
| `PushNotificationNotSupportedError` | Agent declared `pushNotifications: false` |
| `ContentTypeNotSupportedError` | Client requested unsupported MIME type |
| `UnsupportedOperationError` | Method not implemented by this server |
| `VersionNotSupportedError` | Client/server A2A version mismatch |

---

## Stack

| Layer | Technology |
|-------|-----------|
| Agent framework | [Agno](https://docs.agno.com) v2.5+ |
| LLM | Azure OpenAI (GPT-5 / GPT-4o) |
| A2A SDK | [a2a-sdk](https://github.com/a2aproject/a2a-python) v0.3.x |
| HTTP server | FastAPI + Uvicorn |
| Streaming | Server-Sent Events (SSE) via `sse-starlette` |
| HTTP client | `httpx` + `httpx-sse` |
| Protocol | JSON-RPC 2.0 over HTTP |

---

## References

- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A Python SDK — GitHub](https://github.com/a2aproject/a2a-python)
- [Agno Agent Framework](https://docs.agno.com)
- [Google A2A Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
