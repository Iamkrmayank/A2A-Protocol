"""
A2A Client -- Interacting with the ResearchAgent Server
=======================================================
Uses the modern ClientFactory API (a2a-sdk 0.3.x).

Demonstrates:
  1. Resolve the AgentCard (discover what the server can do)
  2. Send a message and iterate over events (streaming by default)
  3. Resume a conversation with the same context_id
  4. Send structured JSON data (DataPart)
  5. Get task status by ID

Run
---
    # Start server first:  python server.py
    # Then:                python client.py
"""

import asyncio
import httpx
import uuid
import dataclasses
import sys

# Fix Windows console encoding for unicode/emoji from LLM responses
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from a2a.client import ClientFactory, ClientConfig, A2ACardResolver
from a2a.client.helpers import create_text_message_object
from a2a.types import (
    Message,
    Part,
    TextPart,
    DataPart,
    Role,
    Task,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    TaskQueryParams,
)

SERVER_URL = "http://localhost:8000"


# -----------------------------------------------------------------------
# Helpers for building messages
# -----------------------------------------------------------------------

def make_text_message(text: str, context_id: str | None = None) -> Message:
    """
    Build a Message with a TextPart.

    Message fields you can set
    --------------------------
    role             - Role.user from the client side
    parts            - list[Part]: TextPart, FilePart, DataPart, ArtifactPart
    context_id       - groups messages into one conversation/session
    task_id          - attach to an existing in-progress task
    message_id       - unique ID for idempotency / deduplication
    reference_task_ids - IDs of related tasks for context
    metadata         - arbitrary dict[str, Any] passed to server
    """
    msg = create_text_message_object(role=Role.user, content=text)
    if context_id:
        msg = Message(**{**msg.model_dump(), "context_id": context_id})
    return msg


def make_json_message(data: dict, context_id: str | None = None) -> Message:
    """Build a Message with structured JSON data (DataPart)."""
    return Message(
        role=Role.user,
        parts=[Part(root=DataPart(data=data))],
        context_id=context_id,
        message_id=str(uuid.uuid4()),
    )


# -----------------------------------------------------------------------
# Event printer — handles token-by-token streaming
# -----------------------------------------------------------------------

# Track whether we are mid-stream so we know when to print a header/newline
_streaming_artifact: dict = {"active": False, "artifact_id": None}

def print_event(event, label: str = "") -> "Task | None":
    """
    Pretty-print any A2A event/response.

    Streaming artifact chunks (last_chunk=False) are printed inline without
    newlines so they appear as a continuous flowing stream on the terminal.
    The final chunk (last_chunk=True) closes the stream with a newline.
    """
    prefix = f"  [{label}]" if label else "  "

    if isinstance(event, tuple):
        task, update = event

        if update is None:
            # Plain task snapshot (no update event)
            if _streaming_artifact["active"]:
                print()  # close any open stream line
                _streaming_artifact["active"] = False
            print(f"{prefix} Task state: {task.status.state.value}")

        elif isinstance(update, TaskStatusUpdateEvent):
            if _streaming_artifact["active"]:
                print()
                _streaming_artifact["active"] = False
            state = update.status.state.value
            msg_text = ""
            if update.status.message:
                for p in update.status.message.parts:
                    if isinstance(p.root, TextPart):
                        msg_text = p.root.text
                        break
            print(f"{prefix} Status -> {state}  {msg_text}")

        elif isinstance(update, TaskArtifactUpdateEvent):
            art = update.artifact
            art_id = art.artifact_id

            # New artifact — print header
            if not _streaming_artifact["active"] or _streaming_artifact["artifact_id"] != art_id:
                print(f"\n{prefix} Streaming artifact: '{art.name}'\n")
                _streaming_artifact["active"] = True
                _streaming_artifact["artifact_id"] = art_id

            # Print each chunk inline (no newline — let the text flow naturally)
            for part in art.parts:
                if isinstance(part.root, TextPart) and part.root.text:
                    print(part.root.text, end="", flush=True)

            # Last chunk — close the stream
            if update.last_chunk:
                print()  # final newline
                _streaming_artifact["active"] = False

        return task

    elif isinstance(event, Message):
        if _streaming_artifact["active"]:
            print()
            _streaming_artifact["active"] = False
        print(f"{prefix} Direct Message reply:")
        for part in event.parts:
            if isinstance(part.root, TextPart):
                print(part.root.text[:800])
        return None


# -----------------------------------------------------------------------
# Demo 1: Discover the agent
# -----------------------------------------------------------------------
async def demo_discover(http: httpx.AsyncClient):
    print("\n" + "=" * 60)
    print("DEMO 1: Discover Agent (AgentCard)")
    print("=" * 60)

    resolver = A2ACardResolver(httpx_client=http, base_url=SERVER_URL)
    card = await resolver.get_agent_card()

    print(f"  Name        : {card.name}")
    print(f"  Description : {card.description}")
    print(f"  Version     : {card.version}")
    print(f"  Streaming   : {card.capabilities.streaming}")
    print(f"  Push Notifs : {card.capabilities.push_notifications}")
    print(f"  Input modes : {card.default_input_modes}")
    print(f"  Output modes: {card.default_output_modes}")
    print(f"\n  Skills ({len(card.skills)}):")
    for skill in card.skills:
        print(f"    [{skill.id}] {skill.name}")
        print(f"      {skill.description}")
        if skill.examples:
            print(f"      Examples: {skill.examples[0]}")

    return card


# -----------------------------------------------------------------------
# Demo 2: Send a message and consume events
# -----------------------------------------------------------------------
async def demo_send_message(factory: ClientFactory, card):
    print("\n" + "=" * 60)
    print("DEMO 2: Send Message and Stream Events")
    print("=" * 60)

    client = factory.create(card)
    message = make_text_message("What is the A2A protocol and why is it important?")

    print(f"  Sending: {message.parts[0].root.text}\n")

    last_task = None
    async for event in client.send_message(message):
        last_task = print_event(event, "EVENT")

    context_id = None
    if last_task:
        context_id = last_task.context_id
        print(f"\n  Task ID    : {last_task.id}")
        print(f"  Context ID : {context_id}")
        print(f"  Final state: {last_task.status.state.value}")

    return last_task.id if last_task else None, context_id


# -----------------------------------------------------------------------
# Demo 3: Resume conversation (same context_id)
# -----------------------------------------------------------------------
async def demo_resume_conversation(factory: ClientFactory, card, context_id: str):
    print("\n" + "=" * 60)
    print("DEMO 3: Resume Conversation (same context_id)")
    print("=" * 60)

    client = factory.create(card)
    message = make_text_message(
        "Now explain only the TaskState transitions in a compact table.",
        context_id=context_id,
    )

    print(f"  context_id: {context_id}")
    print(f"  Asking follow-up question...\n")

    async for event in client.send_message(message):
        print_event(event, "EVENT")


# -----------------------------------------------------------------------
# Demo 4: Send structured JSON (DataPart)
# -----------------------------------------------------------------------
async def demo_json_message(factory: ClientFactory, card):
    print("\n" + "=" * 60)
    print("DEMO 4: Send Structured JSON Data (DataPart)")
    print("=" * 60)

    client = factory.create(card)

    # Sending a code-review request as structured JSON
    message = make_json_message({
        "task": "code_review",
        "language": "python",
        "code": (
            "def fibonacci(n):\n"
            "    if n <= 0: return []\n"
            "    result = [0, 1]\n"
            "    for i in range(2, n):\n"
            "        result.append(result[-1] + result[-2])\n"
            "    return result[:n]\n"
        ),
        "ask": "Review this code. Any bugs or edge cases missed?",
    })

    print("  Sending JSON code-review task...\n")
    async for event in client.send_message(message):
        print_event(event, "EVENT")


# -----------------------------------------------------------------------
# Demo 5: Get task by ID
# -----------------------------------------------------------------------
async def demo_get_task(factory: ClientFactory, card, task_id: str):
    print("\n" + "=" * 60)
    print("DEMO 5: Retrieve Task by ID")
    print("=" * 60)

    client = factory.create(card)
    task = await client.get_task(TaskQueryParams(id=task_id, history_length=3))

    print(f"  Task ID    : {task.id}")
    print(f"  State      : {task.status.state.value}")
    print(f"  Context ID : {task.context_id}")
    print(f"  Artifacts  : {len(task.artifacts or [])}")
    print(f"  History    : {len(task.history or [])} messages")


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
async def main():
    print("\n" + "=" * 60)
    print("  A2A ResearchAgent Client Demo")
    print("=" * 60)

    config = ClientConfig(streaming=True)

    async with httpx.AsyncClient(timeout=120.0) as http:
        # Build factory with an HTTP transport
        factory = ClientFactory(config=dataclasses.replace(config, httpx_client=http))

        # Demo 1: Discover
        card = await demo_discover(http)

        # Demo 2: Send message
        task_id, context_id = await demo_send_message(factory, card)

        # Demo 3: Follow-up in the same conversation
        if context_id:
            await demo_resume_conversation(factory, card, context_id)

        # Demo 4: Structured JSON
        await demo_json_message(factory, card)

        # Demo 5: Retrieve task
        if task_id:
            await demo_get_task(factory, card, task_id)

    print("\n" + "=" * 60)
    print("  All demos complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
