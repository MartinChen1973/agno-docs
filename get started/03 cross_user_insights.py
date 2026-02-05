from os import getenv, makedirs
from os.path import dirname
from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
## ⬇️ Key difference: Import knowledge and vector database components for cross-user learning
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIResponses
from agno.vectordb.chroma import ChromaDb, SearchType

# Load .env file
load_dotenv(find_dotenv(), override=True)

# Ensure tmp directory exists
db_path = "tmp/agents.db"
chroma_path = "tmp/chromadb"
makedirs(dirname(db_path), exist_ok=True)
makedirs(chroma_path, exist_ok=True)

## ⬇️ Key difference: Knowledge base shared across all users for cross-user insights
knowledge = Knowledge(
    name="Agent Learnings",
    vector_db=ChromaDb( ## ⬅️ Using ChromaDB as the vector database for faster processing
        name="learnings",
        path=chroma_path,
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small", ## ⬅️ Using a smaller embedding model for faster processing
            api_key=getenv("OPENAI_API_KEY"),
            base_url=getenv("OPENAI_BASE_URL"),
        ),
    ),
)

# Get environment variables
agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    db=SqliteDb(db_file=db_path),
    add_history_to_context=True,
    ## ⬇️ Key difference: LearnedKnowledge in agentic mode - agent decides what to save, shared across users
    learning=LearningMachine(
        knowledge=knowledge,
        learned_knowledge=LearnedKnowledgeConfig(mode=LearningMode.AGENTIC), ## ⬅️ Agent controls what learnings to save, accessible to all users
    ),
    markdown=True,
)

if __name__ == "__main__":
    ## ⬇️ Key difference: Cross-user learning - User 1 teaches something, User 2 benefits from it
    # Session 1: User 1 teaches the agent
    print("\n--- Session 1: User 1 saves a learning ---\n")
    agent.print_response(
        "We're trying to reduce our cloud egress costs. Remember this.",
        user_id="engineer_1@example.com",
        session_id="session_1",
        stream=True,
    )
    lm = agent.get_learning_machine()
    lm.learned_knowledge_store.print(query="cloud")

    # Session 2: User 2 benefits from the learning
    print("\n--- Session 2: User 2 asks a related question ---\n")
    agent.print_response(
        "I'm picking a cloud provider for a data pipeline. Key considerations?",
        user_id="engineer_2@example.com",
        session_id="session_2",
        stream=True,
    )
