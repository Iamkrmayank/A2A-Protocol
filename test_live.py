"""
Live Test — Watch Server & Client in Action
============================================
Runs a series of real requests and prints:
  - What the CLIENT sends
  - What A2A events the SERVER returns (raw)
  - The streamed token output live

Run:
    python test_live.py
"""

import asyncio
import sys
import io
import httpx
import uuid
import dataclasses

# Fix Windows console encoding
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from a2a.client import ClientFactory, ClientConfig, A2ACardResolver
from a2a.client.helpers import create_text_message_object
from a2a.types import (
    Message, Part, TextPart, DataPart, Role,
    TaskStatusUpdateEvent, TaskArtifactUpdateEvent,
    TaskQueryParams,
)

SERVER = "http://localhost:8000"
SEP    = "=" * 70
THIN   = "-" * 70


# ── helpers ──────────────────────────────────────────────────────────────────

def msg(text: str, context_id: str | None = None) -> Message:
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


# ── core streaming runner ─────────────────────────────────────────────────────

async def run_test(
    factory: ClientFactory,
    card,
    label: str,
    message: Message,
    show_raw_events: bool = True,
):
    print(f"\n{SEP}")
    print(f"  TEST: {label}")
    print(SEP)

    # ── Show what we're sending ───────────────────────────────────────────────
    print("\n[CLIENT -> SERVER]")
    for part in message.parts:
        if isinstance(part.root, TextPart):
            print(f"  TextPart  : {part.root.text[:120]}")
        elif isinstance(part.root, DataPart):
            print(f"  DataPart  : {part.root.data}")
    if message.context_id:
        print(f"  context_id: {message.context_id}")
    print(f"  message_id: {message.message_id}")

    # ── Stream events from server ─────────────────────────────────────────────
    client   = factory.create(card)
    task_id  = None
    ctx_id   = None
    chunks   = 0

    print(f"\n[SERVER -> CLIENT]  (streaming events)\n")

    async for event in client.send_message(message):
        task, update = event

        # Capture IDs from first task snapshot
        if task_id is None:
            task_id = task.id
            ctx_id  = task.context_id
            if show_raw_events:
                print(f"  Task created  : id={task_id}")
                print(f"  Context       : id={ctx_id}\n")

        if update is None:
            continue

        # ── Status events ─────────────────────────────────────────────────────
        if isinstance(update, TaskStatusUpdateEvent):
            state = update.status.state.value
            text  = extract_status_text(update)
            final = update.final
            if show_raw_events:
                print(f"\n  [StatusUpdateEvent]  state={state!r}  final={final}  msg={text!r}")

        # ── Artifact events (token chunks) ────────────────────────────────────
        elif isinstance(update, TaskArtifactUpdateEvent):
            art = update.artifact

            # First chunk of this artifact: print header
            if chunks == 0:
                if show_raw_events:
                    print(f"\n  [ArtifactUpdateEvent] artifact_id={art.artifact_id!r}  name={art.name!r}")
                    print(f"  --- streaming tokens below ---\n")

            for part in art.parts:
                if isinstance(part.root, TextPart) and part.root.text:
                    print(part.root.text, end="", flush=True)
                    chunks += 1

            if update.last_chunk:
                print(f"\n\n  --- stream ended ({chunks} chunks) ---")

    # ── Final summary ─────────────────────────────────────────────────────────
    print(f"\n{THIN}")
    print(f"  Final task state : {task.status.state.value}")
    print(f"  Task ID          : {task_id}")
    print(f"  Context ID       : {ctx_id}")
    print(THIN)

    return task_id, ctx_id


# ── individual tests ──────────────────────────────────────────────────────────

async def test_get_task(factory, card, task_id: str):
    """Show the stored task retrieved by ID after completion."""
    print(f"\n{SEP}")
    print(f"  TEST: GET TASK by ID (task store lookup)")
    print(SEP)
    print(f"\n[CLIENT -> SERVER]  GET task id={task_id}")

    client = factory.create(card)
    task   = await client.get_task(TaskQueryParams(id=task_id, history_length=10))

    print(f"\n[SERVER -> CLIENT]  Task snapshot")
    print(f"  id         : {task.id}")
    print(f"  state      : {task.status.state.value}")
    print(f"  context_id : {task.context_id}")
    print(f"  artifacts  : {len(task.artifacts or [])}")
    print(f"  history    : {len(task.history or [])} messages")
    if task.artifacts:
        art = task.artifacts[0]
        print(f"\n  Stored artifact '{art.name}':")
        full_text = "".join(
            p.root.text for p in art.parts if isinstance(p.root, TextPart)
        )
        print(f"  {full_text[:300]}...")


# ── main ──────────────────────────────────────────────────────────────────────

async def main():
    print(SEP)
    print("  A2A LIVE TEST — Server + Client Trace")
    print(SEP)

    config = ClientConfig(streaming=True)

    async with httpx.AsyncClient(timeout=180.0) as http:

        # ── Discover agent ────────────────────────────────────────────────────
        print("\n[AGENT CARD]  Fetching from /.well-known/agent-card.json")
        resolver = A2ACardResolver(httpx_client=http, base_url=SERVER)
        card     = await resolver.get_agent_card()
        factory  = ClientFactory(config=dataclasses.replace(config, httpx_client=http))

        print(f"  Agent : {card.name} v{card.version}")
        print(f"  Skills: {[s.id for s in card.skills]}")
        print(f"  Caps  : streaming={card.capabilities.streaming}  push={card.capabilities.push_notifications}")

        # ── TEST 1: Simple Q&A ────────────────────────────────────────────────
        task_id, ctx_id = await run_test(
            factory, card,
            label   = "Simple Q&A — token streaming",
            message = msg("Explain what JSON-RPC 2.0 is in 3 bullet points."),
        )

        # ── TEST 2: Multi-turn conversation (same context_id) ─────────────────
        await run_test(
            factory, card,
            label      = "Multi-turn — follow-up in SAME conversation",
            message    = msg("Now add one more bullet about error handling.", context_id=ctx_id),
            show_raw_events=True,
        )

        # ── TEST 3: Structured JSON input (DataPart) ──────────────────────────
        await run_test(
            factory, card,
            label   = "Structured DataPart — JSON code review",
            message = json_msg({
                "task"    : "summarize",
                "content" : (
                    "The A2A protocol uses JSON-RPC 2.0 over HTTP/SSE. "
                    "Clients send Message objects with TextPart, FilePart, or DataPart payloads. "
                    "Servers respond with Task objects that track lifecycle states: "
                    "submitted, working, input-required, completed, failed, canceled. "
                    "Streaming is done via Server-Sent Events. "
                    "The AgentCard is the discovery document at /.well-known/agent-card.json."
                ),
                "format"  : "3 bullet points, max 20 words each",
            }),
        )

        # ── TEST 4: Retrieve completed task from store ────────────────────────
        if task_id:
            await test_get_task(factory, card, task_id)

    print(f"\n{SEP}")
    print("  ALL TESTS PASSED")
    print(SEP + "\n")


if __name__ == "__main__":
    asyncio.run(main())
