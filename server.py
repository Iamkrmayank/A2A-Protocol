"""
A2A Server — Wrapping an Agno Agent
=====================================
This file exposes the ResearchAgent as a standards-compliant
A2A server using the Google A2A SDK (a2a-sdk 0.3.x).

Architecture
────────────
  Client HTTP request
       │
       ▼
  FastAPI  (A2AFastAPIApplication)
       │
       ▼
  DefaultRequestHandler
       │  manages TaskStore, EventQueue, push notifications
       ▼
  AgnoAgentExecutor   ← your custom logic lives here
       │
       ▼
  Agno Agent (ResearchAgent)

What the server accepts from a client
──────────────────────────────────────
• message.parts        - TextPart, FilePart (URL), DataPart (JSON)
• message.context_id   - groups tasks in a session/conversation
• message.task_id      - attaches message to an existing task
• configuration.blocking          - wait until task completes
• configuration.history_length    - how many prior messages to return
• configuration.accepted_output_modes - MIME types client can handle
• configuration.push_notification_config - webhook URL for async updates
• metadata             - arbitrary key→value pairs passed through

What the server sends back
──────────────────────────
• Task object (with id, context_id, status, history, artifacts)
• Message object (for quick synchronous replies)
• TaskStatusUpdateEvent (streaming: state changes)
• TaskArtifactUpdateEvent (streaming: new artifacts)

Run
───
    python server.py
    # or
    uvicorn server:app --host 0.0.0.0 --port 8000 --reload
"""

import asyncio
import os
import logging
import uuid

import uvicorn
from dotenv import load_dotenv

from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.events import EventQueue
from a2a.types import (
    AgentCard,
    AgentSkill,
    AgentCapabilities,
    AgentProvider,
    Task,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    Artifact,
    Message,
    Role,
    Part,
    TextPart,
    DataPart,
)

# Agno streaming event types
from agno.run.agent import RunContentEvent, RunCompletedEvent, RunErrorEvent

from agent import create_agent

load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# ── 1. AgentCard — "business card" of your agent ─────────────────────────────
#    Clients fetch this from GET /.well-known/agent-card.json
#    It tells them: what can this agent do? what does it accept/return?
#    how do I authenticate? does it stream?
AGENT_CARD = AgentCard(
    name="ResearchAgent",
    description=(
        "A smart research and code analysis agent powered by Azure OpenAI GPT-5. "
        "Ask questions, review code, get summaries, or explore any topic."
    ),
    url="http://localhost:8000/",          # base URL of this server
    version="1.0.0",
    provider=AgentProvider(
        organization="A2A Demo",
        url="http://localhost:8000",
    ),

    # ── What can this server do? ──────────────────────────────────────────────
    capabilities=AgentCapabilities(
        streaming=True,              # supports message/stream SSE
        push_notifications=False,    # no webhook delivery (keep it simple)
        state_transition_history=True,
    ),

    # ── Default media types ───────────────────────────────────────────────────
    default_input_modes=["text/plain", "text/markdown", "application/json"],
    default_output_modes=["text/markdown", "text/plain"],

    # ── Skills — logical capabilities exposed to clients ─────────────────────
    skills=[
        AgentSkill(
            id="research",
            name="Research & Q&A",
            description="Answer questions on any topic with citations and reasoning.",
            input_modes=["text/plain", "text/markdown"],
            output_modes=["text/markdown"],
            tags=["research", "qa", "general"],
            examples=[
                "What is the A2A protocol?",
                "Explain transformer architecture.",
                "What happened at the 2025 AI summit?",
            ],
        ),
        AgentSkill(
            id="code_review",
            name="Code Review",
            description="Review code snippets: find bugs, suggest improvements, explain complexity.",
            input_modes=["text/plain", "application/json"],
            output_modes=["text/markdown"],
            tags=["code", "review", "engineering"],
            examples=[
                "Review this Python function for bugs.",
                "How can I optimize this SQL query?",
            ],
        ),
        AgentSkill(
            id="summarize",
            name="Summarization",
            description="Summarize long texts into structured bullet-point summaries.",
            input_modes=["text/plain", "text/markdown"],
            output_modes=["text/markdown"],
            tags=["summarize", "nlp"],
        ),
    ],
)


# ── 2. AgentExecutor — the bridge between A2A and your Agno agent ─────────────
class AgnoAgentExecutor(AgentExecutor):
    """
    Implements the A2A AgentExecutor interface.

    The SDK calls `execute(context, event_queue)` for every incoming message.
    You enqueue events onto event_queue to send them back to the client:
      - TaskStatusUpdateEvent  → state change (working → completed)
      - TaskArtifactUpdateEvent → a result artifact
      - Message                → a direct reply (for non-task flows)

    context contains:
      - context.message        → the incoming Message object
      - context.task_id        → assigned task ID
      - context.context_id     → conversation/session ID
      - context.configuration  → MessageSendConfiguration
      - context.metadata       → arbitrary key→value from client
      - context.current_task   → existing Task if resuming
    """

    def __init__(self):
        self._agent = create_agent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_text = self._extract_text(context.message)
        log.info(f"[Task {context.task_id}] Input: {user_text[:80]}...")

        loop = asyncio.get_running_loop()

        # ── Helper: build a TaskStatus Message ───────────────────────────────
        def status_msg(text: str) -> Message:
            return Message(
                role=Role.agent,
                parts=[Part(root=TextPart(text=text))],
                message_id=str(uuid.uuid4()),
            )

        # ── Signal: working ───────────────────────────────────────────────────
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(
                    state=TaskState.working,
                    message=status_msg("Generating response..."),
                ),
                final=False,
            )
        )

        # ── Async bridge: Agno sync generator → async A2A event queue ─────────
        # asyncio.Queue is the thread-safe bridge.
        # The worker thread pushes tuples:
        #   ("chunk", str)   — a token/chunk of text
        #   ("done",  None)  — generation complete
        #   ("error", str)   — exception message
        chunk_queue: asyncio.Queue = asyncio.Queue()

        def _run_agent_streaming():
            """Runs in a thread-pool thread. Streams Agno output into chunk_queue."""
            try:
                for agno_event in self._agent.run(
                    user_text,
                    stream=True,        # enable streaming from the model
                    stream_events=True, # yield granular RunOutputEvent objects
                ):
                    # RunContentEvent carries a text chunk (token or small batch)
                    if isinstance(agno_event, RunContentEvent):
                        chunk = agno_event.content
                        if chunk:
                            loop.call_soon_threadsafe(
                                chunk_queue.put_nowait, ("chunk", chunk)
                            )
                    # RunErrorEvent — surface the error
                    elif isinstance(agno_event, RunErrorEvent):
                        loop.call_soon_threadsafe(
                            chunk_queue.put_nowait, ("error", str(agno_event))
                        )
                        return

                # Generator exhausted → signal done
                loop.call_soon_threadsafe(chunk_queue.put_nowait, ("done", None))

            except Exception as exc:
                loop.call_soon_threadsafe(
                    chunk_queue.put_nowait, ("error", str(exc))
                )

        # Start the blocking Agno call in the thread pool (non-blocking for event loop)
        agent_future = loop.run_in_executor(None, _run_agent_streaming)

        artifact_id = "result"
        total_chars = 0

        try:
            # ── Drain the queue: emit one A2A artifact event per chunk ────────
            while True:
                kind, payload = await chunk_queue.get()

                if kind == "chunk":
                    total_chars += len(payload)
                    await event_queue.enqueue_event(
                        TaskArtifactUpdateEvent(
                            task_id=context.task_id,
                            context_id=context.context_id,
                            artifact=Artifact(
                                artifact_id=artifact_id,
                                name="Agent Response",
                                # Each event carries only the NEW chunk.
                                # The A2A SDK accumulates them on the client side.
                                parts=[Part(root=TextPart(text=payload))],
                            ),
                            last_chunk=False,  # more chunks coming
                        )
                    )

                elif kind == "done":
                    log.info(f"[Task {context.task_id}] Stream done ({total_chars} chars)")
                    # Final sentinel — signals end of artifact stream
                    await event_queue.enqueue_event(
                        TaskArtifactUpdateEvent(
                            task_id=context.task_id,
                            context_id=context.context_id,
                            artifact=Artifact(
                                artifact_id=artifact_id,
                                name="Agent Response",
                                parts=[Part(root=TextPart(text=""))],
                            ),
                            last_chunk=True,
                        )
                    )
                    break

                elif kind == "error":
                    raise RuntimeError(payload)

            await agent_future  # propagate any thread exceptions

            # ── Signal: completed ─────────────────────────────────────────────
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=context.task_id,
                    context_id=context.context_id,
                    status=TaskStatus(
                        state=TaskState.completed,
                        message=status_msg("Done."),
                    ),
                    final=True,
                )
            )

        except Exception as exc:
            log.exception(f"[Task {context.task_id}] Error: {exc}")
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=context.task_id,
                    context_id=context.context_id,
                    status=TaskStatus(
                        state=TaskState.failed,
                        message=status_msg(f"Error: {exc}"),
                    ),
                    final=True,
                )
            )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle task cancellation request from client."""
        log.info(f"[Task {context.task_id}] Cancellation requested.")
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(
                    state=TaskState.canceled,
                    message=Message(
                        role=Role.agent,
                        parts=[Part(root=TextPart(text="Task was canceled by client request."))],
                        message_id=str(uuid.uuid4()),
                    ),
                ),
                final=True,
            )
        )

    # ── Helper: extract plain text from any Part type ─────────────────────────
    @staticmethod
    def _extract_text(message: Message) -> str:
        texts = []
        for part in message.parts:
            root = part.root
            if isinstance(root, TextPart):
                texts.append(root.text)
            elif isinstance(root, DataPart):
                # structured JSON → convert to string
                texts.append(str(root.data))
        return "\n".join(texts) if texts else "(no text provided)"


# ── 3. Wire everything together ───────────────────────────────────────────────
def build_app():
    handler = DefaultRequestHandler(
        agent_executor=AgnoAgentExecutor(),
        task_store=InMemoryTaskStore(),   # in-memory; swap for Redis/DB in prod
    )

    return A2AFastAPIApplication(
        agent_card=AGENT_CARD,
        http_handler=handler,
    ).build()


app = build_app()


# ── 4. Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  A2A ResearchAgent Server")
    print("=" * 60)
    print(f"  Agent Card :  http://localhost:8000/.well-known/agent-card.json")
    print(f"  JSON-RPC   :  POST http://localhost:8000/")
    print(f"  Streaming  :  POST http://localhost:8000/ (SSE)")
    print("=" * 60 + "\n")

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
