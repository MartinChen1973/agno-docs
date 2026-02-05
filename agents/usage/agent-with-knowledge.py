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
        uri="tmp/lancedb", ## ⬅️ Local path for vector database storage
        table_name="recipes", ## ⬅️ Table name in the vector database
        search_type=SearchType.hybrid, ## ⬅️ Use hybrid search (semantic + keyword)
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small", ## ⬅️ Embedding model ID
            api_key=getenv("OPENAI_API_KEY"), ## ⬅️ OpenAI API key for embeddings
            base_url=getenv("OPENAI_BASE_URL"), ## ⬅️ Base URL for OpenAI API
        ),
    ),
)

## ⬇️ Load a PDF into the knowledge base
knowledge.insert(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf", ## ⬅️ URL to the document to ingest
)

## ⬇️ Create agent with knowledge base
agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"), ## ⬅️ Model ID from environment
        api_key=getenv("OPENAI_API_KEY"), ## ⬅️ OpenAI API key
        base_url=getenv("OPENAI_BASE_URL"), ## ⬅️ Base URL for OpenAI API
    ),
    knowledge=knowledge, ## ⬅️ Attach knowledge base to agent
    instructions="Search your knowledge base for Thai recipes. Be concise.", ## ⬅️ Instructions for the agent
    markdown=True, ## ⬅️ Enable markdown formatting in responses
    debug_mode=True,
)

print("Starting agent run...")
## ⬇️ Query the agent with streaming enabled
agent.print_response("How do I make Pad Thai?", stream=True)
agent.print_response("What ingredients do I need for green curry?", stream=True)
print("Agent run completed.")
