🧠 StoryWeaver: AI-Powered Agile Ticket Refiner

StoryWeaver is an autonomous AI agent built for the GenAI Academy. It solves a massive pain point in software development: translating vague, unstructured feature requests (Product Manager or Client "brain-dumps") into strictly formatted, developer-ready Agile tickets.

By leveraging Google's Agent Development Kit (ADK) and Pydantic schemas, this microservice forces the LLM to output predictable, deeply structured JSON containing Acceptance Criteria, Edge Cases, and Complexity Estimates.

🚀 Key Features

Strict JSON Outputs: Uses ADK's output_schema parameter to guarantee a predictable Pydantic structure.

Agile Contextualization: Synthesizes standard User Stories and extrapolates missing Edge Cases automatically.

Serverless Ready: Containerized and optimized for high-availability deployment on Google Cloud Run.

🏗️ Architecture Flow

sequenceDiagram
    participant User/Webhook
    participant FastAPI as StoryWeaver API
    participant ADK as Google ADK Agent
    participant Gemini as Gemini 2.5 Flash

    User/Webhook->>FastAPI: POST /refine { "text": "messy brain dump" }
    FastAPI->>ADK: Pass unstructured text
    ADK->>Gemini: Prompt + Pydantic JSON Schema
    Gemini-->>ADK: Return formatted JSON ticket
    ADK-->>FastAPI: Parse to Python Object
    FastAPI-->>User/Webhook: Return 200 OK (Structured Agile Ticket)


🛠️ Local Setup & Installation

1. Prerequisites

Python 3.12+

A Google Gemini API Key

2. Clone and Install

git clone [https://github.com/yourusername/story-weaver.git](https://github.com/yourusername/story-weaver.git)
cd story-weaver

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt


3. Run the Server

export GOOGLE_API_KEY="your_api_key_here"
uvicorn main:app --host 0.0.0.0 --port 8080 --reload


☁️ Deployment to Google Cloud Run

Deploy this agent directly via the gcloud CLI:

gcloud run deploy story-weaver-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_api_key_here"


💻 Usage Example

Request:

curl -X POST "http://localhost:8080/refine" \
     -H "Content-Type: application/json" \
     -d '{"text": "We need to let people pay with Apple Pay. Also if their card gets declined don’t just show a generic error, tell them exactly what failed so support stops getting tickets."}'


Expected JSON Response:

{
  "title": "Implement Apple Pay Integration with Specific Error Handling",
  "ticket_type": "Feature",
  "user_story": "As a customer, I want to use Apple Pay at checkout so that I can complete my purchase quickly and securely.",
  "acceptance_criteria": [
    "Apple Pay button is visible and functional on the checkout page.",
    "Payment processing successfully routes through the Apple Pay API.",
    "If a transaction is declined, the UI displays the specific failure reason (e.g., 'Insufficient Funds', 'Card Expired') instead of a generic error."
  ],
  "edge_cases": [
    "User device does not support Apple Pay (hide/disable button).",
    "Network timeout during the Apple Pay authorization handshake.",
    "Apple Pay returns an undocumented error code (fallback to generic error and log to Sentry)."
  ],
  "complexity_estimate": "M"
}
