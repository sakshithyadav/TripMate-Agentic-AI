# ✈️ TripMate AI – Agentic Multi-Agent Travel Planning System

**TripMate AI** is an intelligent, multi-agent travel planning platform that transforms natural-language travel requests into structured, personalized travel itineraries.

Built using **LangGraph, MCP, FastAPI, and Large Language Models (LLMs)**, the system uses a supervisor-driven architecture to coordinate specialized AI agents for flight research, hotel discovery, weather analysis, budget estimation, and itinerary generation.

Unlike traditional AI travel chatbots, TripMate AI incorporates dynamic agent routing, external tool integrations, Human-in-the-Loop approval, persistent workflow checkpointing, and automatic LLM provider fallback to create a more reliable and interactive travel planning experience.

## Key Features

- **Multi-Agent Orchestration:** Supervisor-driven workflow using LangGraph to coordinate specialized travel agents.
- **Dynamic Agent Routing:** Selects relevant agents based on the user's travel requirements.
- **MCP Integrations:** Connects with Tavily, AviationStack, and a custom Weather MCP server.
- **Intelligent Travel Planning:** Generates flight guidance, hotel recommendations, weather insights, budget analysis, and day-by-day itineraries.
- **Human-in-the-Loop (HITL):** Allows users to review, approve, or request revisions to AI-generated travel plans.
- **Input Guardrails:** Validates incoming requests to keep the application focused on travel-related tasks.
- **Persistent Workflow Checkpointing:** Uses PostgreSQL with LangGraph Postgres Checkpointer to preserve workflow state and support resumption.
- **LLM Failover:** Supports Groq as the primary LLM and local Ollama Gemma4:e2b as a fallback model.
- **REST API:** FastAPI-based backend for interacting with the multi-agent system.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Agent Orchestration | LangGraph |
| LLM Integration | LangChain |
| Primary LLM | Groq |
| Fallback LLM | Ollama – Gemma4:e2b |
| Agent Communication & Tools | Model Context Protocol (MCP) |
| Flight Data | AviationStack |
| Web Research | Tavily |
| Weather Information | OpenWeather API via custom MCP server |
| Backend | FastAPI |
| Database | PostgreSQL |
| Workflow Persistence | LangGraph Postgres Checkpointer |
| Frontend | HTML, CSS, JavaScript |

## System Architecture

1. The user submits a travel request through the web interface.
2. FastAPI receives and validates the request.
3. The Supervisor Agent applies input guardrails and determines which specialist agents are required.
4. Selected agents independently gather relevant information using external MCP tools and LLM reasoning.
5. The Itinerary Agent combines the available information into a structured travel plan.
6. The Human-in-the-Loop mechanism pauses execution for user approval or revision feedback.
7. The Final Response Agent generates the polished travel itinerary.
8. PostgreSQL checkpointing preserves the workflow state for later resumption.

## Project Goals

- Explore practical multi-agent AI orchestration.
- Integrate external APIs through MCP.
- Implement stateful AI workflows using LangGraph.
- Improve reliability through LLM fallback mechanisms.
- Introduce human oversight into autonomous AI workflows.
- Build a modular and extensible AI application.

## Future Enhancements

- Comprehensive agent and workflow evaluation.
- LLM observability and tracing using Langfuse.
- Automated routing and response quality benchmarks.
- Improved retry, timeout, and failure-recovery mechanisms.
- Authentication, authorization, and scalable deployment.
- Advanced performance and cost monitoring.


# Multi-Agent-System-using-LangGraph-MCP-Supervisor-Guardrails-HITL

Prerequisites
- Python 3.10+ (recommended)
- Git (to clone the repo)
- A virtual environment tool (venv) or similar

Quick start (Windows)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1    # PowerShell
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run the FastAPI app (development)

```powershell
# option A (run module)
python app.py

# option B (uvicorn)
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

4. Open the web UI

Visit http://127.0.0.1:8000 in your browser to use the TripMate frontend.

Running the MCP server (example)
- The repository includes `custom_weather_mcp_server.py` as an example MCP server. Run it in a separate terminal if you want to experiment with custom adapters used by the demo.

```powershell
# start example MCP server (if needed)
python custom_weather_mcp_server.py
```

API Endpoints
- `POST /api/travel` — create or resume a travel planning thread. JSON: `{ "message": "<user prompt>", "thread_id": "optional-thread-id" }`
- `POST /api/travel/approve` — approve or request revisions for a draft. JSON: `{ "thread_id": "<id>", "approved": true|false, "feedback": "optional" }`
- `GET /health` — basic health check and features list

Configuration & environment
- Secrets and API keys are not included in the repo. Use environment variables or a `.env` file for any required keys consumed by `langgraph`, `langchain`, or other adapters.


## Author

Developed as an exploration of Agentic AI, multi-agent systems, MCP integrations, and production-oriented LLM application architecture.

