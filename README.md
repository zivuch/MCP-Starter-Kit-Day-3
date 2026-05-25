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
| `ideas.md` | 10 server ideas with working code, all using free APIs |
| `demo_smolagents.py` | Instructor demo — smolagents running the same TAO loop automatically |
| `client.py` | Day 2 LLM loop client — use this to test your server |
| `notes.txt` | Sample file used by `demo_smolagents.py` |
| `student_tryit.md` | Exercise sheet |

## Build your server

1. Open `scaffold.py`
2. Rename the server (`"MyServer"` → something meaningful)
3. Delete the example tool, add 2–3 tools for your domain
4. Run it:

```bash
python scaffold.py
```

5. In a second terminal, test it with `client.py`:

```bash
python client.py "Ask it something that needs a tool"
```

**Stuck?** Open `ideas.md` — 10 fully-coded server ideas, no API keys needed.

## Run the smolagents demo

```bash
python demo_smolagents.py
```

Shows the same 4-step loop you built in Day 2, automated by a framework in 5 lines.

Requires Ollama + `qwen3:8b`.

## What's next

- Connect your server to [Goose](https://block.github.io/goose) — no `client.py`, just chat
- Browse more servers at [mcpservers.org](https://mcpservers.org)
- Go deeper: LlamaIndex (retrieval-first), LangGraph (stateful graphs), n8n (visual, low-code)
