"""
demo_agent.py — Day 3: Build an agent, step by step

Three acts. Same chat interface. More tools added each time.

  ACT 1  LLM alone — answers from training data only
  ACT 2  + server.py via MCP — real weather, real files
  ACT 3  + Wikipedia — full agent, chains results across tools

Type 'next' to advance to the next act.
Type 'quit' to exit at any time.

Run:
    python demo_agent.py

Requires:
    - Ollama running: ollama serve
    - Model pulled:   ollama pull qwen3:8b
    - server.py in the same folder
"""

import sys
from pathlib import Path

from smolagents import MCPClient, LiteLLMModel, ToolCallingAgent, tool

# num_ctx=8192 is non-negotiable.
# Agent loops accumulate tokens fast. Without this, Ollama silently truncates
# the context and the agent loops forever or gives garbage.
model = LiteLLMModel(
    model_id="ollama/qwen3:8b",
    api_base="http://localhost:11434",
    num_ctx=8192,
)

SERVER = Path(__file__).parent / "server.py"


@tool
def wikipedia_summary(topic: str) -> str:
    """Get a short summary of any topic, person, place, or concept from Wikipedia.
    Use this when the user asks about facts, history, definitions, or general knowledge.

    Args:
        topic: The topic to look up, e.g. 'France', 'Tel Aviv', 'quantum computing'.
    """
    import json, urllib.parse, urllib.request
    query = urllib.parse.quote(topic)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("extract", "No summary found.")
    except Exception as e:
        return f"Error: {e}"


def chat_loop(agent, header):
    """Interactive chat. Returns True to advance, False to quit."""
    print(header)
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            return False
        if not q:
            continue
        if q.lower() == "next":
            return True
        if q.lower() == "quit":
            return False
        print()
        result = agent.run(q)
        print(f"\nAgent: {result}\n")


# ── Act 1: LLM alone ──────────────────────────────────────────────────────────

agent_bare = ToolCallingAgent(tools=[], model=model)

if not chat_loop(
    agent_bare,
    "\n" + "─" * 60 +
    "\n  ACT 1 — LLM alone (no tools)" +
    "\n  Ask anything. Type 'next' to add the MCP server." +
    "\n" + "─" * 60 + "\n",
):
    sys.exit(0)

# ── Acts 2 + 3 share one MCPClient process ────────────────────────────────────
# MCPClient launches server.py as a subprocess in STDIO mode.
# server.py detects it's not a tty and switches to STDIO automatically.

with MCPClient({"command": sys.executable, "args": [str(SERVER)]}) as mcp_tools:

    # ── Act 2: + MCP server ───────────────────────────────────────────────────

    agent_mcp = ToolCallingAgent(tools=[*mcp_tools], model=model)

    if not chat_loop(
        agent_mcp,
        "\n" + "─" * 60 +
        "\n  ACT 2 — MCP server added  (get_weather + read_file)" +
        "\n  Ask anything. Type 'next' to add Wikipedia." +
        "\n" + "─" * 60 + "\n",
    ):
        sys.exit(0)

    # ── Act 3: + Wikipedia ────────────────────────────────────────────────────

    agent_full = ToolCallingAgent(tools=[*mcp_tools, wikipedia_summary], model=model)

    chat_loop(
        agent_full,
        "\n" + "─" * 60 +
        "\n  ACT 3 — Wikipedia added  (full agent)" +
        "\n  Ask anything. Type 'quit' to exit." +
        "\n  Try: 'What is France known for, what's the weather in its capital," +
        "\n        and what does notes.txt say?'" +
        "\n" + "─" * 60 + "\n",
    )


# ─── To expand ────────────────────────────────────────────────────────────────
# Add another @tool above and include it in agent_full's tools list.
# To use your own Day 3 server instead:
#   MCPClient({"command": sys.executable, "args": ["your_server.py"]})
