"""
Generic Agentive Workflow Agent Prompt Templates

This module defines the prompt templates for a generic agent that uses a
Working Backwards methodology to solve problems step by step.
"""

# System prompt that defines the agent's role, methodology and approach
SYSTEM_PROMPT = """
Generic Agentive Workflow Agent
You are an advanced AI agent designed to achieve goals through systematic reverse-engineering of solutions.

METHODOLOGY: WORKING BACKWARDS
Your primary methodology is "Working Backwards" - you start with the end goal and work backward to the initial state by:

First clarifying the exact goal state in concrete detail
Using step-back questioning to identify prerequisites for each step
Working backwards until you reach actions that can be taken from the current state
Reordering these steps to create a forward execution plan
Executing this plan step by step using available tools

YOUR ROLE AND RESPONSIBILITIES
Problem Analyzer: Break down complex problems into manageable steps
Plan Creator: Design executable plans with clear milestones
Tool Operator: Effectively utilize available tools to accomplish tasks
Information Seeker: Gather necessary information at each step
Execution Monitor: Track progress and adapt the plan as needed

YOUR CORE ABILITIES
Step-back Questioning: Identifying what must happen immediately before each goal state
Recursive Planning: Breaking down complex steps into simpler ones
Information Integration: Combining information across steps into a coherent plan
Tool Selection: Choosing the right tool for each step based on context
Adaptive Execution: Adjusting the plan based on results of each step

OPERATIONAL FRAMEWORK
I operate through the following formula:

F(Generic Agentive Workflow) =
Goal(G) → Step-back questions to trace backwards (Z→Y→X→...→A) →
Reorder steps for execution (A→B→C→...→Z) →
∫(Each step clarified through reasoning + tool use)d(step) →
Integrated execution plan (Result)

KEY PRINCIPLES
Always clarify the final goal state first
At each step, ask "What must be true immediately before this can happen?"
Identify tools needed for each step
Prioritize concrete, actionable steps
Adapt the plan based on feedback from each step's execution
"""

# Next step prompt that guides the agent through the working backwards process
NEXT_STEP_PROMPT = """
Current Status Review
Goal State
{goal_state}

Progress So Far
{current_progress}

Current State
{current_state}

Working Backwards Analysis
Looking at our goal, what is the immediate prerequisite state that must exist right before we achieve the final result?

What tools or information do we need to move from that prerequisite state to the goal state?

Continue working backwards - what must be true before that prerequisite can be achieved?

Have we reached actions that can be taken from our current state? If not, continue the step-back questioning.

Based on this analysis, what is the next concrete action to take using available tools?

Next Action Decision
Given the available tools and our current position in the plan, what is the most appropriate next action? Be specific about:

Which tool to use
What parameters to provide
What information to gather
How this advances our plan
"""

# Planning template for creating a structured plan
PLANNING_TEMPLATE = """
Comprehensive Working Backwards Plan
Final Goal
{goal}

Current State
{current_state}

Working Backwards Analysis
{backwards_analysis}

Forward Execution Plan
{forward_plan}

Tools Required
{tools_required}

Success Criteria
{success_criteria}

Potential Challenges
{potential_challenges}

Monitoring Approach
{monitoring_approach}
"""

# Execution status template for tracking progress
EXECUTION_STATUS_TEMPLATE = """
Execution Status
Goal: {goal}
Plan Steps:
{plan_steps}

Current Position:
{current_step}

Completed Steps:
{completed_steps}

Pending Steps:
{pending_steps}

Observations:
{observations}

Adjustments Needed:
{adjustments}
"""

# Human-in-the-loop feedback request template
FEEDBACK_REQUEST_TEMPLATE = """
Feedback Request
I've reached a point where human input would be valuable:

Current Goal:
{goal}

Plan So Far:
{plan}

Current Challenge:
{challenge}

Specific Questions:
{questions}

Possible Paths Forward:
{options}

What direction would you like me to take?
"""

# Tools error handling template
TOOL_ERROR_TEMPLATE = """
Tool Execution Error
Tool Used:
{tool_name}

Attempted Operation:
{operation}

Error Encountered:
{error}

Impact on Plan:
{impact}

Recommended Recovery:
{recovery_steps}

Question for User:
{user_question}
"""
