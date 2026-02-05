from os import getenv
from typing import AsyncIterator, Iterator

from dotenv import find_dotenv, load_dotenv
import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.db.sqlite import SqliteDb
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools
from agno.workflow import Step, Workflow, Condition, StepInput
from agno.run.workflow import WorkflowRunOutput, WorkflowRunOutputEvent, WorkflowRunEvent
from agno.utils.pprint import pprint_run_response

## ⬇️ Load environment variables
load_dotenv(find_dotenv(), override=True)


## ⬇️ Define agents for the workflow
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


## ⬇️ Example 1: Basic synchronous execution
def example_basic_run():
    """Run workflow synchronously and get WorkflowRunOutput"""
    print("=" * 70)
    print("Example 1: Basic Synchronous Execution")
    print("=" * 70)
    
    response: WorkflowRunOutput = content_creation_workflow.run(
        input="AI trends in 2024",
        markdown=True,
    )
    
    pprint_run_response(response, markdown=True)


## ⬇️ Example 2: Async execution
async def example_async_run():
    """Run workflow asynchronously using arun()"""
    print("\n" + "=" * 70)
    print("Example 2: Async Execution")
    print("=" * 70)
    
    try:
        response: WorkflowRunOutput = await content_creation_workflow.arun(
            input="AI trends in 2024",
            markdown=True,
        )
        pprint_run_response(response, markdown=True)
    except Exception as e:
        print(f"Error: {e}")


## ⬇️ Example 3: Streaming responses
def example_streaming():
    """Stream workflow execution events"""
    print("\n" + "=" * 70)
    print("Example 3: Streaming Responses")
    print("=" * 70)
    
    response: Iterator[WorkflowRunOutputEvent] = content_creation_workflow.run(
        input="AI trends in 2024",
        markdown=True,
        stream=True,
    )
    
    pprint_run_response(response, markdown=True)


## ⬇️ Example 4: Streaming all events
def example_streaming_all_events():
    """Stream all workflow events including internal events"""
    print("\n" + "=" * 70)
    print("Example 4: Streaming All Events")
    print("=" * 70)
    
    response: Iterator[WorkflowRunOutputEvent] = content_creation_workflow.run(
        input="AI trends in 2024",
        stream=True,
        stream_events=True,
    )
    
    for event in response:
        if event.event == WorkflowRunEvent.workflow_started.value:
            print(f"→ Workflow Started: {event}")
        elif event.event == WorkflowRunEvent.step_started.value:
            print(f"→ Step Started: {event}")
        elif event.event == WorkflowRunEvent.step_completed.value:
            print(f"→ Step Completed: {event}")
        elif event.event == WorkflowRunEvent.workflow_completed.value:
            print(f"→ Workflow Completed: {event}")


## ⬇️ Example 5: Async streaming
async def example_async_streaming():
    """Stream workflow execution asynchronously"""
    print("\n" + "=" * 70)
    print("Example 5: Async Streaming")
    print("=" * 70)
    
    try:
        response: AsyncIterator[WorkflowRunOutputEvent] = content_creation_workflow.arun(
            input="AI trends in 2024",
            stream=True,
            stream_events=True,
        )
        
        async for event in response:
            if event.event == WorkflowRunEvent.workflow_started.value:
                print(f"→ Workflow Started: {event}")
            elif event.event == WorkflowRunEvent.step_started.value:
                print(f"→ Step Started: {event}")
            elif event.event == WorkflowRunEvent.step_completed.value:
                print(f"→ Step Completed: {event}")
            elif event.event == WorkflowRunEvent.workflow_completed.value:
                print(f"→ Workflow Completed: {event}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


## ⬇️ Example 6: Conditional workflow with streaming
def needs_fact_checking(step_input: StepInput) -> bool:
    """Determine if the research contains claims that need fact-checking"""
    summary = step_input.previous_step_content or ""
    
    ## ⬇️ Look for keywords that suggest factual claims
    fact_indicators = [
        "study shows",
        "breakthroughs",
        "research indicates",
        "according to",
        "statistics",
        "data shows",
        "survey",
        "report",
        "million",
        "billion",
        "percent",
        "%",
        "increase",
        "decrease",
    ]
    
    return any(indicator in summary.lower() for indicator in fact_indicators)


def example_conditional_workflow():
    """Example with conditional steps"""
    print("\n" + "=" * 70)
    print("Example 6: Conditional Workflow")
    print("=" * 70)
    
    ## ⬇️ Define agents for conditional workflow
    researcher = Agent(
        name="Researcher",
        model=OpenAIResponses(
            id=getenv("DEFAULT_MODEL_ID", "gpt-4o"),
            api_key=getenv("OPENAI_API_KEY"),
            base_url=getenv("OPENAI_BASE_URL"),
        ),
        instructions="Research the given topic and provide detailed findings.",
        tools=[HackerNewsTools()],
    )
    
    summarizer = Agent(
        name="Summarizer",
        model=OpenAIResponses(
            id=getenv("DEFAULT_MODEL_ID", "gpt-4o"),
            api_key=getenv("OPENAI_API_KEY"),
            base_url=getenv("OPENAI_BASE_URL"),
        ),
        instructions="Create a clear summary of the research findings.",
    )
    
    fact_checker = Agent(
        name="Fact Checker",
        model=OpenAIResponses(
            id=getenv("DEFAULT_MODEL_ID", "gpt-4o"),
            api_key=getenv("OPENAI_API_KEY"),
            base_url=getenv("OPENAI_BASE_URL"),
        ),
        instructions="Verify facts and check for accuracy in the research.",
        tools=[HackerNewsTools()],
    )
    
    writer = Agent(
        name="Writer",
        model=OpenAIResponses(
            id=getenv("DEFAULT_MODEL_ID", "gpt-4o"),
            api_key=getenv("OPENAI_API_KEY"),
            base_url=getenv("OPENAI_BASE_URL"),
        ),
        instructions="Write a comprehensive article based on all available research and verification.",
    )
    
    ## ⬇️ Define workflow steps
    research_step = Step(
        name="research",
        description="Research the topic",
        agent=researcher,
    )
    
    summarize_step = Step(
        name="summarize",
        description="Summarize research findings",
        agent=summarizer,
    )
    
    fact_check_step = Step(
        name="fact_check",
        description="Verify facts and claims",
        agent=fact_checker,
    )
    
    write_article = Step(
        name="write_article",
        description="Write final article",
        agent=writer,
    )
    
    ## ⬇️ Create workflow with conditional step
    basic_workflow = Workflow(
        name="Basic Linear Workflow",
        description="Research -> Summarize -> Condition(Fact Check) -> Write Article",
        steps=[
            research_step,
            summarize_step,
            Condition(
                name="fact_check_condition",
                description="Check if fact-checking is needed",
                evaluator=needs_fact_checking,
                steps=[fact_check_step],
            ),
            write_article,
        ],
    )
    
    try:
        response: Iterator[WorkflowRunOutputEvent] = basic_workflow.run(
            input="Recent breakthroughs in quantum computing",
            stream=True,
            stream_events=True,
        )
        
        for event in response:
            if event.event == WorkflowRunEvent.condition_execution_started.value:
                print(f"→ Condition Execution Started: {event}")
            elif event.event == WorkflowRunEvent.condition_execution_completed.value:
                print(f"→ Condition Execution Completed: {event}")
            elif event.event == WorkflowRunEvent.workflow_started.value:
                print(f"→ Workflow Started: {event}")
            elif event.event == WorkflowRunEvent.step_started.value:
                print(f"→ Step Started: {event}")
            elif event.event == WorkflowRunEvent.step_completed.value:
                print(f"→ Step Completed: {event}")
            elif event.event == WorkflowRunEvent.workflow_completed.value:
                print(f"→ Workflow Completed: {event}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    ## ⬇️ Run examples
    ## Uncomment the example you want to run:
    
    # example_basic_run()
    # asyncio.run(example_async_run())
    # example_streaming()
    # example_streaming_all_events()
    # asyncio.run(example_async_streaming())
    example_conditional_workflow()
