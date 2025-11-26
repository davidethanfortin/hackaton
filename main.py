from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import uvicorn
from beans import QueryBean
from service import AgentQueryService

app = FastAPI(title="Query Generator API", version="1.0.0")
agent_service = AgentQueryService()


@app.post("/generate")
async def generate_query(request: QueryBean):
    """
    Generate a greeting message.
    
    - **uiFieldName**: UI field name
    - **policyType**: Policy type
    """
    result = agent_service.call_agent(request)
    return result


@app.get("/")
async def root():
    return {"message": "Query Generator API", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
