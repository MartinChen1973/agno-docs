---
name: action-finder
description: Generate CRUD action names for a given entity name
license: MIT
metadata:
  version: "1.0.0"
  author: agno-docs
  tags: ["crud", "entity", "actions", "api"]
---

# Action Finder Skill

Use this skill to generate CRUD action names for a given entity by selecting an appropriate template and intelligently generating action names.

## When to Use

- User asks for actions related to an entity
- User needs to generate API endpoint names
- User wants to discover available operations for an entity
- User is designing a REST API or service interface

## Process

**⚠️ CRITICAL**: You MUST generate camelCase action names (like `createUser`, `listUsers`), NOT template names (like "Create", "Index"). Template names will cause logging to fail.

1. **Load Template Reference**: Use `get_skill_reference('action-finder', 'crud-templates.md')` to load available CRUD templates
2. **Select Template**: Based on the entity type and use case, select the most appropriate template:
   - **CIDED**: For standard entities with full CRUD (Create, Index, Details, Edit, Delete)
   - **CIDRA**: For entities requiring approval workflows (Create, Index, Details, Reject, Approve)
   - **CID**: For readonly entities like logs or audit trails (Create, Index, Details)
3. **Generate Actions**: Intelligently generate action names based on:
   - The selected template's required actions
   - The entity name (considering proper naming conventions, pluralization, etc.)
   - Common naming patterns (camelCase, consistent verb choices)
   - **CRITICAL**: You MUST transform template action names into camelCase function names:
     - "Create" → `create{Entity}` (e.g., `createUser`)
     - "Index" → `list{Entity}s` (plural, e.g., `listUsers`)
     - "Details" → `get{Entity}` (e.g., `getUser`)
     - "Edit" → `edit{Entity}` (e.g., `editUser`)
     - "Delete" → `delete{Entity}` (e.g., `deleteUser`)
     - "Reject" → `reject{Entity}` (e.g., `rejectRequest`)
     - "Approve" → `approve{Entity}` (e.g., `approveRequest`)
   - **DO NOT** pass template names like "Create", "Index", "Details" - these are WRONG
   - **DO** generate camelCase names like `createUser`, `listUsers`, `getUser` - these are CORRECT
   - Examples:
     - CIDED template for "User" → `createUser`, `listUsers`, `getUser`, `editUser`, `deleteUser`
     - CIDRA template for "Request" → `createRequest`, `listRequests`, `getRequest`, `rejectRequest`, `approveRequest`
     - CID template for "Log" → `createLog`, `listLogs`, `getLog`
4. **REQUIRED - Log Operation**: You MUST log the operation using `get_skill_script('action-finder', 'scripts/log.py', execute=True, args=[entity_name, template_selected, action1, action2, ...])`. Pass the entity name, selected template, and all generated camelCase action names as arguments (e.g., `['User', 'CIDED', 'createUser', 'listUsers', 'getUser', 'editUser', 'deleteUser']`).
5. **Return Results**: Format and return the results including:
   - The template_selected (CIDED, CIDRA, or CID)
   - The generated camelCase action names as a markdown unordered list
   - Example format:

     ```
     Template: CIDED

     Actions:
     - createUser
     - listUsers
     - getUser
     - editUser
     - deleteUser
     ```

## Important Notes

- **Do NOT use any script to generate actions**: Generate actions intelligently yourself based on the template and entity context. The only script available is `log.py` for logging operations after you've generated the actions.
- **No find_actions.py script exists**: Do not attempt to call `scripts/find_actions.py` - it does not exist. Generate actions directly.
- **Template Selection**: Consider the entity's purpose when selecting a template (e.g., "Request" entities likely need CIDRA, "Log" entities need CID)
- **Action Naming**: Use consistent naming conventions (camelCase) and appropriate verbs for each action type
- **REQUIRED - Logging**: You MUST log every operation using `get_skill_script('action-finder', 'scripts/log.py', execute=True, args=[entity_name, template_selected, ...actions])`. This is mandatory and must be done before returning results. The log file is stored at `scripts/history.yaml`.

## References

Load the CRUD templates reference to understand available patterns:

- Use `get_skill_reference('action-finder', 'crud-templates.md')` to access template definitions

## Logging (REQUIRED)

**You MUST log every operation before returning results.**

Use the skill script tool to execute the log script with the generated camelCase action names:

```
get_skill_script('action-finder', 'scripts/log.py', execute=True, args=[entity_name, template_selected, action1, action2, ...])
```

**IMPORTANT**: Pass the actual generated camelCase action names, NOT template action names.

Correct Example:

```
get_skill_script('action-finder', 'scripts/log.py', execute=True, args=['User', 'CIDED', 'createUser', 'listUsers', 'getUser', 'editUser', 'deleteUser'])
```

Wrong Example (DO NOT DO THIS):

```
get_skill_script('action-finder', 'scripts/log.py', execute=True, args=['User', 'CIDED', 'Create', 'Index', 'Details', 'Edit', 'Delete'])
```

The log file is stored at `skills/examples/skills/action-finder/scripts/history.yaml` and contains all operation histories with:

- datetime: ISO format timestamp
- entity_name: Name of the entity
- template_selected: Template used (CIDED, CIDRA, or CID)
- actions_found: List of generated action names
- actions_count: Number of actions generated
