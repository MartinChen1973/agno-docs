from os import getenv
import random

from dotenv import find_dotenv, load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools import tool

load_dotenv(find_dotenv(), override=True)


## ⬇️ Define custom tool function
def get_weather(city: str) -> str:
    """Get the weather for the given city.

    Args:
        city (str): The city to get the weather for.
    """

    # In a real implementation, this would call a weather API
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    random_weather = random.choice(weather_conditions)

    return f"The weather in {city} is {random_weather}."


## ⬇️ Create agent with custom tool
agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    tools=[get_weather], ## ⬅️ Pass custom tool to agent
    markdown=True,
)


## ⬇️ Use agent with tool
if __name__ == "__main__":
    # Our Agent will now be able to use our tool, when it deems it relevant
    agent.print_response("What is the weather in San Francisco?", stream=True)
