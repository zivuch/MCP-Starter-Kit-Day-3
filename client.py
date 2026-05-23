"""
client.py — Day 2: Wire an LLM into the MCP loop

The full decision loop:
  1. Connect to the MCP server → discover tools
  2. Ask the LLM: here are the tools, what should we do?
  3. LLM returns a decision (not an execution)
  4. Client executes the tool via MCP
  5. Feed the result back to the LLM → final answer

Usage:
    python client.py
    python client.py "What is written in notes.txt?"
    python client.py "What is the weather in Paris?"

Requires:
    - Ollama running: ollama serve
    - Model pulled: ollama pull qwen3:8b
    - Day 1 server running: python server.py
"""

import asyncio
import json
import sys

# Force UTF-8 output so emoji from APIs (weather symbols etc.) don't crash on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel

console = Console()

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp/"
OLLAMA_BASE    = "http://localhost:11434/v1"
MODEL          = "qwen3:8b"

llm = OpenAI(base_url=OLLAMA_BASE, api_key="ollama")


def to_openai_tool(mcp_tool) -> dict:
    """Convert an MCP tool schema into the format OpenAI/Ollama expects."""
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description or "",
            "parameters": {
                "type": "object",
                "properties": mcp_tool.inputSchema.get("properties", {}),
                "required":   mcp_tool.inputSchema.get("required", []),
            },
        },
    }


async def run(prompt: str):
    console.print(f"\n[bold blue]Day 2 — LLM + MCP[/bold blue]  [dim]{MODEL}[/dim]\n")

    async with streamablehttp_client(MCP_SERVER_URL) as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()

            # ── Step 1: Discover tools ─────────────────────────────────────────
            tools_result = await session.list_tools()
            openai_tools = [to_openai_tool(t) for t in tools_result.tools]

            console.print(Panel(
                "\n".join(f"  [cyan]{t.name}[/cyan] — {t.description}" for t in tools_result.tools),
                title=f"[1/4] Discovered {len(openai_tools)} tool(s)"
            ))

            # ── Step 2: Ask the LLM what to do ────────────────────────────────
            messages = [
                {"role": "system", "content": "You are a helpful assistant. Use the available tools to answer."},
                {"role": "user",   "content": prompt},
            ]

            console.print(Panel(
                f'[bold]"{prompt}"[/bold]',
                title="[2/4] Asking LLM which tool to call"
            ))

            response = llm.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto",
            )

            assistant_msg = response.choices[0].message
            tool_calls    = assistant_msg.tool_calls or []

            if not tool_calls:
                console.print(Panel(
                    f"[yellow]LLM answered directly (no tool needed):[/yellow]\n\n{assistant_msg.content}",
                    title="[2/4] LLM decision"
                ))
                return

            for tc in tool_calls:
                args = json.loads(tc.function.arguments)
                console.print(Panel(
                    f"[bold]Tool chosen:[/bold] [cyan]{tc.function.name}[/cyan]\n"
                    f"[bold]Arguments:[/bold]   {args}\n\n"
                    f"[dim]The LLM chose — it did NOT execute. The client will execute.[/dim]",
                    title="[2/4] LLM decision",
                    border_style="yellow"
                ))

            # ── Step 3: Client executes each tool call ─────────────────────────
            tool_results = []
            for tc in tool_calls:
                args   = json.loads(tc.function.arguments)
                result = await session.call_tool(tc.function.name, arguments=args)
                text   = "\n".join(getattr(c, "text", str(c)) for c in result.content)
                tool_results.append({"id": tc.id, "name": tc.function.name, "content": text})

                console.print(Panel(
                    text,
                    title=f"[3/4] Tool result: {tc.function.name}({args})",
                    border_style="green"
                ))

            # ── Step 4: Feed results back → final answer ───────────────────────
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in tool_calls
                ],
            })
            for tr in tool_results:
                messages.append({"role": "tool", "tool_call_id": tr["id"], "content": tr["content"]})

            final = llm.chat.completions.create(model=MODEL, messages=messages)

            console.print(Panel(
                final.choices[0].message.content,
                title="[4/4] Final answer (with real data)",
                border_style="bright_green"
            ))


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is the current weather in Tel Aviv?"
    asyncio.run(run(prompt))
