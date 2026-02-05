from os import getenv
import asyncio

from dotenv import find_dotenv, load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.mcp import MCPTools

## ⬇️ Load environment variables
load_dotenv(find_dotenv(), override=True)


## ⬇️ Initialize and connect to the MCP server
async def main():
    mcp_tools = MCPTools(url="https://docs.agno.com/mcp")
    await mcp_tools.connect()

    try:
        agent = Agent(
            model=OpenAIResponses(
                id=getenv("DEFAULT_MODEL_ID"),
                api_key=getenv("OPENAI_API_KEY"),
                base_url=getenv("OPENAI_BASE_URL"),
            ),
            tools=[mcp_tools], ## ⬅️ Pass MCP tools to agent
        )
        await agent.aprint_response("Tell me more about MCP support in Agno", stream=True)
    finally:
        ## ⬇️ Always close the connection when done
        await mcp_tools.close()


if __name__ == "__main__":
    asyncio.run(main())
