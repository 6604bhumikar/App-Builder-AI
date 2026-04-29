from app_builder_ai.agents.nodes import (
    architect_node,
    generate_node,
    plan_node,
    review_node,
    tool_schema_node,
)
from app_builder_ai.agents.state import BuilderState
from app_builder_ai.schemas.projects import GeneratedProject, GenerateProjectRequest


def _run_sequential(state: BuilderState) -> BuilderState:
    for node in (plan_node, architect_node, tool_schema_node, generate_node, review_node):
        state = node(state)
    return state


def _run_langgraph(state: BuilderState) -> BuilderState:
    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        return _run_sequential(state)

    graph = StateGraph(BuilderState)
    graph.add_node("plan", plan_node)
    graph.add_node("architect", architect_node)
    graph.add_node("tools", tool_schema_node)
    graph.add_node("generate", generate_node)
    graph.add_node("review", review_node)
    graph.set_entry_point("plan")
    graph.add_edge("plan", "architect")
    graph.add_edge("architect", "tools")
    graph.add_edge("tools", "generate")
    graph.add_edge("generate", "review")
    graph.add_edge("review", END)
    return graph.compile().invoke(state)


def generate_project(request: GenerateProjectRequest) -> GeneratedProject:
    final_state = _run_langgraph({"request": request})
    return GeneratedProject(
        prompt=request.prompt,
        target_stack=request.target_stack,
        blueprint=final_state["blueprint"],
        tool_calls=final_state["tool_calls"],
        files=final_state["files"],
        review=final_state["review"],
    )
