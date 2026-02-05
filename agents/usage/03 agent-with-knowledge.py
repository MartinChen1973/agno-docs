from os import getenv

from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIResponses
from agno.vectordb.lancedb import LanceDb, SearchType

# Load .env file
load_dotenv(find_dotenv(), override=True)

## ⬇️ Create knowledge base with vector database and embedder
knowledge = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="recipes", 
        search_type=SearchType.hybrid, ## ⬅️ Use hybrid search (semantic + keyword)
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small", ## ⬅️ Embedding model ID
            api_key=getenv("OPENAI_API_KEY"), 
            base_url=getenv("OPENAI_BASE_URL"), 
        ),
    ),
)

## ⬇️ Load a PDF into the knowledge base
knowledge.insert(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf", 
)

agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"), 
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    knowledge=knowledge, ## ⬅️ Attach knowledge base to agent
    instructions="Search your knowledge base for Thai recipes. Be concise.",
    markdown=True, 
    debug_mode=True,
)

print("Starting agent run...")
agent.print_response("How do I make Pad Thai?", stream=True)
agent.print_response("What ingredients do I need for green curry?", stream=True)
print("Agent run completed.")
