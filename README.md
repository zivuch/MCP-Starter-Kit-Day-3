# MCP Starter Kit — Day 3: Build Your Own

Build an MCP server for a domain you care about.

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
| `scaffold.py` | Your starting point — rename, delete the example tool, add your own |
| `server.py` | Exercise server with Day 1 tools — used for Tasks A/B/C in `student_tryit.md` |
| `client.py` | LLM loop from Day 2 — use this to test your server |
| `ideas.md` | 10 ready-to-build server ideas with working code |
| `notes.txt` | Sample file the server can read |
| `student_tryit.md` | Exercise sheet |

## Workflow

**Terminal 1 — run your server:**
```bash
python scaffold.py
```

**Terminal 2 — test it with the LLM:**
```bash
python client.py "your question here"
```

## Building your server

1. Open `scaffold.py`
2. Rename `MyServer` to something meaningful
3. Delete the example tool
4. Add 2–3 tools for your domain (see `ideas.md` for inspiration)
5. Write the docstring before the function body — it's what the LLM reads to decide when to call the tool
6. Restart the server after every change

## Tips

- Start with 1 tool. Get it working before adding the next.
- Use free APIs — no sign-ups, no keys. See `ideas.md` for options.
- If the LLM isn't calling your tool, improve the docstring.
