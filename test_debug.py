"""
Debug Test — Server + Client in ONE terminal
============================================
Starts the A2A server as a subprocess, captures its stdout/stderr
and prefixes every line with a colored [SERVER] tag.

The client runs in the same process with [CLIENT] tags.

Everything streams into one terminal so you can watch the full
request/response cycle step by step.

Run:
    python test_debug.py
"""

import asyncio
import subprocess
import sys
import io
import threading
import time
import uuid
import dataclasses
import httpx

# ── Unicode-safe stdout ───────────────────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from a2a.client import ClientFactory, ClientConfig, A2ACardResolver
from a2a.client.helpers import create_text_message_object
from a2a.types import (
    Message, Part, TextPart, DataPart, Role,
    TaskStatusUpdateEvent, TaskArtifactUpdateEvent,
    TaskQueryParams,
)

# ── ANSI colors ───────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

SERVER_TAG = f"{GREEN}{BOLD}[SERVER]{RESET}"
CLIENT_TAG = f"{CYAN}{BOLD}[CLIENT]{RESET}"
EVENT_TAG  = f"{YELLOW}{BOLD}[EVENT ]{RESET}"
CHUNK_TAG  = f"{GREY}[CHUNK ]{RESET}"
ERROR_TAG  = f"{RED}{BOLD}[ERROR ]{RESET}"
SEP        = f"{BOLD}" + "=" * 70 + RESET
THIN       = "-" * 70

SERVER_URL = "http://localhost:8000"


# ── Server subprocess launcher ────────────────────────────────────────────────

def _pipe_server_output(proc: subprocess.Popen):
    """
    Background thread: reads server stdout+stderr line by line
    and prints each one prefixed with [SERVER].
    """
    for raw in proc.stdout:
        line = raw.rstrip("\n")
        if not line:
            continue
        # Colour-code common uvicorn log levels
        if "ERROR" in line or "error" in line.lower():
            print(f"{ERROR_TAG} {line}", flush=True)
        elif "WARNING" in line or "WARNING" in line:
            print(f"{YELLOW}[WARN  ]{RESET} {line}", flush=True)
        elif "INFO" in line:
            print(f"{SERVER_TAG} {line}", flush=True)
        elif "DEBUG" in line:
            print(f"{GREY}[DEBUG ]{RESET} {line}", flush=True)
        else:
            print(f"{SERVER_TAG} {line}", flush=True)


def start_server() -> subprocess.Popen:
    """Launch server.py as a child process and stream its output."""
    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,       # merge stderr into stdout
        text=True,
        bufsize=1,                      # line-buffered
        cwd="D:/A2A-Protocol",
    )
    t = threading.Thread(target=_pipe_server_output, args=(proc,), daemon=True)
    t.start()
    return proc


def wait_for_server(timeout: int = 15) -> bool:
    """Poll until the server is accepting connections."""
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{SERVER_URL}/.well-known/agent-card.json", timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False


# ── Message helpers ───────────────────────────────────────────────────────────

def text_msg(text: str, context_id: str | None = None) -> Message:
    m = create_text_message_object(role=Role.user, content=text)
    if context_id:
        m = Message(**{**m.model_dump(), "context_id": context_id})
    return m


def json_msg(data: dict) -> Message:
    return Message(
        role=Role.user,
        parts=[Part(root=DataPart(data=data))],
        message_id=str(uuid.uuid4()),
    )


def extract_status_text(update: TaskStatusUpdateEvent) -> str:
    if update.status.message:
        for p in update.status.message.parts:
            if isinstance(p.root, TextPart):
                return p.root.text
    return ""


# ── Core runner: one request with full step-by-step trace ────────────────────

async def run_request(factory, card, label: str, message: Message):
    print(f"\n{SEP}")
    print(f"  {BOLD}{label}{RESET}")
    print(SEP)

    # ── Step 1: What the client is sending ───────────────────────────────────
    print(f"\n{CLIENT_TAG} Preparing request")
    for part in message.parts:
        if isinstance(part.root, TextPart):
            print(f"{CLIENT_TAG}   TextPart    : {part.root.text[:100]}")
        elif isinstance(part.root, DataPart):
            print(f"{CLIENT_TAG}   DataPart    : {part.root.data}")
    if message.context_id:
        print(f"{CLIENT_TAG}   context_id  : {message.context_id}")
    print(f"{CLIENT_TAG}   message_id  : {message.message_id}")
    print(f"{CLIENT_TAG}   → POST {SERVER_URL}/  (JSON-RPC: message/stream)")

    # ── Step 2: Open SSE stream and iterate events ────────────────────────────
    client   = factory.create(card)
    task_id  = None
    ctx_id   = None
    chunks   = 0
    total_ch = 0
    event_n  = 0

    print(f"\n{CLIENT_TAG} Waiting for server response...\n")

    async for raw_event in client.send_message(message):
        task, update = raw_event
        event_n += 1

        # First event: task was created
        if task_id is None:
            task_id = task.id
            ctx_id  = task.context_id
            print(f"{EVENT_TAG} #{event_n:02d}  Task CREATED")
            print(f"{EVENT_TAG}       task_id    = {task_id}")
            print(f"{EVENT_TAG}       context_id = {ctx_id}")
            print(f"{EVENT_TAG}       state      = {task.status.state.value!r}")

        if update is None:
            continue

        # ── Status update ─────────────────────────────────────────────────────
        if isinstance(update, TaskStatusUpdateEvent):
            state    = update.status.state.value
            msg_text = extract_status_text(update)
            final    = update.final
            print(f"\n{EVENT_TAG} #{event_n:02d}  TaskStatusUpdateEvent")
            print(f"{EVENT_TAG}       state   = {state!r}")
            print(f"{EVENT_TAG}       message = {msg_text!r}")
            print(f"{EVENT_TAG}       final   = {final}")

        # ── Artifact update (token chunks) ────────────────────────────────────
        elif isinstance(update, TaskArtifactUpdateEvent):
            art = update.artifact

            if chunks == 0:
                print(f"\n{EVENT_TAG} #{event_n:02d}  TaskArtifactUpdateEvent — stream OPEN")
                print(f"{EVENT_TAG}       artifact_id = {art.artifact_id!r}")
                print(f"{EVENT_TAG}       name        = {art.name!r}")
                print(f"{EVENT_TAG}       last_chunk  = {update.last_chunk}")
                print(f"\n{CLIENT_TAG} Token stream:\n")

            for part in art.parts:
                if isinstance(part.root, TextPart) and part.root.text:
                    token = part.root.text
                    total_ch += len(token)
                    chunks   += 1
                    # Show each raw chunk with its index in grey, then the text
                    print(f"{CHUNK_TAG}[{chunks:04d}] {repr(token)}", flush=True)

            if update.last_chunk:
                print(f"\n{EVENT_TAG} #{event_n:02d}  TaskArtifactUpdateEvent — stream CLOSED")
                print(f"{EVENT_TAG}       total chunks = {chunks}")
                print(f"{EVENT_TAG}       total chars  = {total_ch}")
                print(f"{EVENT_TAG}       last_chunk   = True")

    # ── Step 3: Final task summary ────────────────────────────────────────────
    print(f"\n{CLIENT_TAG} Request complete")
    print(f"{CLIENT_TAG}   final state : {task.status.state.value!r}")
    print(f"{CLIENT_TAG}   task_id     : {task_id}")
    print(f"{CLIENT_TAG}   context_id  : {ctx_id}")
    print(f"{CLIENT_TAG}   total events: {event_n}")
    print(THIN)

    return task_id, ctx_id


# ── GET task by ID ────────────────────────────────────────────────────────────

async def get_task(factory, card, task_id: str):
    print(f"\n{SEP}")
    print(f"  {BOLD}GET TASK — retrieve stored task from server{RESET}")
    print(SEP)
    print(f"\n{CLIENT_TAG} → GET task/{task_id}")

    client = factory.create(card)
    task   = await client.get_task(TaskQueryParams(id=task_id, history_length=10))

    print(f"\n{EVENT_TAG}  Task snapshot received")
    print(f"{EVENT_TAG}    id        : {task.id}")
    print(f"{EVENT_TAG}    state     : {task.status.state.value!r}")
    print(f"{EVENT_TAG}    context   : {task.context_id}")
    print(f"{EVENT_TAG}    artifacts : {len(task.artifacts or [])}")
    print(f"{EVENT_TAG}    history   : {len(task.history or [])} messages")

    if task.history:
        print(f"\n{EVENT_TAG}  Conversation history:")
        for i, h in enumerate(task.history):
            for p in h.parts:
                if isinstance(p.root, TextPart):
                    print(f"{EVENT_TAG}    [{i}] {h.role.value}: {p.root.text[:80]}")

    if task.artifacts:
        print(f"\n{EVENT_TAG}  Artifact content (first 200 chars):")
        for art in task.artifacts:
            full = "".join(
                p.root.text for p in art.parts if isinstance(p.root, TextPart)
            )
            print(f"{EVENT_TAG}    '{art.name}': {full[:200]}...")


# ── Main ──────────────────────────────────────────────────────────────────────

async def run_client(factory, card):
    """All client-side tests."""

    # TEST 1 — Simple Q&A
    task_id, ctx_id = await run_request(
        factory, card,
        label   = "TEST 1 — Simple Q&A (TextPart, no context)",
        message = text_msg("What is JSON-RPC 2.0? Answer in exactly 2 sentences."),
    )

    # TEST 2 — Multi-turn (same context_id)
    await run_request(
        factory, card,
        label      = "TEST 2 — Multi-turn follow-up (same context_id)",
        message    = text_msg(
            "Now give one sentence on how A2A uses JSON-RPC.",
            context_id=ctx_id,
        ),
    )

    # TEST 3 — Structured JSON (DataPart)
    await run_request(
        factory, card,
        label   = "TEST 3 — Structured DataPart (JSON payload)",
        message = json_msg({
            "action" : "summarize",
            "text"   : (
                "The A2A protocol defines 11 JSON-RPC methods. "
                "It uses SSE for streaming. Tasks go through states: "
                "submitted, working, completed, failed, canceled. "
                "The AgentCard at /.well-known/agent-card.json describes skills."
            ),
            "style"  : "one sentence",
        }),
    )

    # TEST 4 — GET task
    if task_id:
        await get_task(factory, card, task_id)


async def main():
    # ── Kill any existing server on port 8000 ────────────────────────────────
    import socket
    with socket.socket() as s:
        if s.connect_ex(("localhost", 8000)) == 0:
            print(f"{YELLOW}[WARN  ]{RESET} Port 8000 in use — killing old server...")
            import subprocess as sp
            sp.run(
                'for /f "tokens=5" %p in (\'netstat -ano ^| findstr :8000 ^| findstr LISTENING\') '
                'do wmic process where ProcessId=%p delete',
                shell=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL
            )
            time.sleep(2)

    print(SEP)
    print(f"  {BOLD}A2A DEBUG TEST — Server + Client trace{RESET}")
    print(SEP)
    print(f"\n{SERVER_TAG} Starting server subprocess...")

    proc = start_server()

    if not wait_for_server(timeout=15):
        print(f"{ERROR_TAG} Server did not start in time.")
        proc.terminate()
        return

    print(f"{SERVER_TAG} Server is UP at {SERVER_URL}\n")
    time.sleep(0.5)   # let any startup logs flush

    # ── Run client tests ──────────────────────────────────────────────────────
    config = ClientConfig(streaming=True)
    async with httpx.AsyncClient(timeout=180.0) as http:
        resolver = A2ACardResolver(httpx_client=http, base_url=SERVER_URL)
        card     = await resolver.get_agent_card()
        factory  = ClientFactory(config=dataclasses.replace(config, httpx_client=http))

        print(f"{CLIENT_TAG} AgentCard resolved: {card.name} v{card.version}")
        await run_client(factory, card)

    print(f"\n{SEP}")
    print(f"  {BOLD}ALL TESTS DONE — shutting down server{RESET}")
    print(SEP + "\n")

    proc.terminate()
    proc.wait()


if __name__ == "__main__":
    asyncio.run(main())
