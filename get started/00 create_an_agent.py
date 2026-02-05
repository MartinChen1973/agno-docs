from os import getenv
from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike

# Load .env file
load_dotenv(find_dotenv(), override=True)

# Get environment variables
agent = Agent(
    model=OpenAILike(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    )
)

agent.print_response("Hi! I'm Alice. I work at Anthropic as a research scientist.", stream=True)