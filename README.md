# XinobiAgent_Devin

XinobiAgent_Devin is a framework for building AI agents using the Working Backwards methodology. This project provides a structured approach to developing agents that can solve complex problems by working backwards from the goal to the initial state.

## Key Features

- **Working Backwards Methodology**: Start with the end goal and work backward to the initial state
- **Step-back Questioning**: Identify prerequisites for each step
- **Tool Integration**: Utilize various tools to accomplish tasks
- **Flexible Agent System**: Adapt to different domains and use cases
- **OpenAI API Integration**: Leverage powerful language models for reasoning and planning

## Project Structure

```
XinobiAgent_Devin/
├── app/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── generic_agent.py
│   ├── prompt/
│   │   └── generic_agent.py
│   ├── schema/
│   │   └── message.py
│   ├── tool/
│   │   ├── base.py
│   │   └── collection.py
│   └── examples/
│       └── kindle_unlimited_agent_example.py
└── README.md
```

## GenericAgent

The GenericAgent is the core component of this framework. It implements the Working Backwards methodology to solve problems step by step.

### Working Backwards Methodology

The Working Backwards methodology for agent workflows involves:

1. **Define the Goal State**: Clearly specify the desired outcome in concrete detail
2. **Step-back Questioning**: Identify what must happen immediately before the goal can be achieved
3. **Recursive Planning**: Continue working backwards until reaching the initial state
4. **Forward Execution**: Reorder steps and execute from initial state to goal (A→B→C→...→Z)
5. **Adaptive Execution**: Adjust the plan based on feedback and results

This can be expressed as:

F(Generic Agentive Workflow) = 
  Goal → Step-back questions (Z→Y→X→...→A) →
  Reordering (A→B→C→...→Z) →
  ∫(Each step with OpenAI API reasoning + tool use)d(step) →
  Integrated execution plan (Result)

### Key Components

- **GenericAgent class**: Implements the Working Backwards methodology
- **Prompt templates**: Guide the agent through the Working Backwards process
- **Tool integration**: Allows the agent to interact with the environment
- **Plan tracking**: Manages both backwards analysis and forward execution

### Example Usage

```python
import asyncio
from app.agent.generic_agent import GenericAgent
from app.tool.collection import ToolCollection
from app.tool.base import BaseTool

# Create custom tools
tools = ToolCollection([
    # Add your custom tools here
])

# Create the generic agent
agent = GenericAgent(
    name="my_agent",
    description="Agent for solving problems",
    available_tools=tools
)

# Define the goal
goal = "Implement a marketing campaign for Product X"

# Run the agent
async def main():
    result = await agent.run(goal)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Kindle Unlimited Affiliate Marketing Example

The repository includes an example implementation of a Kindle Unlimited affiliate marketing agent. This example demonstrates how to use the GenericAgent to implement a marketing campaign with specific goals and target audiences.

To run the example:

```bash
python -m app.examples.kindle_unlimited_agent_example
```

The Kindle Unlimited affiliate marketing example:

1. Creates custom tools for blog posts, social media, email campaigns, and analytics
2. Defines a specific goal for the marketing campaign
3. Uses the Working Backwards methodology to plan and execute the campaign
4. Targets specific reader personas (commuters, manga fans, self-improvement enthusiasts)
5. Implements a multi-channel marketing approach
6. Tracks performance against KPIs (page views, open rates, conversion rates)

## Requirements

- Python 3.8+
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)
- Required Python packages (see requirements.txt)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
