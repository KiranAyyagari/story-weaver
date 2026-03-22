import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import ticket_refiner_agent
from schemas import AgileTicket

app = FastAPI(title="StoryWeaver API", description="AI Agile Ticket Refiner")

class BrainDumpRequest(BaseModel):
    text: str = "Make the login button pop more and let people use their Google accounts. Also if they enter the wrong password too many times lock them out."

@app.post("/refine", response_model=AgileTicket)
async def refine_ticket(request: BrainDumpRequest):
    try:
        # Pass the messy text to the ADK agent
        response = await ticket_refiner_agent.run(request.text)
        
        # In ADK, structured outputs are often returned in response.data.
        # If the framework returns it as a JSON string, we safely parse it.
        if hasattr(response, 'data') and response.data:
            return response.data
            
        text_response = getattr(response, "text", str(response))
        
        # Clean up markdown code blocks if the LLM wraps the JSON
        if text_response.strip().startswith("```json"):
            text_response = text_response.strip().strip("```json").strip("```").strip()
            
        return json.loads(text_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Automatically bind to the port Cloud Run provides
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)