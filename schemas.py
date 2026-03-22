from pydantic import BaseModel, Field
from typing import List, Literal

class AgileTicket(BaseModel):
    """
    This schema defines the exact structure we want the Gemini model to return.
    Using 'Literal' forces the model to choose from a strict list of options.
    """
    title: str = Field(description="A clear, concise, and professional title for the ticket.")
    ticket_type: Literal["Feature", "Bug", "Chore", "Spike"] = Field(description="Categorize the type of work.")
    user_story: str = Field(description="Standard agile format: 'As a [role], I want to [action] so that [benefit]'.")
    acceptance_criteria: List[str] = Field(description="A bulleted list of strict conditions that must be met for this ticket to be considered 'Done'.")
    edge_cases: List[str] = Field(description="Potential error states, edge cases, or UX traps the developer needs to handle.")
    complexity_estimate: Literal["XS", "S", "M", "L", "XL"] = Field(description="A T-shirt size estimate of the development effort required.")