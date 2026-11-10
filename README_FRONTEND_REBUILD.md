# TripMate AI frontend rebuild

This rebuild keeps the existing LangGraph backend modules and API contract, and replaces the FastAPI entry point plus frontend HTML/CSS/JavaScript.

## Run locally (Windows PowerShell)

1. Extract the project ZIP.
2. Open a terminal in the project root (the folder containing `app.py`).
3. Create/activate a virtual environment if needed:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Create your own `.env` file using the variable names documented in your existing project README. Do not share or commit API keys or database credentials.
5. Start the app:

```powershell
python app.py
```

6. Open http://127.0.0.1:8000 and check http://127.0.0.1:8000/health.

The browser frontend calls `POST /api/travel` and `POST /api/travel/approve`, using the response fields returned by `backend._serialize_result`.

## Important

- `backend.py`, `mcp_client.py`, `llm_provider.py`, and the MCP server were preserved; the agent graph was not rewritten.
- The ZIP intentionally excludes `.env`, `.venv`, caches, and generated secrets. Recreate `.env` locally.
- Third-party Google Fonts, Marked, and html2pdf are loaded from CDNs; PDF export and custom fonts need internet access. Markdown still displays as plain escaped text if Marked cannot load.
