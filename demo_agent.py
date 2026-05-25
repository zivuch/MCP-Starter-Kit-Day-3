"""
demo_agent.py — Day 3: Build an agent, step by step

Run:  python demo_agent.py
Ctrl+C to stop.

Requires:
    - Ollama running: ollama serve
    - Model pulled:   ollama pull qwen3:8b
"""

import sys
from smolagents import ToolCallingAgent, LiteLLMModel

# num_ctx=8192 is non-negotiable.
# Ollama defaults to 2048 tokens. Agent loops run out of space silently
# and loop forever or produce garbage. Always set this.
model = LiteLLMModel(
    model_id="ollama/qwen3:8b",
    api_base="http://localhost:11434",
    num_ctx=8192,
)

agent = ToolCallingAgent(tools=[], model=model)

print("\n── ACT 1: LLM alone ── (Ctrl+C to stop)\n")
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
