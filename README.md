# Generic Agentive Workflow Agent

This project implements a generic agent that uses a "Working Backwards" methodology to solve problems step by step using OpenAI API.

## Concept

The Generic Agentive Workflow is defined as:

```
F(Generic Agentive Workflow) = 
  Agent(OpenAI API [LLM, Roles & Responsibilities, Tools, Abilities]) 
  achieving goals through Working Backwards methodology.
```

Specifically, it uses step-back questioning to decompose thinking from the final goal state back to the initial state.

## Implementation

The agent works as follows:

1. Goal state is clearly defined
2. Step-back questions are used to identify the state immediately before the goal
3. This process continues recursively, working backwards to the initial state
4. The steps are then reordered from initial state to goal (A→B→C→...→Z)
5. Each step is executed using OpenAI API reasoning and appropriate tools

This can be expressed as:

```
F(Generic Agentive Workflow) = 
  Goal → Step-back questions (Z→Y→X→...→A) →
  Reordering (A→B→C→...→Z) →
  ∫(Each step with OpenAI API reasoning + tool use)d(step) →
  Integrated execution plan (Result)
```

## Key Components

- **GenericAgent class**: Implements the Working Backwards methodology
- **Prompt templates**: Guide the agent through the Working Backwards process
- **Tool integration**: Allows the agent to interact with the environment
- **Plan tracking**: Manages both backwards analysis and forward execution

## Usage

```python
from app.agent.generic_agent import GenericAgent
from app.tool import ToolCollection, Bash, GoogleSearch, Terminate

# Create a tool collection
tools = ToolCollection([Bash(), GoogleSearch(), Terminate()])

# Create the generic agent
agent = GenericAgent(
    name="task_solver",
    description="Solves tasks using Working Backwards methodology",
    available_tools=tools
)

# Run the agent with a goal
result = await agent.run("Create a Python script that downloads the latest Bitcoin price")

# Print the result
print(result)
```

## OpenAI API Usage

The implementation uses OpenAI API with:

- **LLM**: For reasoning and planning
- **Roles & Responsibilities**: Defined in system prompts
- **Tools**: For information gathering and environment interaction
- **Abilities**: Encoded in prompts and agent behavior

## Key Features

- Step-by-step planning from goal to initial state
- Dynamic plan creation and execution
- Tool selection based on task requirements
- Progress tracking and status reporting
- Adaptive execution based on previous steps' results

## Example Run

See `app/examples/generic_agent_example.py` for a complete example of using the GenericAgent.
