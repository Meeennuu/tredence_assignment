from typing import Dict, Any
from .tools import tools


def node_extract_functions(state: Dict[str, Any], tool_registry):
    code = state.get("code", "")
    result = tool_registry["extract_functions"](code)
    return {"state": result}


def node_check_complexity(state: Dict[str, Any], tool_registry):
    functions = state.get("functions", [])
    result = tool_registry["check_complexity"](functions)
    return {"state": result}


def node_detect_issues(state: Dict[str, Any], tool_registry):
    code = state.get("code", "")
    result = tool_registry["detect_basic_issues"](code)
    return {"state": result}


def node_suggest_improvements(state: Dict[str, Any], tool_registry):
    result = tool_registry["suggest_improvements"](state)
    return {"state": result}


def node_evaluate_quality(state: Dict[str, Any], tool_registry):
    result = tool_registry["evaluate_quality"](state)
    new_state = result
    threshold = state.get("quality_threshold", 0.8)
    quality = result["quality_score"]

    # Loop: if quality_score < threshold, go back to "suggest_improvements"
    if quality < threshold:
        next_node = "suggest_improvements"
    else:
        next_node = None  # stop

    return {
        "state": new_state,
        "next_node": next_node
    }


NODE_REGISTRY = {
    "node_extract_functions": node_extract_functions,
    "node_check_complexity": node_check_complexity,
    "node_detect_issues": node_detect_issues,
    "node_suggest_improvements": node_suggest_improvements,
    "node_evaluate_quality": node_evaluate_quality,
}
