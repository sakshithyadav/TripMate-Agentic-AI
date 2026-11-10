from pathlib import Path
import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from backend import run_travel_agent, resume_travel_agent

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(
    title="TripMate AI",
    description="LangGraph multi-agent travel planner with MCP, guardrails and human approval.",
    version="2.1.0",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TravelRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    thread_id: str | None = None


class ApprovalRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    approved: bool
    feedback: str = ""


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.post("/api/travel")
def travel_planner(data: TravelRequest):
    try:
        message = data.message.strip()
        if not message:
            return JSONResponse(status_code=400, content={"success": False, "error": "Please enter a travel request."})
        result = run_travel_agent(user_input=message, thread_id=data.thread_id)
        return JSONResponse(content={"success": True, **result})
    except Exception as exc:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"success": False, "error": str(exc)})


@app.post("/api/travel/approve")
def approve_travel_plan(data: ApprovalRequest):
    try:
        if not data.approved and not data.feedback.strip():
            return JSONResponse(status_code=400, content={"success": False, "error": "Please provide feedback when requesting a revision."})
        result = resume_travel_agent(thread_id=data.thread_id, approved=data.approved, feedback=data.feedback)
        return JSONResponse(content={"success": True, **result})
    except Exception as exc:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"success": False, "error": str(exc)})


@app.get("/health")
async def health():
    return {"status": "ok", "message": "TripMate AI API is running"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
