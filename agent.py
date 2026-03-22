from google.adk.agents import Agent
from schemas import AgileTicket

# Initialize the Backlog Brain Agent
ticket_refiner_agent = Agent(
    model='gemini-2.5-flash', # Fast, efficient, and great at structured outputs
    name='AgileTicketRefiner',
    description='A Senior Technical Product Manager agent that refines unstructured ideas into precise Agile development tickets.',
    instruction='''
        You are an expert Senior Technical Product Manager. Your job is to take messy, unstructured "brain dumps" from stakeholders or clients and translate them into perfectly formatted, developer-ready Agile tickets.
        
        Follow these steps:
        1. Analyze the input text to identify the core request, the target user, and the desired outcome.
        2. Generate a precise title and a standard user story.
        3. Define clear, testable acceptance criteria.
        4. Identify any edge cases or potential pitfalls the developer should consider.
        5. Estimate the complexity using T-shirt sizing (XS, S, M, L, XL).
        
        You MUST return the output strictly matching the provided JSON schema. Do not include conversational filler.
    ''',
    # This single line forces Gemini to map its response to our Pydantic model
    output_schema=AgileTicket 
)