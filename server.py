import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import ticket_refiner_agent
from schemas import AgileTicket

app = FastAPI(title="StoryWeaver API", description="AI Agile Ticket Refiner")

session_service = InMemorySessionService()
runner = Runner(agent=ticket_refiner_agent, app_name="story-weaver", session_service=session_service)

class StoryWeaverRequest(BaseModel):
    text: str = "Make the login button pop more and let people use their Google accounts. Also if they enter the wrong password too many times lock them out."

@app.post("/refine", response_model=AgileTicket)
async def refine_ticket(request: StoryWeaverRequest):
    try:
        session = await session_service.create_session(app_name="story-weaver", user_id="user")
        content = types.Content(role="user", parts=[types.Part(text=request.text)])

        final_response = None
        async for event in runner.run_async(
            user_id="user",
            session_id=session.id,
            new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
                break

        if not final_response:
            raise ValueError("No response from agent")

        # Clean up markdown code blocks if the LLM wraps the JSON
        text = final_response.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        return AgileTicket(**json.loads(text))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
