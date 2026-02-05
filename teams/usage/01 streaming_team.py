from os import getenv

from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools

# Load .env file
load_dotenv(find_dotenv(), override=True)


## ⬇️ Create specialized agents for the team
news_agent = Agent(
    name="News Agent",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    role="Gets trending tech stories from HackerNews.",
    tools=[HackerNewsTools()], ## ⬅️ Pass HackerNews tools to the news agent
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    role="Gets stock prices and financial data.",
    tools=[YFinanceTools()], ## ⬅️ Pass YFinance tools to the finance agent
)

## ⬇️ Create the team with both agents
team = Team(
    name="Research Team",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    members=[news_agent, finance_agent], ## ⬅️ Add both agents as team members
    markdown=True,
    show_members_responses=True,
)

print("Starting streaming team run...")

# Stream the response in real-time
team.print_response(
    input="What are the trending AI stories and how is NVDA stock doing?",
    stream=True, ## ⬅️ Enable streaming for real-time output
)

print("\nStreaming team run completed.")
