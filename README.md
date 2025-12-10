**Mini Agent Workflow Engine – FastAPI Implementation**

This project implements an extensible workflow engine (mini-agent system) using FastAPI.
The engine allows dynamic creation of workflows, execution of node-based graphs, state management, and inspection of run logs.
Additionally, the project includes a sample intelligent workflow: Code Review Mini-Agent.

**Project Overview**

The goal of the assignment is to build:

-A workflow engine that can:

   -Define nodes and edges

   -Execute workflows step-by-step

   -Pass shared state between nodes

   -Support branching and looping

-A tool registry to store tool functions
-A graph engine to run workflows
-A working FastAPI backend exposing the required API endpoints

-A sample intelligent workflow (Code Review Agent)

-Clean, readable, and modular code

This repository includes:

-app/engine.py → Workflow engine

-app/tools.py → Tool registry + example tools

-app/workflows.py → Node definitions + Code Review workflow

-app/main.py → FastAPI endpoints and graph initialization

**Project Structure**

TRENDENCE_ASSIGNMENT/
│
├── app/

│   ├── __init__.py

│   ├── engine.py   

│   ├── tools.py

│   ├── workflows.py       

│   └── main.py            
│
├── .gitignore

└── README.md

**System Architecture**
1. Tool Registry
A centralized registry that stores reusable functions ("tools") which nodes can call.

Example tools implemented:

-Function extraction from code

-Code complexity estimation

-Issue detection (debug prints, TODO comments)

-Suggestions generator

-Code quality evaluator

2. Workflow Engine
The core engine is responsible for:

-Validating graph definitions

-Executing node functions in order

-Maintaining and updating state

-Logging step-wise execution

-Supporting branching through next_node

-Supporting loops based on node outputs

-Storing past runs for later inspection

3. Nodes
Each node:

-Accepts state

-Uses tools from the registry

-Returns updated state

-Can optionally specify next_node → enables branching & looping

4. Sample Workflow – Code Review Mini-Agent
The workflow steps:

-extract_functions

-check_complexity

-detect_issues

-suggest_improvements

-evaluate_quality

   -If quality_score < threshold, loop back to suggest_improvements
   -Else stop
This simulates an automated iterative code review system.

 **API Endpoints (FastAPI)**
1️⃣ Create Graph
POST /graph/create
Creates a workflow graph dynamically.

Body:

{
  "nodes": { "node_name": "function_name", ... },
  "edges": { "node_name": "next_node", ... },
  "start_node": "extract_functions"
}

2️⃣ Run Graph
POST /graph/run
Executes the workflow from start to finish.

3️⃣ Get Run State
GET /graph/state/{run_id}
Returns the final state and complete execution log of a previous run.

**Running the Project**
1. Create environment
python -m venv .venv

2. Activate environment
.venv\Scripts\activate

3. Install dependencies
pip install fastapi uvicorn pydantic

4. Run FastAPI
uvicorn app.main:app --reload

5. Open Swagger UI
http://127.0.0.1:8000/docs


Use this to:
-Create a graph
-Run the graph
-Inspect run state

**Example Workflow Execution**

Create Graph

Use /graph/create with the predefined workflow JSON.

Run Graph

Use /graph/run with:

{
  "graph_id": "<your_graph_id>",
  "initial_state": {
    "code": "def foo():\n  print('debug')\n# TODO: fix\n",
    "quality_threshold": 0.8
  }
}

Output includes:

-Extracted functions

-Issues detected

-Suggestions

-Quality score

-Step-by-step log
