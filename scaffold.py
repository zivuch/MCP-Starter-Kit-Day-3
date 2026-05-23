"""
scaffold.py — Day 3: Build your own MCP server

Use this as a starting point. Replace the example tool with tools for your own use case.

Steps:
  1. Rename the server below ("MyServer" → something meaningful)
  2. Delete the example tool
  3. Add 2-3 tools for your domain
  4. Run it: python scaffold.py
  5. Connect client.py from Day 2 and ask it questions

Tips:
  - Each tool does ONE thing
  - Write the docstring first — it's what the LLM reads to decide when to call it
  - Return a string (or something that serializes to a string)
  - Keep it simple: you can always add more later
"""

import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")   # TODO: rename this


# ─── Example tool — replace this with your own ────────────────────────────────

@mcp.tool()
def example_tool(input: str) -> str:
    """Example tool. Replace with something useful for your domain."""
    return f"You gave me: {input}"


# ─── Add your tools below ─────────────────────────────────────────────────────

# @mcp.tool()
# def your_tool_name(param: str) -> str:
#     """Describe what this tool does and when the LLM should call it."""
#     # your code here
#     return "result"


# ─── Server entry point (leave this as-is) ────────────────────────────────────

if __name__ == "__main__":
    if sys.stdin.isatty():
        print(f"Server starting → http://127.0.0.1:8000/mcp/", file=sys.stderr)
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
