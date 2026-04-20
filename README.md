# CrewAI Practice Projects

A comprehensive practice project demonstrating multiple CrewAI use cases and patterns. This workspace contains five distinct crew implementations showcasing different capabilities of the CrewAI framework.

## 📋 Project Structure

```
crewai/
├── main.py                          # Main entry point
├── pyproject.toml                   # Root project configuration
├── README.md                        # This file
│
├── debate/                          # Debate Crew - Multi-agent debate orchestration
│   ├── pyproject.toml
│   ├── src/debate/
│   │   ├── __init__.py
│   │   ├── main.py                 # Debate crew execution script
│   │   ├── crew.py                 # Crew configuration with agents and tasks
│   │   ├── config/
│   │   │   ├── agents.yaml         # Agent definitions
│   │   │   └── tasks.yaml          # Task definitions
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── custom_tool.py      # Custom tools for debate crew
│   ├── knowledge/                   # Knowledge base for debate
│   ├── output/                      # Debate outputs
│   └── tests/
│
├── stock_picker/                   # Stock Picker Crew - Trending stock research
│   ├── pyproject.toml
│   ├── README.md
│   ├── src/stock_picker/
│   │   ├── __init__.py
│   │   ├── main.py                 # Stock picker execution script
│   │   ├── crew.py                 # Crew configuration with agents and tasks
│   │   ├── config/
│   │   │   ├── agents.yaml         # Agent definitions
│   │   │   └── tasks.yaml          # Task definitions
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── custom_tool.py      # Custom tools for stock picker
│   ├── knowledge/                   # Knowledge base for research
│   ├── output/                      # Stock research outputs
│   └── tests/
│
├── financial_researcher/           # Financial Researcher Crew - Company research & analysis
│   ├── pyproject.toml
│   ├── src/financial_researcher/
│   │   ├── __init__.py
│   │   ├── main.py                 # Financial researcher execution script
│   │   ├── crew.py                 # Crew configuration with agents and tasks
│   │   ├── config/
│   │   │   ├── agents.yaml         # Agent definitions
│   │   │   └── tasks.yaml          # Task definitions
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── custom_tool.py      # Custom tools for financial researcher
│   ├── knowledge/                   # Knowledge base for research
│   ├── output/                      # Financial research outputs
│   └── tests/
│
├── engineering_team/               # Engineering Team Crew - Full-stack development
│   ├── pyproject.toml
│   ├── README.md
│   ├── .env
│   ├── src/engineering_team/
│   │   ├── __init__.py
│   │   ├── main.py                 # Engineering team execution script
│   │   ├── crew.py                 # Crew configuration with agents and tasks
│   │   ├── config/
│   │   │   ├── agents.yaml         # Agent definitions
│   │   │   └── tasks.yaml          # Task definitions
│   │   └── tools/
│   ├── knowledge/                   # Knowledge base for engineering
│   ├── output/                      # Generated code and applications
│   │   ├── accounts.py             # Generated Python module
│   │   ├── app.py                  # Generated Gradio UI application
│   │   └── test_accounts.py        # Generated test file
│   └── tests/
│
└── coder/                          # Coder Crew - Code generation and execution
    ├── pyproject.toml
    ├── .env
    ├── src/coder/
    │   ├── __init__.py
    │   ├── main.py                 # Coder execution script
    │   ├── crew.py                 # Crew configuration with agents and tasks
    │   ├── config/
    │   │   ├── agents.yaml         # Agent definitions
    │   │   └── tasks.yaml          # Task definitions
    │   └── tools/
    ├── knowledge/                   # Knowledge base for coding
    ├── output/                      # Generated code outputs
    └── tests/
```

## 🎯 Project Descriptions

### 1. **Debate Crew** (`debate/`)
A multi-agent debate orchestration system that demonstrates sequential task processing and inter-agent collaboration.

**Purpose:** Simulates a structured debate on a given motion with multiple agents taking different roles.

**Agents:**
- **Debater** - Presents arguments on the motion
- **Judge** - Evaluates both sides and renders a decision

**Tasks:**
- Propose arguments for the motion
- Oppose arguments against the motion
- Judge decides on the best arguments

**Example Motion:** "There needs to be strict laws to regulate LLMs."

**Usage:**
```bash
cd debate
python src/debate/main.py
```

---

### 2. **Stock Picker Crew** (`stock_picker/`)
An AI-powered stock research and recommendation system that identifies trending companies and evaluates their investment potential.

**Purpose:** Discovers trending companies in specific sectors and provides comprehensive investment analysis.

**Agents:**
- **Trending Company Finder** - Identifies companies gaining market attention
- **Financial Researcher** - Conducts deep research on each company

**Workflow:**
1. Find trending companies in the specified sector
2. Research market position, future outlook, and investment potential
3. Generate structured investment recommendations

**Key Features:**
- Structured output with trending companies and research data
- Uses SerperDevTool for real-time market data
- Pydantic models for consistent output format

**Example Input:**
```python
inputs = {
    'sector': 'Pharmaceuticals',
}
```

**Usage:**
```bash
cd stock_picker
python src/stock_picker/main.py
```

**Output Files:**
- `output/best_stock.md` - Top stock recommendation
- `output/trending_companies.json` - List of trending companies
- `output/research_report.json` - Detailed research analysis

---

### 3. **Financial Researcher Crew** (`financial_researcher/`)
A comprehensive financial analysis system that researches and analyzes companies' financial performance and outlook.

**Purpose:** Provides thorough financial research and analysis for specific companies.

**Agents:**
- **Researcher** - Gathers financial data and market information
- **Analyst** - Analyzes findings and generates insights

**Workflow:**
1. Research company financial metrics and market position
2. Analyze the gathered information
3. Generate comprehensive financial analysis report

**Key Features:**
- Uses SerperDevTool for financial data collection
- Sequential task processing for logical workflow
- Structured analysis output

**Example Input:**
```python
inputs = {
    'company': 'Microsoft',
}
```

**Usage:**
```bash
cd financial_researcher
python src/financial_researcher/main.py
```

**Output Files:**
- `output/report.md` - Financial analysis report

---

### 4. **Engineering Team Crew** (`engineering_team/`)
A multi-agent software development team that collaboratively builds complete software systems from requirements to deployment.

**Purpose:** Generates complete, functional software applications with backend logic, frontend UI, and test coverage based on detailed requirements.

**Agents:**
- **Engineering Lead** - Analyzes requirements and creates architecture design
- **Backend Engineer** - Implements backend logic with code execution capability
- **Frontend Engineer** - Creates user interfaces (including Gradio UIs)
- **Test Engineer** - Develops comprehensive test suites

**Workflow:**
1. Parse and analyze software requirements
2. Design system architecture and API contracts
3. Generate backend implementation code
4. Create frontend/UI components
5. Generate and execute test cases
6. Output complete, production-ready code

**Key Features:**
- Code execution capability (safe mode with sandboxing)
- Generates complete Python modules with classes and methods
- Creates functional Gradio UI applications
- Generates unit tests automatically
- Architecture-focused design before implementation
- Multi-agent collaboration with specialized roles

**Example Requirements:**
```
A simple account management system for a trading simulation platform.
The system should allow users to create accounts, deposit and withdraw funds...
```

**Usage:**
```bash
cd engineering_team
python src/engineering_team/main.py
```

**Output Files:**
- `output/accounts.py` - Generated backend module
- `output/app.py` - Generated Gradio UI application
- `output/test_accounts.py` - Generated test file
- `output/accounts.py_design.md` - Design documentation

---

### 5. **Coder Crew** (`coder/`)
An autonomous code generation and execution crew that can write and execute Python programs for specific assignments.

**Purpose:** Takes programming assignments and generates, tests, and executes Python code solutions.

**Agents:**
- **Coder** - Expert Python programmer with code execution capability

**Workflow:**
1. Receive programming assignment
2. Analyze requirements
3. Generate Python solution code
4. Execute code safely in sandbox
5. Validate results
6. Return working solution

**Key Features:**
- Safe code execution mode with timeout protection
- Can handle complex mathematical and algorithmic problems
- Direct code execution feedback
- Automatic error handling and retries
- Perfect for programming challenges and automation tasks

**Example Assignment:**
```
Write a Python program to calculate the first 20 numbers of the series
and multiply the total by 5: 3-5+7-9+11-...
```

**Usage:**
```bash
cd coder
python src/coder/main.py
```

**Output Files:**
- `output/` - Generated code solutions and execution results

---

### Prerequisites
- Python 3.10+
- CrewAI framework
- API keys for LLM and search tools (if needed)

### Installation

1. Clone or navigate to the project directory:
```bash
cd crewai
```

2. Install dependencies for a specific project:
```bash
cd debate
pip install -e .
```

Or install all projects:
```bash
pip install -e debate
pip install -e stock_picker
pip install -e financial_researcher
pip install -e engineering_team
pip install -e coder
```

### Configuration

Each crew project contains YAML configuration files:
- **agents.yaml** - Defines agent roles, goals, and backstories
- **tasks.yaml** - Defines tasks, descriptions, and expected outputs

Edit these files to customize agent behavior and task parameters.

---

## 📝 Common Patterns

### Agent Definition (YAML)
```yaml
agent_name:
  role: "Role Description"
  goal: "Primary goal of the agent"
  backstory: "Background and expertise"
```

### Task Definition (YAML)
```yaml
task_name:
  description: "What the task should do"
  expected_output: "What the output should contain"
  agent: "agent_name"
```

---

## 🛠️ Key Technologies

- **CrewAI** - Multi-agent framework for orchestrating AI agents
- **Pydantic** - Data validation and structured output
- **SerperDevTool** - Web search capability for agents
- **YAML** - Configuration management
- **Python** - Core programming language

---

## 📂 Output & Knowledge

Each project includes:
- **knowledge/** - Domain-specific knowledge files
- **output/** - Generated outputs from crew executions
- **tests/** - Test suites (ready for implementation)

---

## 🔧 Customization Guide

### Adding a New Agent
1. Define the agent in `config/agents.yaml`
2. Add a method decorated with `@agent` in `crew.py`
3. Create corresponding tasks using the agent

### Adding a New Task
1. Define the task in `config/tasks.yaml`
2. Add a method decorated with `@task` in `crew.py`
3. Assign it to an agent in the task configuration

### Adding Tools
1. Create tool implementations in `tools/`
2. Import and pass tools to agent definitions
3. Document tool capabilities in agent backstory

---

## 📚 Learning Outcomes

This practice project demonstrates:
- ✅ Multi-agent orchestration patterns
- ✅ Sequential task processing workflows
- ✅ Agent role specialization
- ✅ Tool integration with agents
- ✅ Structured output formatting
- ✅ Configuration management with YAML
- ✅ Real-world use cases (debate, stock research, financial analysis)
- ✅ **Software development with multi-agent teams** (Engineering Team)
- ✅ **Safe code execution and automation** (Coder)
- ✅ **Gradio UI generation** (Engineering Team)
- ✅ **Dynamic code generation and testing** (Engineering Team, Coder)

---

## 📖 References

- [CrewAI Documentation](https://docs.crewai.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## 📝 Notes

- Each crew project is independently runnable
- Projects can be combined for more complex workflows
- Extend tools and agents as needed for your use cases
- Monitor token usage when using LLM-based agents
