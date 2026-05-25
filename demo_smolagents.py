"""
demo_smolagents.py — Day 3: Your first agent framework

Shows the same loop you built in Day 2 (discover → decide → execute → answer)
automated by smolagents. One TAO cycle used to take 50 lines of Python.
Now it's 5.

Requires:
    pip install smolagents[litellm] requests

Run:
    python demo_smolagents.py

Requires:
    - Ollama running: ollama serve
    - Model pulled: ollama pull qwen3:8b
"""

from smolagents import ToolCallingAgent, LiteLLMModel, tool

# num_ctx=8192 is non-negotiable.
# Ollama defaults to 2048 tokens. Agent loops run out of space silently
# and loop forever or produce garbage. Always set this.
model = LiteLLMModel(
    model_id="ollama/qwen3:8b",
    api_base="http://localhost:11434",
    num_ctx=8192,
)


@tool
def get_weather(city: str) -> str:
    """Get the current weather conditions and temperature for any city in the world.

    Args:
        city: The name of the city to get weather for, e.g. 'Tel Aviv' or 'Paris'.
    """
    import requests
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        r.raise_for_status()
        return r.text.strip()
    except Exception as e:
        return f"Weather unavailable: {e}"


@tool
def read_file(filename: str) -> str:
    """Read any text file from the Day 3 folder and return its full contents.

    Args:
        filename: The name of the file to read, e.g. 'notes.txt'.
    """
    from pathlib import Path
    path = Path(__file__).parent / filename
    if not path.exists():
        return f"File not found: {filename}"
    return path.read_text(encoding="utf-8")


agent = ToolCallingAgent(tools=[get_weather, read_file], model=model)

questions = [
    "What is the weather in Tel Aviv right now?",
    "What is written in notes.txt?",
    "What is the capital of France?",   # no tool needed — LLM answers directly
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print(f"{'='*60}")
    result = agent.run(q)
    print(f"A: {result}")
