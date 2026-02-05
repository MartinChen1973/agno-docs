from os import getenv, makedirs
from os.path import dirname, abspath
from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses

# Load .env file
load_dotenv(find_dotenv(), override=True)

# Ensure tmp directory exists
db_path = "tmp/agents.db"
makedirs(dirname(db_path), exist_ok=True)

# Get environment variables
agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    db=SqliteDb(db_file=db_path),
    add_history_to_context=True, ## ⬅️ This is the history of the conversation
    learning=True,
    markdown=True,
)

if __name__ == "__main__":
    user_id = "alice@example.com"

    # Session 1: Share information naturally
    print("\n--- Session 1: Extraction happens automatically ---\n")
    agent.print_response(
        "Hi! I'm Alice. I work at Anthropic as a research scientist. "
        "I prefer concise responses without too much explanation.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    lm = agent.get_learning_machine() ## ⬅️ This is the learning machine
    lm.user_profile_store.print(user_id=user_id)
    lm.user_memory_store.print(user_id=user_id)

    # Session 2: New session - agent remembers
    print("\n--- Session 2: Agent remembers across sessions ---\n")
    agent.print_response(
        "What do you know about me?",
        user_id=user_id,
        session_id="session_2", ## ⬅️ This is a new session ID
        stream=True,
    )
