from os import getenv
from typing import Iterator

from dotenv import find_dotenv, load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.db.sqlite import SqliteDb
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools
from agno.workflow import Step, Workflow
from agno.run.workflow import WorkflowRunOutput, WorkflowRunOutputEvent, WorkflowRunEvent
from agno.utils.pprint import pprint_run_response

## ⬇️ Load environment variables
load_dotenv(find_dotenv(), override=True)


## ⬇️ Define agents
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    tools=[HackerNewsTools()], ## ⬅️ HackerNews tools for research
    role="Extract key insights and content from Hackernews posts",
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    tools=[YFinanceTools()], ## ⬅️ YFinance tools for stock data
    role="Get stock prices and financial data",
)

## ⬇️ Define research team for complex analysis
research_team = Team(
    name="Research Team",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    members=[hackernews_agent, finance_agent],
    instructions="Research tech topics and related stocks",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    instructions=[
        "Plan a content schedule over 4 weeks for the provided topic and research content",
        "Ensure that I have posts for 3 posts per week",
    ],
)

## ⬇️ Create the workflow
content_creation_workflow = Workflow(
    name="Content Creation Workflow",
    description="Automated content creation from blog posts to social media",
    db=SqliteDb(db_file="tmp/workflow.db"),
    steps=[research_team, content_planner],
)


## ⬇️ Create and use workflow
if __name__ == "__main__":
    ## ⬇️ Stream workflow execution to see all steps and agent actions
    response: Iterator[WorkflowRunOutputEvent] = content_creation_workflow.run(
        input="AI trends in 2025",
        markdown=True,
        stream=True,
        stream_events=True,
    )
    
    ## ⬇️ Process and display events as they occur
    for event in response:
        if event.event == WorkflowRunEvent.workflow_started.value:
            print(f"→ Workflow Started: {event.workflow_name or 'Content Creation Workflow'}")
        elif event.event == WorkflowRunEvent.step_started.value:
            print(f"→ Step Started: {event.step_name}")
        elif event.event == WorkflowRunEvent.step_completed.value:
            print(f"→ Step Completed: {event.step_name}")
            if hasattr(event, 'content') and event.content:
                content_str = str(event.content)
                print(f"  Content preview: {content_str[:200]}..." if len(content_str) > 200 else f"  Content: {content_str}")
        elif event.event == WorkflowRunEvent.workflow_completed.value:
            print(f"→ Workflow Completed")
            if hasattr(event, 'content') and event.content:
                print(f"\nFinal Result:\n{event.content}")
