# Student Exercise — Day 3

**Time:** ~30 minutes (after class or during the build session)  
**Goal:** Give your agent multiple sources of information and watch it choose the right one.

---

## Setup

Make sure your Day 1 server is running:
```
python "../Day1-Build-a-Server/server.py"
```

---

## Task A — Add a Wikipedia Tool (10 min)

Open `server.py` from Day 1. Add this tool:

```python
@mcp.tool()
def wikipedia_summary(topic: str) -> str:
    """Get a short Wikipedia summary of any topic, person, place, or concept.
    Use this when the user asks about facts, history, definitions, or general knowledge."""
    import urllib.request, urllib.parse, json
    query = urllib.parse.quote(topic)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("extract", "No summary found.")
    except Exception as e:
        return f"Error: {e}"
```

Restart the server. Run `client.py` with any question. Confirm `wikipedia_summary` now appears in the "Discovered tools" panel.

---

## Task B — Test Source Selection (10 min)

Ask these three questions via `client.py` and record which tool the LLM chose:

```
python client.py "What is the capital of Japan?"
python client.py "What's the weather in Tokyo today?"
python client.py "What's written in notes.txt?"
```

| Question | Tool you expected | Tool actually called |
|----------|-----------------|---------------------|
| Capital of Japan | wikipedia_summary | |
| Weather in Tokyo | get_weather | |
| Contents of notes.txt | read_file | |

**If it picked the wrong tool:** Read the docstrings of the tools it confused. Which words caused the confusion? Edit the docstring of the misfiring tool to be more specific about *when* to use it, then retry.

---

## Task C — Two Sources, One Answer (10 min)

Ask this question:

```
python client.py "What year was Python created, and what's the weather in its birthplace?"
```

- Which tools did it call?
- Did it combine both answers into one response?
- Could you tell which part of the answer came from which source?

**This is what "grounded answers with citations" means in LlamaIndex.** You just built the underlying pattern manually — source selection + synthesis. LlamaIndex automates and formalizes it; the concept is the same.

---

## Reflection Questions

1. You now have 3 tools: `get_weather`, `read_file`, `wikipedia_summary`. The LLM picks among them using only the docstrings. What would happen if all three docstrings said "gets information"?

2. Your server also exposes a resource (`notes://today`). The LLM never calls it — the host app reads it automatically. When would a resource be better than a tool for the same data?

3. The TAO loop (Thought → Action → Observation) runs once per tool call. For the "Python birthplace + weather" question, how many TAO cycles did the client run?

---

## Bonus: Build Your Own Multi-Tool Server

Design a server for a real use case you care about. It should have:
- At least 2 tools that serve different purposes (so the LLM must choose)
- 1 resource that gives the LLM background context at startup
- Tool docstrings that clearly say *when* to use each one (not just what it does)

Start from `scaffold.py`. Ideas in `ideas.md`.

---

## Bonus: Connect Goose to Your Server

You built your own server today. Connect Goose to it — no `client.py`, no code, just chat.

**Install:** download from `block.github.io/goose`

**Step 1 — Set the model to qwen3:8b**

Goose's default model is too small for tool calling. Connect it to your local Ollama:
1. Open Goose → click **Connect to a Provider**
2. Find **Ollama** → click **Configure**
3. **Ollama Host:** `localhost` — leave as-is → click **Submit**
4. Select model: `qwen3:8b`

**Step 2 — Add the MCP extension**

**Config** — edit `C:\Users\<your-name>\.config\goose\config.yaml`:
```yaml
extensions:
  my_server:
    enabled: true
    name: my_server
    type: stdio
    cmd: python
    args:
      - "C:\\full\\path\\to\\your_server.py"
    envs: {}
```
Replace the path with the actual path to the server you built today.

**Or via Goose UI:** Settings → Extensions → Add custom extension:
- Extension Name: `MyServer` *(or whatever you named it)*
- Type: `STDIO`
- Command: `python C:\full\path\to\your_server.py` *(python and path in one field)*

**Test it:** Ask Goose questions that need your tools. Watch it decide which one to call.

**Day 3 observation:** Three days ago you had no server. Today you have a running MCP server for a domain you chose, and it works with any MCP client — Goose, Claude Desktop, your own `client.py` — without changing a line of server code. That's the protocol.
