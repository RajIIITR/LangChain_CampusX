# AI Agent & Agentic AI - Complete Guide

## Table of Contents
- [Understanding AI Agents vs Agentic AI](#understanding-ai-agents-vs-agentic-ai)
- [Real-Life Example: Trip Planning](#real-life-example-trip-planning)
- [LangChain Agents](#langchain-agents)
- [Implementation Guide](#implementation-guide)
- [Best Practices](#best-practices)

## Understanding AI Agents vs Agentic AI

### AI Agent
An **AI Agent** is a system that can perceive its environment, make decisions, and take actions to achieve specific goals. It follows a predefined workflow or sequence of steps to accomplish tasks.

**Key Characteristics:**
- Goal-oriented behavior
- Sequential task execution
- Uses tools and APIs
- Makes decisions based on context
- Can break down complex tasks into subtasks

### Agentic AI
**Agentic AI** refers to the broader capability of AI systems to act autonomously with a sense of agency - making independent decisions, adapting to new situations, and taking initiative without constant human guidance.

**Key Characteristics:**
- Autonomous decision-making
- Adaptive behavior
- Self-directed problem solving
- Dynamic tool selection
- Continuous learning from feedback

### The Difference
Think of it this way:
- **AI Agent** = The implementation (the actual system you build)
- **Agentic AI** = The capability/quality (how autonomous and intelligent it is)

An AI Agent exhibits Agentic AI when it can independently navigate complex scenarios with minimal human intervention.

---

## Real-Life Example: Trip Planning

Let's use the **CampusX example** of planning a trip from Delhi to Goa to understand how an AI Agent works.

### Scenario: Planning a Delhi to Goa Trip

When you ask: *"Plan a complete trip from Delhi to Goa for 4 days"*

The AI Agent breaks this down into a **sequence of steps**:

#### Step 1: Flight Booking (Delhi → Goa)
```
Agent Action: Search for flights
Tool Used: Flight Booking API
Input: {
  "origin": "Delhi",
  "destination": "Goa",
  "date": "2025-01-15",
  "passengers": 1
}
Output: Flight options with prices and timings
Decision: Select best flight based on price and timing
```

#### Step 2: Hotel Reservation
```
Agent Action: Find and book accommodation
Tool Used: Hotel Booking API
Input: {
  "location": "Goa",
  "check_in": "2025-01-15",
  "check_out": "2025-01-19",
  "guests": 1
}
Output: Hotel recommendations with ratings
Decision: Book hotel near popular beaches
```

#### Step 3: Places to Visit
```
Agent Action: Create itinerary
Tool Used: Tourism Information API + Maps API
Input: {
  "destination": "Goa",
  "duration": "4 days",
  "interests": ["beaches", "culture", "food"]
}
Output: Day-wise itinerary with attractions
Decision: Optimize route for minimal travel time
```

#### Step 4: Return Flight Booking (Goa → Delhi)
```
Agent Action: Book return journey
Tool Used: Flight Booking API
Input: {
  "origin": "Goa",
  "destination": "Delhi",
  "date": "2025-01-19",
  "passengers": 1
}
Output: Return flight confirmation
Decision: Select flight that fits the schedule
```

### The Agent's Workflow

```
User Query
    ↓
Agent receives task
    ↓
Break down into subtasks
    ↓
[Flight Booking] → [Hotel Booking] → [Itinerary Planning] → [Return Flight]
    ↓               ↓                  ↓                       ↓
Use Tools       Use Tools          Use Tools              Use Tools
    ↓               ↓                  ↓                       ↓
Make Decisions  Make Decisions     Make Decisions         Make Decisions
    ↓               ↓                  ↓                       ↓
    └───────────────┴──────────────────┴───────────────────────┘
                            ↓
                    Combine Results
                            ↓
                    Final Trip Plan
```

This demonstrates **Agentic AI** because:
- The agent autonomously decides the sequence of steps
- It adapts based on available options (flight times, hotel availability)
- It makes decisions without asking for approval at each step
- It uses multiple tools in coordination

---

## LangChain Agents

LangChain provides powerful abstractions for building AI Agents. The two main approaches are:

### 1. Agent Types in LangChain

**ReAct Agent (Reasoning + Acting)**
- Most versatile and commonly used
- Combines reasoning with action
- Iteratively thinks and acts

**Other Agent Types:**
- OpenAI Functions Agent
- Structured Chat Agent
- Conversational Agent

### 2. The `create_react_agent` Module

The `create_react_agent` function creates an agent that uses the ReAct (Reasoning and Acting) framework.

#### Basic Structure

```python
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor

# Components needed:
# 1. LLM (Language Model)
# 2. Tools (Functions the agent can use)
# 3. Prompt Template
# 4. Agent Executor (Runs the agent)
```

---

## Implementation Guide

### Core Components

#### 1. Setting Up the LLM

```python
from langchain_openai import ChatOpenAI

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,  # Lower temperature for consistent outputs
    api_key="your-api-key"
)
```

#### 2. Creating Tools

Tools are the functions your agent can use. Each tool must have:
- **name**: Identifier for the tool
- **description**: What the tool does (crucial for agent decision-making)
- **function**: The actual implementation

```python
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field

# Example: Flight Search Tool
def search_flights(query: str) -> str:
    """Search for available flights"""
    # Your flight search logic here
    return f"Found flights for: {query}"

flight_tool = Tool(
    name="FlightSearch",
    func=search_flights,
    description="Useful for searching flights between cities. Input should be origin, destination, and date."
)

# Example: Hotel Booking Tool
def search_hotels(query: str) -> str:
    """Search for available hotels"""
    # Your hotel search logic here
    return f"Found hotels for: {query}"

hotel_tool = Tool(
    name="HotelSearch",
    func=search_hotels,
    description="Useful for finding hotels in a specific location. Input should be location and dates."
)

# Create tools list
tools = [flight_tool, hotel_tool]
```

#### 3. Creating the Prompt Template

The prompt is crucial - it guides how the agent thinks and acts.

```python
from langchain.prompts import PromptTemplate

# ReAct prompt template
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
```

#### 4. Creating the Agent

```python
from langchain.agents import create_react_agent

# Create the agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
```

#### 5. Running the Agent with AgentExecutor

```python
from langchain.agents import AgentExecutor

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Shows reasoning process
    max_iterations=10,  # Prevents infinite loops
    handle_parsing_errors=True  # Graceful error handling
)

# Run the agent
response = agent_executor.invoke({
    "input": "Plan a trip from Delhi to Goa for 4 days"
})

print(response["output"])
```

### Complete Working Example

```python
from langchain.agents import create_react_agent, AgentExecutor, Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# 1. Define Tools
def book_flight(query: str) -> str:
    # Simulated flight booking
    return f"Booked flight: {query}"

def book_hotel(query: str) -> str:
    # Simulated hotel booking
    return f"Booked hotel: {query}"

def create_itinerary(query: str) -> str:
    # Simulated itinerary creation
    return f"Created itinerary: {query}"

tools = [
    Tool(name="BookFlight", func=book_flight, 
         description="Books flights. Input: origin, destination, date"),
    Tool(name="BookHotel", func=book_hotel,
         description="Books hotels. Input: location, check-in, check-out"),
    Tool(name="CreateItinerary", func=create_itinerary,
         description="Creates travel itinerary. Input: destination, days")
]

# 2. Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 3. Create Prompt
prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to these tools:

{tools}

Use this format:
Question: the input question
Thought: think about what to do
Action: tool to use from [{tool_names}]
Action Input: input for the tool
Observation: result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer

Question: {input}
Thought: {agent_scratchpad}
""")

# 4. Create Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# 5. Create Executor
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=15
)

# 6. Run Agent
result = executor.invoke({
    "input": "Plan a complete 4-day trip from Delhi to Goa"
})
```

---

## Crucial Things for LangChain Agents

### 1. Tool Descriptions Are Critical
The agent decides which tool to use based on descriptions. Be specific and clear.

```python
# Bad description
description="Does stuff with flights"

# Good description
description="Searches for available flights between two cities. Input format: 'origin city, destination city, date (YYYY-MM-DD)'. Returns flight options with prices and times."
```

### 2. Prompt Engineering
The prompt template guides the agent's reasoning. Key elements:
- Clear instruction format
- Tool list and usage pattern
- Iteration structure (Thought → Action → Observation)
- Stop conditions

### 3. Error Handling
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,  # Essential
    max_iterations=10,  # Prevent infinite loops
    early_stopping_method="generate"  # Stop if taking too long
)
```

### 4. Memory (Optional but Useful)
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,  # Maintains context
    verbose=True
)
```

### 5. Structured Output (When Needed)
```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class TripPlan(BaseModel):
    flights: list
    hotels: list
    itinerary: dict

parser = PydanticOutputParser(pydantic_object=TripPlan)
```

### 6. Callbacks for Monitoring
```python
from langchain.callbacks import StdOutCallbackHandler

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[StdOutCallbackHandler()],  # Track execution
    verbose=True
)
```

---

## Best Practices

### 1. Start Simple
Begin with 2-3 tools and gradually add more as needed.

### 2. Test Tools Independently
Ensure each tool works correctly before integrating with the agent.

### 3. Set Appropriate Limits
```python
max_iterations=10  # Adjust based on task complexity
timeout=120  # Maximum execution time in seconds
```

### 4. Use Verbose Mode During Development
```python
verbose=True  # See the agent's reasoning process
```

### 5. Handle Edge Cases
```python
try:
    result = agent_executor.invoke({"input": user_query})
except Exception as e:
    print(f"Agent failed: {e}")
    # Fallback logic
```

### 6. Monitor Token Usage
AI agents can consume many tokens with multiple iterations.

### 7. Implement Guardrails
```python
def validate_input(user_input: str) -> bool:
    # Check for malicious inputs
    # Validate format
    return True
```

---

## Key Takeaways

1. **AI Agent** = System that autonomously completes tasks using tools
2. **Agentic AI** = Quality of being autonomous and intelligent
3. **ReAct Pattern** = Reasoning (Thought) + Acting (Action) in loops
4. **Tools** = Functions the agent can use (must have clear descriptions)
5. **Prompt** = Guides the agent's reasoning process
6. **AgentExecutor** = Runs the agent with safety limits

## Further Reading

- [LangChain Documentation](https://python.langchain.com/docs/modules/agents/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Agent Best Practices](https://python.langchain.com/docs/modules/agents/how_to/)

---

**Remember**: The power of AI Agents lies in their ability to break down complex tasks, use appropriate tools, and make decisions autonomously - just like planning that trip from Delhi to Goa!