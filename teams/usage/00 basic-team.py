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
hn_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    role="Gets trending stories from HackerNews.",
    tools=[HackerNewsTools()], ## ⬅️ Pass HackerNews tools to the researcher
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
    members=[hn_researcher, finance_agent], ## ⬅️ Add both agents as team members
    instructions=[
        ## ⬇️ Comment those 2 Delegation instructions to see the results (should still work)
        "Delegate to the HackerNews Researcher for tech news and trends.",
        "Delegate to the Finance Agent for stock prices and financial data.",
        "Synthesize the results into a clear summary.",
    ],
    markdown=True,
    show_members_responses=True,
)

print("Starting team run...")
team.print_response(
    input="What are the top AI stories on HackerNews and how is NVDA doing?",
    stream=True
)
print("Team run completed.")
