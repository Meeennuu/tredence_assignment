from typing import Any, Dict, Callable, List, Optional
from pydantic import BaseModel
from uuid import uuid4


class GraphDefinition(BaseModel):
    id: str
    nodes: Dict[str, str]            # node_name -> function_name
    edges: Dict[str, Optional[str]]  # node_name -> default next_node
    start_node: str


class StepLog(BaseModel):
    node: str
    function: str
    state_snapshot: Dict[str, Any]


class RunRecord(BaseModel):
    id: str
    graph_id: str
    state: Dict[str, Any]
    log: List[StepLog]
    status: str  # "running" | "completed" | "failed"
    error: Optional[str] = None


class WorkflowEngine:
    def __init__(self, tool_registry: Dict[str, Callable], node_registry: Dict[str, Callable]):
        self.tool_registry = tool_registry
        self.node_registry = node_registry
        self.graphs: Dict[str, GraphDefinition] = {}
        self.runs: Dict[str, RunRecord] = {}

    def create_graph(self, nodes: Dict[str, str], edges: Dict[str, Optional[str]], start_node: str) -> str:
        graph_id = str(uuid4())
        graph = GraphDefinition(
            id=graph_id,
            nodes=nodes,
            edges=edges,
            start_node=start_node
        )
        self.graphs[graph_id] = graph
        return graph_id

    def get_graph(self, graph_id: str) -> GraphDefinition:
        return self.graphs[graph_id]

    def get_run(self, run_id: str) -> RunRecord:
        return self.runs[run_id]

    def run_graph(self, graph_id: str, initial_state: Dict[str, Any]) -> RunRecord:
        graph = self.get_graph(graph_id)
        run_id = str(uuid4())
        run = RunRecord(
            id=run_id,
            graph_id=graph_id,
            state=initial_state.copy(),
            log=[],
            status="running",
        )
        self.runs[run_id] = run

        current_node = graph.start_node
        max_steps = 100  # safety guard

        try:
            for _ in range(max_steps):
                if current_node is None:
                    break

                if current_node not in graph.nodes:
                    raise ValueError(f"Unknown node: {current_node}")

                function_name = graph.nodes[current_node]
                node_fn = self.node_registry.get(function_name)
                if node_fn is None:
                    raise ValueError(f"Node function not registered: {function_name}")

                # Call node function
                result = node_fn(run.state, self.tool_registry)

                if result is None:
                    result = {}
                if not isinstance(result, dict):
                    raise ValueError("Node function must return a dict")

                # Update state
                state_update = result.get("state", {})
                if not isinstance(state_update, dict):
                    raise ValueError("result['state'] must be a dict if present")
                run.state.update(state_update)

                # Log step
                run.log.append(
                    StepLog(
                        node=current_node,
                        function=function_name,
                        state_snapshot=run.state.copy(),
                    )
                )

                # Decide next node
                next_node = result.get("next_node")
                if next_node is None:
                    next_node = graph.edges.get(current_node)

                current_node = next_node

            run.status = "completed"
        except Exception as e:
            run.status = "failed"
            run.error = str(e)

        return run
