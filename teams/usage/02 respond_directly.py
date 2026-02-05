from os import getenv

from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team.team import Team

# Load .env file
load_dotenv(find_dotenv(), override=True)


## ⬇️ Create specialized language agents for the team
english_agent = Agent(
    name="English Agent",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    role="You only answer in English",
)

japanese_agent = Agent(
    name="Japanese Agent",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    role="You only answer in Japanese",
)

spanish_agent = Agent(
    name="Spanish Agent",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    role="You only answer in Spanish",
)

## ⬇️ Create the team with respond_directly=True for direct routing
language_router = Team(
    name="Language Router",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    respond_directly=True, ## ⬅️ Enable direct response mode - agents respond directly without team leader processing
    members=[english_agent, japanese_agent, spanish_agent], ## ⬅️ Add all language agents as team members
    instructions=[
        "Route questions to the appropriate language agent.",
        "If the language is not supported, respond in English.",
    ],
    markdown=True,
    show_members_responses=True,
)

print("Starting language router run...")

# English
print("\n--- English Query ---")
language_router.print_response("How are you?", stream=True)

# Japanese
print("\n--- Japanese Query ---")
language_router.print_response("お元気ですか?", stream=True)

# Spanish
print("\n--- Spanish Query ---")
language_router.print_response("¿Cómo estás?", stream=True)

print("\nLanguage router run completed.")
