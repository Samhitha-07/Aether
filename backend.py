# Setup pydantic model
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
     model_name: str
     model_provider: str
     system_prompt: str
     messages: List[str]
     allow_search: bool
# Setup AI agent from frontend
from fastapi import FastAPI
from agent_ai import get_response_from_ai_agent
Allowed_models = ["llama3-70b-8192","mixtral-8x7b-32768","llama3-70b-versatile","gpt-4o-mini"]
app=FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    
    """
    if request.model_name not in Allowed_models:
        return {"error": "Invalid model name"}
    
    llm_id=request.model_name
    query=request.messages
    system_prompt=request.system_prompt
    allow_search=request.allow_search
    provider=request.model_provider
    #create ai agent
    response=get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider)
    return response
# Swagger UI testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)