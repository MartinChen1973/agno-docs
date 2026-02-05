from os import getenv

from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.yfinance import YFinanceTools

# Load .env file
load_dotenv(find_dotenv(), override=True)

## ⬇️ Initialize SQLite database for agent storage
db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    tools=[YFinanceTools()], 
    db=db, ## ⬅️ Pass the database for storage
    add_history_to_context=True, ## ⬅️ Enable history in context
    num_history_runs=5, ## ⬅️ Include last 5 runs in context
    markdown=True, ## ⬅️ Enable markdown formatting
)

session_id = "finance-session"

# Turn 1: Analyze a stock
agent.print_response(
    "Give me a quick analysis of NVIDIA",
    session_id=session_id,
    stream=True,
)

# Turn 2: The agent remembers NVDA from turn 1
agent.print_response(
    "Compare that to AMD",
    session_id=session_id,
    stream=True,
)

# Turn 3: Ask based on full conversation
agent.print_response(
    "Which looks like the better investment?",
    session_id=session_id,
    stream=True,
)
