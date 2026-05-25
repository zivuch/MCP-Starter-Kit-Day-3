"""
demo_smolagents_live.py — Day 3: Live agent demo with real data

Two tools, one agent, one question that forces the LLM to use both.
Wikipedia (free) + live exchange rates (free) — no API keys needed.

Run:
    python demo_smolagents_live.py

Requires:
    - Ollama running: ollama serve
    - Model pulled:   ollama pull qwen3:8b
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
def wikipedia_summary(topic: str) -> str:
    """Get a short summary of any topic, person, place, or concept from Wikipedia.
    Use this when the user asks about facts, history, definitions, or general knowledge.

    Args:
        topic: The topic to look up, e.g. 'France', 'Tel Aviv', 'quantum computing'.
    """
    import urllib.request, urllib.parse, json
    query = urllib.parse.quote(topic)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("extract", "No summary found.")
    except Exception as e:
        return f"Error: {e}"


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another using live exchange rates.
    Use this when the user asks about currency conversion or current exchange rates.

    Args:
        amount: The numeric amount to convert, e.g. 1000.0.
        from_currency: The ISO 4217 source currency code, e.g. 'EUR', 'USD', 'ILS'.
        to_currency: The ISO 4217 target currency code, e.g. 'ILS', 'USD', 'EUR'.
    """
    import urllib.request, json
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            rate = data["rates"].get(to_currency.upper())
            if rate is None:
                return f"Currency not found: {to_currency}"
            result = amount * rate
            return f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}"
    except Exception as e:
        return f"Error: {e}"


agent = ToolCallingAgent(tools=[wikipedia_summary, convert_currency], model=model)

questions = [
    "What is France known for economically?",                              # wikipedia only
    "How much is 500 USD in ILS right now?",                               # currency only
    "What is the GDP of France, and how much is 1000 EUR in ILS right now?",  # both tools
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print(f"{'='*60}")
    result = agent.run(q)
    print(f"A: {result}")
