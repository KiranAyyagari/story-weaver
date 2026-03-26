# 🧠 StoryWeaver

> AI-powered Agile ticket refiner — turns messy stakeholder brain-dumps into structured, developer-ready tickets.

Built with [Google ADK](https://google.github.io/adk-docs/) + Gemini 2.5 Flash, deployed on Google Cloud Run.

---

## How it works

```
POST /refine  →  ADK Runner  →  Gemini 2.5 Flash  →  Structured JSON ticket
```

1. You send unstructured text (a feature request, a complaint, a brain-dump)
2. The ADK agent prompts Gemini with a strict Pydantic output schema
3. You get back a clean, validated Agile ticket every time

---

## Output schema

| Field | Type | Description |
|---|---|---|
| `title` | `string` | Clear, concise ticket title |
| `ticket_type` | `Feature \| Bug \| Chore \| Spike` | Category of work |
| `user_story` | `string` | Standard "As a... I want... so that..." format |
| `acceptance_criteria` | `string[]` | Testable done conditions |
| `edge_cases` | `string[]` | Error states and UX traps to handle |
| `complexity_estimate` | `XS \| S \| M \| L \| XL` | T-shirt size effort estimate |

---

## Local setup

**Prerequisites:** Python 3.12+, a Gemini API key

```bash
git clone https://github.com/yourusername/story-weaver.git
cd story-weaver

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

export GOOGLE_API_KEY="your_api_key_here"   # Windows: set GOOGLE_API_KEY=your_api_key_here
python server.py
```

Server runs at `http://localhost:8080`

---

## Deploy to Cloud Run

```bash
gcloud run deploy story-weaver-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_api_key_here"
```

---

## Usage

**Linux / macOS**
```bash
curl -X POST "https://YOUR_SERVICE_URL/refine" \
  -H "Content-Type: application/json" \
  -d '{"text": "We need Apple Pay. Also show specific decline reasons instead of generic errors."}'
```

**Windows CMD**
```cmd
curl -X POST "https://YOUR_SERVICE_URL/refine" -H "Content-Type: application/json" -d "{\"text\": \"We need Apple Pay. Also show specific decline reasons instead of generic errors.\"}"
```

**Example response**
```json
{
  "title": "Implement Apple Pay with Specific Decline Error Handling",
  "ticket_type": "Feature",
  "user_story": "As a customer, I want to pay with Apple Pay and see specific error messages on decline so that I can resolve payment issues without contacting support.",
  "acceptance_criteria": [
    "Apple Pay button appears on checkout for supported devices.",
    "Successful payments are processed and confirmed.",
    "Declined transactions show a specific reason (e.g. 'Insufficient Funds', 'Card Expired')."
  ],
  "edge_cases": [
    "Device does not support Apple Pay — hide the button.",
    "Network timeout during authorization handshake.",
    "Undocumented error code returned — fallback to generic message and log the error."
  ],
  "complexity_estimate": "M"
}
```

Interactive API docs available at `/docs`.
