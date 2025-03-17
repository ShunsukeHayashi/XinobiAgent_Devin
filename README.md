# XinobiAgent with Working Backwards Methodology

This project implements a generic agent framework that uses a "Working Backwards" methodology to solve problems step by step.

## Concept

The Working Backwards methodology is defined as:

1. Start with the end goal clearly defined
2. Use step-back questioning to identify prerequisites for each step
3. Work backwards until reaching actions that can be taken from the initial state
4. Reorder steps for forward execution (A→B→C→...→Z)
5. Execute each step with continuous feedback and adaptation

This can be expressed as:

```
F(Generic Agentive Workflow) = 
  Goal → Step-back questions (Z→Y→X→...→A) →
  Reordering (A→B→C→...→Z) →
  ∫(Each step with reasoning + tool use)d(step) →
  Integrated execution plan (Result)
```

## Key Components

- **GenericAgent**: Implements the Working Backwards methodology
- **ToolCallAgent**: Base class for agents that use tools
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

## Key Features

- Step-by-step planning from goal to initial state
- Dynamic plan creation and execution
- Tool selection based on task requirements
- Progress tracking and status reporting
- Adaptive execution based on previous steps' results

## Example Run

See `app/examples/generic_agent_example.py` for a complete example of using the GenericAgent.

## Implementation Details

The GenericAgent follows these steps:

1. **Goal Setting**: Define the exact goal state in concrete detail
2. **Backwards Planning**: Use step-back questioning to identify prerequisites
3. **Plan Organization**: Reorder steps from initial state to goal
4. **Execution**: Execute each step using appropriate tools
5. **Monitoring**: Track progress and adapt the plan as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.
