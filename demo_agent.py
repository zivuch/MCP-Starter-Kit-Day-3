"""
demo_agent.py — Day 3: An interactive agent

Two tool sources, one agent:
  - server.py (Day 1) — connected via MCP. Provides get_weather + read_file.
  - wikipedia_summary  — a new @tool added directly. No server needed.

The agent decides which tool to call, chains results across steps, and keeps
going until it has a complete answer. The context grows with each step — watch
the token counts in the output.

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
# the context and the agent loops forever or produces garbage.
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


# MCPClient launches server.py as a subprocess in STDIO mode.
# server.py detects it's not a tty and switches to STDIO automatically.
# One terminal. No port conflicts.
with MCPClient({"command": sys.executable, "args": [str(SERVER)]}) as mcp_tools:
    agent = ToolCallingAgent(
        tools=[*mcp_tools, wikipedia_summary],
        model=model,
    )

    print("\nAgent ready.")
    print(f"MCP tools loaded from server.py + wikipedia_summary")
    print("Type 'quit' to exit.\n")

    while True:
        q = input("You: ").strip()
        if not q or q.lower() in ("quit", "exit"):
            break
        print()
        result = agent.run(q)
        print(f"\nAgent: {result}\n")


# ─── To expand this agent ─────────────────────────────────────────────────────
#
# Add more @tool functions above and include them in the tools list.
#
# To use your own Day 3 server instead of server.py:
#   with MCPClient({"command": sys.executable, "args": ["your_server.py"]}) as mcp_tools:
#
# To connect to a running HTTP server:
#   with MCPClient({"url": "http://127.0.0.1:8000/mcp/"}) as mcp_tools:
