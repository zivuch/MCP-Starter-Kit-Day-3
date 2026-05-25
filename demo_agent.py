"""
demo_agent.py — Day 3: Build an agent, step by step

Stage 1 (this file):  LLM only — no tools
Stage 2 (uncomment):  connect server.py → get_weather + read_file
Stage 3 (uncomment):  add Wikipedia @tool → full agent
Stage 4 (your task):  add a web search @tool

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
    structured_output=False,
)

# ── Stage 2: connect to server.py (must be running in Terminal 1) ─────────────
# import atexit
# from smolagents import MCPClient


# ── Stage 3: add Wikipedia ─────────────────────────────────────────────────────
# from smolagents import tool


# ── Stage 4 — your task: add a web search tool ────────────────────────────────
# Goal: write a @tool that searches the web, then add it to the tools list below.
#
# Option A — DuckDuckGo (no API key needed):
#   pip install ddgs
#
#   @tool
#
# Option B — Tavily (free API key at tavily.com):
#
#   @tool

# ── tools list — update as you add stages ─────────────────────────────────────
tools = []

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
