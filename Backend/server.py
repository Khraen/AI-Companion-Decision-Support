import os
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import DecisionAnalyzer.Engine as Engine
import DecisionAnalyzer.long_term_memory_manager  as MemoryManager


app = FastAPI(title="FastAPI for Matt's cortana",
              description="server that holds api endpts for react ui",
              )

# origin port of the react build. both development server and production. Note: if using cloud, you gotta change the deployment port.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

# needed to allow react to communicate with server.
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials= True,
  allow_methods = ["*"],
  allow_headers= ["*"]
)

class ChatRequest(BaseModel):
  message:str



@app.get("/")
def Root():
  # Message showing the initial backend setup is fine.
  return {"status":"online", "backend-api-system":"cortana-api"}

@app.get("/api/Get-Engine-State")
def GetEngineState():
  """
    Called by React on initial page load to populate your UI panels:
    - profile.json
    - summary.json
    - short-term context window (last 14 messages)
    """

  try:
    profile = Engine.load_profile()
    summary = Engine.load_summary_file()
    context = Engine.load_past_conversation()

    return {
      "profile": profile,
      "summary": summary,
      "context": context
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to load state: {str(e)}")


@app.post("/api/Process-User-Message")
def RetrieveAiMessage(user_message: ChatRequest):
  """
    Triggered when the user types a message and clicks 'Send' in React.
    Passes message to Engine.py, logs to disk, and returns Cortana's response.
    """
  try:
    response_message = Engine.process_chat_message(user_message.message)
    return {
      "response_message": response_message
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"failed to get response message. Chat execution failed {str(e)}")


def run_consolidation_and_reset():
    MemoryManager.consolidate_long_term_memory()
    Engine.reset_active_messages()

@app.put("/api/Consolidate-Memory")
def consolidate_memory(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_consolidation_and_reset)
    return {"status": "Consolidation queued"}
  


if __name__ == "__main__":
  import uvicorn
  # Start server at http://127.0.0.1:8000

  uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)




