"""
server.py — Day 3 exercise server

This is the Day 1 server with two tools already in place.
Task A: add wikipedia_summary below, then restart.
"""

import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Workshop")


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
        return r.text.strip()
    except Exception as e:
        return f"Weather unavailable: {e}"


# ── Task A: add wikipedia_summary here ────────────────────────────────────────


@mcp.resource("notes://today")
def today_notes() -> str:
    """Workshop notes for today."""
    path = Path(__file__).parent / "notes.txt"
    if not path.exists():
        return "No notes found."
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    if sys.stdin.isatty():
        print("Server starting → http://127.0.0.1:8000/mcp/", file=sys.stderr)
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
