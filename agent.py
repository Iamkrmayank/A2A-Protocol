"""
Agno Research Agent
===================
A smart research & analysis agent powered by Azure OpenAI (GPT-5),
built with the Agno framework. This agent:
  - Answers questions across any domain
  - Analyzes code snippets and suggests improvements
  - Summarizes information
  - Maintains conversation context across turns
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.azure import AzureOpenAI

load_dotenv()


def create_agent() -> Agent:
    """
    Create and return the Agno Research Agent.

    Agent Configuration Reference
    ------------------------------
    model                   - The LLM backend (AzureOpenAI here)
    name                    - Display name shown in logs / responses
    description             - One-sentence purpose shown in AgentCard
    instructions            - System prompt: list[str] or str.
                              Defines personality, rules, and behavior.
                              YES — you can absolutely define instructions!
    markdown                - Return responses in Markdown format
    add_datetime_to_context - Inject current date/time into system prompt
    add_name_to_context     - Inject agent name into system prompt
    debug_mode              - Print detailed logs to console
    stream                  - Stream tokens as they arrive
    """
    model = AzureOpenAI(
        id=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-chat"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
    )

    agent = Agent(
        model=model,
        name="ResearchAgent",
        description="A smart research and code analysis agent.",

        # ── Instructions (System Prompt) ─────────────────────────────────────
        # You CAN define instructions — they become part of the system message.
        # Accepts: str  OR  list[str] (each item = a bullet in the system prompt)
        instructions=[
            "You are an expert research and software engineering assistant.",
            "When answering questions, be precise, structured, and cite reasoning.",
            "When asked to review code: identify bugs, suggest improvements, "
            "explain complexity, and provide a corrected version if needed.",
            "When summarizing: extract the key points in bullet format.",
            "Always respond in clean Markdown.",
            "If you don't know something, say so — never hallucinate facts.",
        ],

        markdown=True,
        add_datetime_to_context=True,
        add_name_to_context=True,
        debug_mode=False,
    )

    return agent


# ── Quick standalone test ────────────────────────────────────────────────────
if __name__ == "__main__":
    agent = create_agent()
    print("=== ResearchAgent direct test ===\n")
    response = agent.run("What is the A2A protocol and why was it created?")
    print(response.content)
