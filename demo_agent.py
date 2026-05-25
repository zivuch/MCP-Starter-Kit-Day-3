"""
demo_agent.py — Day 3: Build an agent, step by step

Stage 1 (this file):  LLM only — no tools
Stage 2 (add below):  connect server.py → get_weather + read_file
Stage 3 (add below):  add Wikipedia @tool → full agent

Run:
    Terminal 1:  python server.py
    Terminal 2:  python demo_agent.py

Requires:
    - Ollama running: ollama serve
    - Model pulled:   ollama pull qwen3:8b
"""

import sys
from smolagents import ToolCallingAgent, LiteLLMModel

# num_ctx=8192 is non-negotiable.
# Agent loops accumulate tokens fast. Without this, Ollama silently truncates
# the context and the agent loops forever or gives garbage.
model = LiteLLMModel(
    model_id="ollama/qwen3:8b",
    api_base="http://localhost:11434",
    num_ctx=8192,
)

# ── Stage 2: add server tools ──────────────────────────────────────────────────
# import atexit
# from smolagents import MCPClient
#
# _mcp = MCPClient({"url": "http://127.0.0.1:8000/mcp/"})
# server_tools = [*_mcp.__enter__()]
# atexit.register(lambda: _mcp.__exit__(None, None, None))

# ── Stage 3: add Wikipedia ─────────────────────────────────────────────────────
# from smolagents import tool
#
# @tool
# def wikipedia_summary(topic: str) -> str:
#     """Get a short summary of any topic from Wikipedia.
#     Use this for facts, history, definitions, or general knowledge.
#     Args:
#         topic: The topic to look up, e.g. 'France', 'Tel Aviv'.
#     """
#     import json, urllib.parse, urllib.request
#     query = urllib.parse.quote(topic)
#     url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
#     try:
#         with urllib.request.urlopen(url, timeout=5) as resp:
#             return json.loads(resp.read()).get("extract", "No summary found.")
#     except Exception as e:
#         return f"Error: {e}"

# ── tools list — update as you add stages ─────────────────────────────────────
tools = []
# Stage 2: tools = server_tools
# Stage 3: tools = [*server_tools, wikipedia_summary]

agent = ToolCallingAgent(tools=tools, model=model)

print("\n── Agent chat ── (Ctrl+C to stop)\n")
while True:
    try:
        q = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    if not q:
        continue
    print()
    print(f"Agent: {agent.run(q)}\n")
