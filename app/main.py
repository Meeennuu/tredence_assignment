from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from .engine import WorkflowEngine
from .tools import tools
from .workflows import NODE_REGISTRY


app = FastAPI(title="Mini Agent Workflow Engine")

# Initialize engine
engine = WorkflowEngine(tool_registry=tools, node_registry=NODE_REGISTRY)


class GraphCreateRequest(BaseModel):
    nodes: Dict[str, str]            # node_name -> function_name
    edges: Dict[str, Optional[str]]  # node_name -> next_node
    start_node: str


class GraphCreateResponse(BaseModel):
    graph_id: str


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


@app.post("/graph/create", response_model=GraphCreateResponse)
def create_graph(req: GraphCreateRequest):
    graph_id = engine.create_graph(
        nodes=req.nodes,
        edges=req.edges,
        start_node=req.start_node
    )
    return GraphCreateResponse(graph_id=graph_id)


@app.post("/graph/run")
def run_graph(req: GraphRunRequest):
    if req.graph_id not in engine.graphs:
        raise HTTPException(status_code=404, detail="Graph not found")
    run = engine.run_graph(req.graph_id, req.initial_state)
    return {
        "run_id": run.id,
        "status": run.status,
        "final_state": run.state,
        "log": [step.dict() for step in run.log],
        "error": run.error,
    }


@app.get("/graph/state/{run_id}")
def get_run_state(run_id: str):
    if run_id not in engine.runs:
        raise HTTPException(status_code=404, detail="Run not found")
    run = engine.get_run(run_id)
    return {
        "run_id": run.id,
        "status": run.status,
        "state": run.state,
        "log_length": len(run.log),
        "error": run.error,
    }


@app.on_event("startup")
def register_example_workflow():
    """
    Pre-register Code Review Mini-Agent graph:
    extract_functions -> check_complexity -> detect_issues -> suggest_improvements -> evaluate_quality
    evaluate_quality may loop back to suggest_improvements based on quality_score.
    """
    nodes = {
        "extract_functions": "node_extract_functions",
        "check_complexity": "node_check_complexity",
        "detect_issues": "node_detect_issues",
        "suggest_improvements": "node_suggest_improvements",
        "evaluate_quality": "node_evaluate_quality",
    }

    edges = {
        "extract_functions": "check_complexity",
        "check_complexity": "detect_issues",
        "detect_issues": "suggest_improvements",
        "suggest_improvements": "evaluate_quality",
        # evaluate_quality has no default edge; looping handled in node logic
    }

    graph_id = engine.create_graph(
        nodes=nodes,
        edges=edges,
        start_node="extract_functions"
    )
    print("Pre-registered Code Review graph:", graph_id)
