# Server Ideas — Day 3

Ten domains. Each one has enough to get started in 60 minutes.

---

## 1. Personal Notes Server

Tools: `list_notes`, `read_note`, `search_notes`  
Use case: "Find all my notes about product launches" — LLM searches your local files.

```python
from pathlib import Path

NOTES_DIR = Path.home() / "notes"

@mcp.tool()
def list_notes() -> str:
    """List all available note files."""
    files = list(NOTES_DIR.glob("*.md")) + list(NOTES_DIR.glob("*.txt"))
    return "\n".join(f.name for f in files) if files else "No notes found."

@mcp.tool()
def read_note(filename: str) -> str:
    """Read the contents of a specific note file."""
    path = NOTES_DIR / filename
    if not path.exists():
        return f"Note not found: {filename}"
    return path.read_text(encoding="utf-8")

@mcp.tool()
def search_notes(keyword: str) -> str:
    """Search all notes for a keyword and return matching lines."""
    results = []
    for f in NOTES_DIR.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if keyword.lower() in line.lower():
                results.append(f"{f.name}: {line.strip()}")
    return "\n".join(results) if results else f"No matches for '{keyword}'."
```

---

## 2. Currency & Finance Server

Tools: `get_exchange_rate`, `convert_currency`  
Use case: "How much is 500 EUR in ILS?" — LLM fetches live rates.

```python
@mcp.tool()
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Get the current exchange rate between two currencies. Use ISO codes like USD, EUR, ILS."""
    import urllib.request, json
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            rate = data["rates"].get(to_currency.upper())
            if rate is None:
                return f"Currency not found: {to_currency}"
            return f"1 {from_currency.upper()} = {rate} {to_currency.upper()}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another using live exchange rates."""
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
```

---

## 3. Wikipedia Research Server

Tools: `search_wikipedia`, `get_article_summary`, `get_article_section`  
Use case: "Give me a brief overview of quantum computing" — LLM fetches real articles.

```python
import urllib.request, urllib.parse, json

@mcp.tool()
def search_wikipedia(query: str) -> str:
    """Search Wikipedia and return the top 5 matching article titles."""
    q = urllib.parse.quote(query)
    url = f"https://en.wikipedia.org/w/api.php?action=search&list=search&srsearch={q}&format=json&srlimit=5"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            results = data["query"]["search"]
            return "\n".join(f"{r['title']}: {r['snippet']}" for r in results)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def get_article_summary(title: str) -> str:
    """Get a plain-text summary of a Wikipedia article by its exact title."""
    q = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("extract", "No summary available.")
    except Exception as e:
        return f"Error: {e}"
```

---

## 4. Local CSV / Data Server

Tools: `list_datasets`, `describe_dataset`, `query_csv`  
Use case: "What is the average sale in the Q1 data?" — LLM queries your CSV files.

```python
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

@mcp.tool()
def list_datasets() -> str:
    """List all CSV files available for analysis."""
    files = list(DATA_DIR.glob("*.csv"))
    return "\n".join(f.name for f in files) if files else "No CSV files found."

@mcp.tool()
def describe_dataset(filename: str) -> str:
    """Show the column headers and first 3 rows of a CSV file."""
    path = DATA_DIR / filename
    if not path.exists():
        return f"File not found: {filename}"
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)[:4]
    return "\n".join(",".join(row) for row in rows)
```

---

## 5. System Information Server

Tools: `get_disk_usage`, `list_processes`, `get_system_info`  
Use case: "Is my disk getting full?" — LLM checks your machine's state.

```python
import shutil, platform, os

@mcp.tool()
def get_disk_usage() -> str:
    """Get the disk usage for the main drive (total, used, free space)."""
    total, used, free = shutil.disk_usage("/")
    return (
        f"Total: {total // (1024**3)} GB\n"
        f"Used:  {used  // (1024**3)} GB\n"
        f"Free:  {free  // (1024**3)} GB"
    )

@mcp.tool()
def get_system_info() -> str:
    """Return basic system information: OS, Python version, machine name."""
    import sys
    return (
        f"OS: {platform.system()} {platform.release()}\n"
        f"Machine: {platform.node()}\n"
        f"Python: {sys.version.split()[0]}"
    )
```

---

## 6. Todo List Server

Tools: `add_todo`, `list_todos`, `complete_todo`  
Use case: "Add 'Buy milk' to my list" — LLM manages a local task list.

```python
import json
from pathlib import Path

TODOS_FILE = Path(__file__).parent / "todos.json"

def _load():
    if not TODOS_FILE.exists():
        return []
    return json.loads(TODOS_FILE.read_text())

def _save(todos):
    TODOS_FILE.write_text(json.dumps(todos, indent=2))

@mcp.tool()
def add_todo(task: str) -> str:
    """Add a new task to the todo list."""
    todos = _load()
    todos.append({"task": task, "done": False})
    _save(todos)
    return f"Added: {task}"

@mcp.tool()
def list_todos() -> str:
    """List all current todo items, showing which are complete and which are pending."""
    todos = _load()
    if not todos:
        return "No todos yet."
    lines = []
    for i, t in enumerate(todos):
        status = "✓" if t["done"] else "○"
        lines.append(f"{i+1}. {status} {t['task']}")
    return "\n".join(lines)

@mcp.tool()
def complete_todo(task_number: int) -> str:
    """Mark a todo item as complete by its number (1-based index)."""
    todos = _load()
    if task_number < 1 or task_number > len(todos):
        return f"No task {task_number}."
    todos[task_number - 1]["done"] = True
    _save(todos)
    return f"Completed: {todos[task_number-1]['task']}"
```

---

## 7. Recipe Server

Tools: `search_recipes`, `get_recipe_details`  
Use case: "What can I cook with chicken and tomatoes?" — LLM queries a recipe database.

Starter: use a JSON file of recipes (create your own, or use a free API like TheMealDB).

```python
import urllib.request, urllib.parse, json

@mcp.tool()
def search_recipes(ingredient: str) -> str:
    """Search for recipes that include a specific ingredient."""
    q = urllib.parse.quote(ingredient)
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={q}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            meals = data.get("meals") or []
            if not meals:
                return f"No recipes found with {ingredient}."
            return "\n".join(f"{m['strMeal']} (id: {m['idMeal']})" for m in meals[:10])
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def get_recipe_details(meal_id: str) -> str:
    """Get the full details and ingredients for a recipe by its ID."""
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            meal = (data.get("meals") or [None])[0]
            if not meal:
                return "Recipe not found."
            ingredients = [
                f"{meal[f'strIngredient{i}']} — {meal[f'strMeasure{i}']}"
                for i in range(1, 21)
                if meal.get(f"strIngredient{i}")
            ]
            return f"{meal['strMeal']}\n\nIngredients:\n" + "\n".join(ingredients)
    except Exception as e:
        return f"Error: {e}"
```

---

## 8. Job Listings Server

Tools: `search_jobs`  
Use case: "Show me Python developer jobs" — LLM queries a jobs API.

*(Uses RemoteOK free API — no key needed.)*

```python
@mcp.tool()
def search_jobs(technology: str) -> str:
    """Search for remote job listings by technology or skill (e.g. 'python', 'react', 'devops')."""
    import urllib.request, urllib.parse, json
    url = f"https://remoteok.com/api?tag={urllib.parse.quote(technology)}"
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            jobs = json.loads(resp.read())
            jobs = [j for j in jobs if isinstance(j, dict) and "position" in j][:5]
            if not jobs:
                return f"No jobs found for {technology}."
            return "\n\n".join(f"{j['position']} at {j['company']}\n{j.get('url','')}" for j in jobs)
    except Exception as e:
        return f"Error: {e}"
```

---

## 9. Git Repository Server

Tools: `list_recent_commits`, `get_file_diff`, `list_changed_files`  
Use case: "What changed in the last 3 commits?" — LLM summarizes git history.

```python
import subprocess

@mcp.tool()
def list_recent_commits(count: int = 5) -> str:
    """List the most recent git commits with their messages and authors."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{count}", "--oneline", "--format=%h %an: %s"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or "No commits found."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def list_changed_files(commit_hash: str = "HEAD") -> str:
    """List files changed in a specific commit."""
    try:
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", commit_hash],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or "No files changed."
    except Exception as e:
        return f"Error: {e}"
```

---

## 10. Language Learning Server

Tools: `translate`  
Use case: "Translate 'hello' to Spanish" — LLM calls a free translation API.

```python
@mcp.tool()
def translate(text: str, language_code: str) -> str:
    """Translate English text into another language. Use ISO 639-1 language codes:
    es=Spanish, fr=French, de=German, he=Hebrew, ar=Arabic, it=Italian, pt=Portuguese, zh=Chinese."""
    import urllib.request, urllib.parse, json
    # Uses MyMemory free translation API (no key needed, ~1000 words/day limit)
    q = urllib.parse.quote(text)
    url = f"https://api.mymemory.translated.net/get?q={q}&langpair=en|{language_code}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            return data["responseData"]["translatedText"]
    except Exception as e:
        return f"Translation error: {e}"
```

---

## Tips for Picking Your Idea

1. **Pick something you'd actually use.** If you care about the result, you'll debug it harder.
2. **Start with 2 tools.** You can add more once the first two work.
3. **Use free APIs.** wttr.in, Open-Meteo, Wikipedia, TheMealDB, RemoteOK — no sign-ups.
4. **Avoid APIs that need keys.** You'll spend the whole time on auth instead of MCP.
5. **Return strings.** MCP tools return text. Format it clearly — the LLM will read it.
