from os import getenv

from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.openai import OpenAIResponses
from agno.tools.yfinance import YFinanceTools
from rich.pretty import pprint

# Load .env file
load_dotenv(find_dotenv(), override=True)

## ⬇️ Initialize SQLite database for agent storage and memory
db = SqliteDb(db_file="tmp/agents.db")

## ⬇️ Initialize memory manager to store user preferences
memory_manager = MemoryManager(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    db=db,
)

agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    tools=[YFinanceTools()], 
    db=db, ## ⬅️ Pass the database for storage
    memory_manager=memory_manager, ## ⬅️ Pass the memory manager
    enable_agentic_memory=True, ## ⬅️ Enable agentic memory (agent decides when to store/recall)
    markdown=True,
)

user_id = "investor@example.com"

# Tell the agent about yourself
agent.print_response(
    "I'm interested in AI and semiconductor stocks. My risk tolerance is moderate.",
    user_id=user_id,
    stream=True,
)

# The agent now knows your preferences
agent.print_response(
    "What stocks would you recommend for me?",
    user_id=user_id,
    stream=True,
)

# View stored memories
memories = agent.get_user_memories(user_id=user_id)
print("\nStored Memories:")
pprint(memories)
