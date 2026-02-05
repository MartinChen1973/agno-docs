from os import getenv
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.yfinance import YFinanceTools
from pydantic import BaseModel, Field

# Load .env file
load_dotenv(find_dotenv(), override=True)


## ⬇️ Pydantic model for the output
class StockAnalysis(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Full company name")
    current_price: float = Field(..., description="Current price in USD")
    pe_ratio: Optional[float] = Field(None, description="P/E ratio")
    summary: str = Field(..., description="One-line summary")
    key_drivers: List[str] = Field(..., description="2-3 key growth drivers")
    key_risks: List[str] = Field(..., description="2-3 key risks")


agent = Agent(
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    tools=[YFinanceTools()], ## ⬅️ Pass the tools to the agent
    output_schema=StockAnalysis, ## ⬅️ Pass the Pydantic model to the agent
    debug_mode=True,
)

print("Starting agent run...")
response = agent.run("Analyze NVIDIA stock")
print("Agent run completed.")

# Access typed data directly
analysis: StockAnalysis = response.content ## ⬅️ Access the typed data directly
print(f"{analysis.company_name} ({analysis.ticker})")
print(f"Price: ${analysis.current_price}")
print(f"P/E Ratio: {analysis.pe_ratio or 'N/A'}")
print(f"Summary: {analysis.summary}")
print("Key Drivers:")
for driver in analysis.key_drivers:
    print(f"  - {driver}")
print("Key Risks:")
for risk in analysis.key_risks:
    print(f"  - {risk}")