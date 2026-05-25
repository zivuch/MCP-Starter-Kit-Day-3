# MCP Starter Kit — Day 3: Build Your Own

Build an MCP server for a domain you care about, then connect it to an LLM.

---

## Prerequisites

- Python 3.10 or later
- Ollama running with `qwen3:8b` pulled:
  ```bash
  ollama serve          # separate terminal
  ollama pull qwen3:8b
  ```

## Setup

```bash
pip install -r requirements.txt
```

## Files

| File | What it is |
|------|------------|
| `scaffold.py` | **Starting point** — rename, delete the example tool, add your own |
| `server.py` | Day 1 server with `get_weather` and `read_file` — used for Tasks A/B/C in `student_tryit.md` |
| `client.py` | Day 2 LLM loop client — use this to test your server |
| `demo_agent.py` | Instructor demo — progressive agent: LLM only → MCP tools → Wikipedia → web search |
| `ideas.md` | 10 server ideas with working code, all using free APIs |
| `notes.txt` | Sample file the server can read |
| `student_tryit.md` | Exercise sheet |

## Build your server

**Terminal 1 — run your server:**
```bash
python scaffold.py
```

**Terminal 2 — test it with the LLM:**
```bash
python client.py "Ask it something that needs a tool"
```

1. Open `scaffold.py`
2. Rename `MyServer` to something meaningful
3. Delete the example tool
4. Add 2–3 tools for your domain (see `ideas.md` for inspiration)
5. Write the docstring before the function body — it's what the LLM reads to decide when to call the tool
6. Restart the server after every change

**Stuck?** Open `ideas.md` — 10 fully-coded server ideas, no API keys needed.

## Tips

- Start with 1 tool. Get it working before adding the next.
- Use free APIs — no sign-ups, no keys. See `ideas.md` for options.
- If the LLM isn't calling your tool, improve the docstring.

## Run the agent demo

```bash
# Terminal 1 — MCP server (needed for Stage 2+):
python server.py

# Terminal 2 — agent chat:
python demo_agent.py
```

Starts as LLM-only chat. Add code stage by stage to connect MCP tools, Wikipedia, and web search. Requires Ollama + `qwen3:8b`.

## What's next

- Connect your server to [Goose](https://block.github.io/goose) — no `client.py`, just chat
- Browse more servers at [mcpservers.org](https://mcpservers.org)
- Go deeper: LlamaIndex (retrieval-first), LangGraph (stateful graphs), n8n (visual, low-code)
