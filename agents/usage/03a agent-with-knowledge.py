from os import getenv
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.models.openai import OpenAIResponses
from agno.vectordb.lancedb import LanceDb, SearchType

# Load .env file
load_dotenv(find_dotenv(), override=True)

## ⬇️ Create knowledge base with vector database and embedder
knowledge = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="markdown_docs", 
        search_type=SearchType.vector, ## ⬅️ Use hybrid search (semantic + keyword)
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small", ## ⬅️ Embedding model ID
            api_key=getenv("OPENAI_API_KEY"), 
            base_url=getenv("OPENAI_BASE_URL"), 
        ),
    ),
)

## ⬇️ Load markdown files from local path with markdown chunking
documents_path = Path(__file__).parent / "documents" ## ⬅️ Absolute path to documents directory
knowledge.insert(
    path=str(documents_path), ## ⬅️ Path to directory or file containing markdown
    reader=MarkdownReader(
        chunking_strategy=MarkdownChunking(), ## ⬅️ Use markdown-aware chunking
    ),
)

agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"), 
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    knowledge=knowledge, ## ⬅️ Attach knowledge base to agent
    instructions="Search your knowledge base for information. Be concise.",
    markdown=True, 
    debug_mode=True,
)

print("Starting agent run...")
agent.print_response("What information is available in the knowledge base?", stream=True)
# agent.print_response("Summarize the key topics covered.", stream=True)
# agent.print_response("What flavors does BingChuan ice cream offer?", stream=True)
print("Agent run completed.")
