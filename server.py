"""
server.py — Day 1: Your first MCP server

Three MCP primitives, all in one file:
  - Tools (LLM calls these):  read_file, get_weather
  - Resource (host reads this at startup):  notes://today
  - Prompt (user triggers by name):  summarize

Run it:
    python server.py

When you run it from a terminal → HTTP mode at http://127.0.0.1:8000/mcp/
When Goose / Claude Desktop spawns it   → STDIO mode, automatically
"""

import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Workshop")


# ── Tools (the LLM decides when to call these) ─────────────────────────────
@mcp.tool()
def read_file(filename: str) -> str:
    """Read any text file from the current directory and return its full contents."""
    path = Path(__file__).parent / filename
    if not path.exists():
        return f"File not found: {filename}"
    return path.read_text(encoding="utf-8")


@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather conditions and temperature for any city in the world."""
    import requests
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        r.raise_for_status()
        return r.text.strip()          # e.g. "Tel Aviv: ⛅️  +28°C"
    except Exception as e:
        return f"Weather unavailable: {e}"


# ── Resource (the host application reads this, not the LLM) ────────────────

@mcp.resource("notes://today")
def today_notes() -> str:
    """Workshop notes for today. A host app like Goose reads this on startup
    to give the LLM background context without the user having to ask."""
    path = Path(__file__).parent / "notes.txt"
    if not path.exists():
        return "No notes found."
    return path.read_text(encoding="utf-8")


# ── Prompt (the user triggers this workflow by name) ───────────────────────

@mcp.prompt(name="summarize")
def summarize_prompt(filename: str) -> str:
    """Prompt template: instructs the LLM to read a file and summarize it.
    The user triggers this by selecting 'summarize' in a client like Goose."""
    return (
        f"Please read the file '{filename}' using the read_file tool, "
        f"then write a brief, clear summary of its contents."
    )


if __name__ == "__main__":
    if sys.stdin.isatty():
        print("Server starting → http://127.0.0.1:8000/mcp/", file=sys.stderr)
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
