# XinobiAgent Prompt Structure Analysis

## Overview

The XinobiAgent prompt structure is designed as a template system using Jinja2 for creating agent prompts. It follows a structured format with specific sections to guide the agent's behavior and execution.

## Key Components

1. **Procedure Section**
   - Contains numbered steps with titles and descriptions
   - Format:
     ```
     {% for step in procedures %}
     {{ loop.index }}. **{{ step.title }}**
        - {{ step.description }}
     {% endfor %}
     ```

2. **Advice & Pointers Section**
   - Lists guidance and best practices for the agent
   - Format:
     ```
     {% for advice in advice_pointers %}
     - {{ advice }}
     {% endfor %}
     ```

3. **Forbidden Actions Section**
   - Lists actions that the agent should not perform
   - Format:
     ```
     {% for forbidden_action in forbidden_actions %}
     - ⚠️ **{{ forbidden_action }}**
     {% endfor %}
     ```

4. **User Intent Interpretation Section**
   - Contains the user's input and interpretation of their intent
   - Format:
     ```
     **User Input:**
     ```
     {{ user_input }}
     ```
     ```

5. **Abstracted Intent Section**
   - Breaks down the user's intent into original and want/need components
   - Format:
     ```
     ### Abstracted Intent
     - Original Intent: {{ original_intent }}
     - Want or Need Intent: {{ want_or_need_intent }}
     ```

6. **Goals Section**
   - Lists the fixed goals for the agent to achieve
   - Format:
     ```
     {% for goal in fixed_goals %}
     - ✅ **{{ goal }}**
     {% endfor %}
     ```

7. **Task Breakdown Section**
   - Lists the tasks needed to achieve the goals
   - Format:
     ```
     {% for task in tasks %}
     - [Task {{ loop.index }}] {{ task }}
     {% endfor %}
     ```

8. **Agent Execution Stack Section**
   - Details the tasks, assigned agents, descriptions, and expected outcomes
   - Format:
     ```
     {% for task in agent_tasks %}
     {{ loop.index }}. Task: **{{ task.name }}**
        - Assigned Agent: {{ task.agent }}
        - Description: {{ task.description }}
        - Expected Outcome: {{ task.outcome }}
     {% endfor %}
     ```

9. **Visual Guidelines Section**
   - Provides examples of valid and invalid formatting
   - Format:
     ```
     ### Invalid Format (NG)
     ```xml
     <thinking>
     ここにコンテキストが挿入されます。
     </thinking>
     ```

     ### Valid Format (OK)
     ```
     ◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢
     ここにコンテキストが挿入されます。
     ◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢
     ```
     ```

10. **Environment & Initialization Check Section**
    - Contains information about the system environment
    - Format:
      ```
      - Operating System: **{{ system_information.operating_system }}**
      - Default Shell: **{{ system_information.default_shell }}**
      - Home Directory: **{{ system_information.home_directory }}**
      - Current Working Directory: **{{ system_information.current_working_directory }}**
      ```

11. **Continuous Execution & Testing Section**
    - Contains information about testing and execution
    - Format:
      ```
      - Unit Testing: {{ testing.unit_testing }}
      - Overall Testing: {{ testing.overall_testing }}
      - Continuous Execution: {{ continuous_execution }}
      ```

12. **Git Usage Section**
    - Provides guidance on Git usage
    - Format:
      ```
      - Commit Message: **AIが実行した内容**
      ```

## Visual Formatting

The XinobiAgent prompt uses special formatting for context blocks:
- Valid format uses `◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢` as delimiters
- Invalid format uses XML-style tags like `<thinking>...</thinking>`

## Intent Analysis Structure

The intent analysis follows a specific structure:
1. `[Input] → [User Intent] → [Intent](...)`
2. `[Input] → [User Intent] → [Want or need Intent](...)`
3. `[Fixed User want intent] = Def Fixed Goal`
4. `Achieve Goal == Need Tasks[Goal]=[Tasks](Task, Task, ...)`
5. `To Do Task Execute need Prompt And (Need Tool) assign Agent`
6. `Agent Task Execute Feed back loop Then Task Complete`
