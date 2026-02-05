from os import getenv
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.skills import Skills, LocalSkills

## ⬇️ Load environment variables
load_dotenv(find_dotenv(), override=True)

## ⬇️ Get skills directory relative to this file
skills_dir = Path(__file__).parent / "skills"

## ⬇️ Create agent with action-finder skill
agent = Agent(
    name="Action Finder Assistant",
    model=OpenAIResponses(
        id=getenv("DEFAULT_MODEL_ID"),
        api_key=getenv("OPENAI_API_KEY"),
        base_url=getenv("OPENAI_BASE_URL"),
    ),
    skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
    instructions=[
        "You have access to the action-finder skill.",
        "When asked to find actions for an entity:",
        "  1. Load the CRUD templates reference using get_skill_reference('action-finder', 'crud-templates.md')",
        "  2. Select the appropriate template (CIDED, CIDRA, or CID) based on the entity type",
        "  3. Generate camelCase action names based on the template and entity name:",
        "     - Transform 'Create' → create{Entity} (e.g., 'createUser' for User entity)",
        "     - Transform 'Index' → list{Entity}s (e.g., 'listUsers' for User entity)",
        "     - Transform 'Details' → get{Entity} (e.g., 'getUser' for User entity)",
        "     - Transform 'Edit' → edit{Entity} (e.g., 'editUser' for User entity)",
        "     - Transform 'Delete' → delete{Entity} (e.g., 'deleteUser' for User entity)",
        "     - DO NOT use template names like 'Create', 'Index', 'Details' - these are WRONG",
        "     - DO use camelCase names like 'createUser', 'listUsers', 'getUser' - these are CORRECT",
        "  4. Log the operation using get_skill_script('action-finder', 'scripts/log.py', execute=True, args=[entity_name, template, ...camelCaseActions])",
        "     Example: args=['User', 'CIDED', 'createUser', 'listUsers', 'getUser', 'editUser', 'deleteUser']",
        "  5. Return the results as a formatted markdown list.",
        "Do NOT use any script to generate actions - generate them intelligently yourself.",
    ],
    markdown=True,
)

if __name__ == "__main__":
    ## ⬇️ Example: Find actions for "User" entity
    print("Finding CRUD actions for 'User' entity:\n")
    agent.print_response("Find all CRUD actions for the User entity")
    
    # print("\n" + "="*50 + "\n")
    
    # ## ⬇️ Example: Find actions for "Product" entity
    # print("Finding CRUD actions for 'Product' entity:\n")
    # agent.print_response("What actions are available for a Product entity?")
