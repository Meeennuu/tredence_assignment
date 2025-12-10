from typing import Dict, Callable, Any, List

ToolRegistry = Dict[str, Callable[..., Any]]

tools: ToolRegistry = {}


def register_tool(name: str):
    def decorator(fn: Callable[..., Any]):
        tools[name] = fn
        return fn
    return decorator


@register_tool("extract_functions")
def tool_extract_functions(code: str) -> Dict[str, Any]:
    lines = code.splitlines()
    functions: List[str] = [line.strip() for line in lines if line.strip().startswith("def ")]
    return {
        "functions": functions,
        "function_count": len(functions),
    }


@register_tool("check_complexity")
def tool_check_complexity(functions: list) -> Dict[str, Any]:
    count = len(functions)
    complexity_score = min(1.0, 0.2 + 0.1 * count)
    return {
        "complexity_score": complexity_score
    }


@register_tool("detect_basic_issues")
def tool_detect_basic_issues(code: str) -> Dict[str, Any]:
    issues = []
    if "print(" in code:
        issues.append("Debug print statements detected.")
    if "todo" in code.lower():
        issues.append("TODO comments not resolved.")
    return {
        "issues": issues,
        "issue_count": len(issues),
    }


@register_tool("suggest_improvements")
def tool_suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    suggestions = []
    if state.get("complexity_score", 0) > 0.7:
        suggestions.append("Refactor large functions into smaller ones.")
    if state.get("issue_count", 0) > 0:
        suggestions.append("Resolve all TODOs and remove debug prints.")
    if not suggestions:
        suggestions.append("Code looks clean. Consider adding more tests.")
    return {
        "suggestions": suggestions
    }


@register_tool("evaluate_quality")
def tool_evaluate_quality(state: Dict[str, Any]) -> Dict[str, Any]:
    complexity = state.get("complexity_score", 0.5)
    issues = state.get("issue_count", 0)
    suggestions = state.get("suggestions", [])

    quality_score = max(0.0, 1.0 - complexity - 0.1 * issues)
    if not suggestions:
        quality_score = min(1.0, quality_score + 0.2)

    return {
        "quality_score": round(quality_score, 2)
    }
