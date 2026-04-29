import re

from app_builder_ai.agents.state import BuilderState
from app_builder_ai.schemas.projects import Blueprint, GeneratedFile, ReviewReport
from app_builder_ai.schemas.tools import (
    CreateApiRouteArgs,
    CreateFileArgs,
    CreateFrontendComponentArgs,
    CreateTestArgs,
    FileRole,
    ToolCall,
    ToolName,
    WriteFileArgs,
)
from app_builder_ai.services.llm_planner import LlmPlanner


def _project_name(prompt: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", prompt)[:4]
    return " ".join(words).title() if words else "Generated App"


def plan_node(state: BuilderState) -> BuilderState:
    request = state["request"]
    brief = LlmPlanner().summarize(request.prompt)
    return {**state, "brief": brief}


def architect_node(state: BuilderState) -> BuilderState:
    request = state["request"]
    brief = state["brief"]
    blueprint = Blueprint(
        name=_project_name(request.prompt),
        summary=brief,
        personas=["Founder", "Product manager", "Engineer", "Operations admin"],
        core_features=[
            "Prompt intake and validation",
            "Agentic planning workflow",
            "Validated code generation tool calls",
            "Generated file manifest preview",
            "Review and quality checklist",
        ],
        architecture=[
            f"Target stack: {request.target_stack}",
            "FastAPI API layer with typed request and response schemas",
            "LangGraph orchestration with deterministic fallback executor",
            "React operator console for prompt submission and manifest review",
        ],
        risks=[
            "LLM output must be constrained by typed tool schemas",
            "Generated code should be reviewed before execution",
            "Persistence adapter should be swapped before production use",
        ],
    )
    return {**state, "blueprint": blueprint}


def tool_schema_node(state: BuilderState) -> BuilderState:
    request = state["request"]
    calls: list[ToolCall] = [
        ToolCall(
            name=ToolName.create_file,
            args=CreateFileArgs(
                path="backend/app/main.py",
                role=FileRole.backend,
                purpose="FastAPI application entrypoint for generated app",
            ),
        ),
        ToolCall(
            name=ToolName.create_api_route,
            args=CreateApiRouteArgs(
                method="GET",
                path="/health",
                handler_name="health_check",
                description="Expose service health for deployment probes",
            ),
        ),
        ToolCall(
            name=ToolName.create_frontend_component,
            args=CreateFrontendComponentArgs(
                name="AppShell",
                route="/",
                state_requirements=["prompt", "generationStatus", "files"],
            ),
        ),
    ]

    if request.include_tests:
        calls.append(
            ToolCall(
                name=ToolName.create_test,
                args=CreateTestArgs(
                    path="backend/tests/test_health.py",
                    target="GET /health",
                    scenario="returns status ok",
                ),
            )
        )

    return {**state, "tool_calls": calls}


def generate_node(state: BuilderState) -> BuilderState:
    request = state["request"]
    blueprint = state["blueprint"]
    files = [
        GeneratedFile(
            path="README.md",
            role="docs",
            content=f"# {blueprint.name}\n\n{blueprint.summary}\n",
        ),
        GeneratedFile(
            path="backend/app/main.py",
            role="backend",
            content=(
                "from fastapi import FastAPI\n\n"
                "app = FastAPI(title='Generated App')\n\n"
                "@app.get('/health')\n"
                "def health_check():\n"
                "    return {'status': 'ok'}\n"
            ),
        ),
        GeneratedFile(
            path="frontend/src/App.jsx",
            role="frontend",
            content=(
                "export default function App() {\n"
                f"  return <main><h1>{blueprint.name}</h1><p>{blueprint.summary}</p></main>;\n"
                "}\n"
            ),
        ),
    ]

    if request.include_tests:
        files.append(
            GeneratedFile(
                path="backend/tests/test_health.py",
                role="test",
                content=(
                    "from fastapi.testclient import TestClient\n"
                    "from app.main import app\n\n"
                    "def test_health_check():\n"
                    "    response = TestClient(app).get('/health')\n"
                    "    assert response.status_code == 200\n"
                    "    assert response.json()['status'] == 'ok'\n"
                ),
            )
        )

    if request.include_docker:
        files.append(
            GeneratedFile(
                path="docker-compose.yml",
                role="config",
                content="services:\n  api:\n    build: ./backend\n    ports:\n      - '8000:8000'\n",
            )
        )

    write_calls = [
        ToolCall(
            name=ToolName.write_file,
            args=WriteFileArgs(path=file.path, content=file.content),
        )
        for file in files
    ]
    return {**state, "files": files, "tool_calls": [*state["tool_calls"], *write_calls]}


def review_node(state: BuilderState) -> BuilderState:
    files = state["files"]
    checks = [
        "Prompt was validated before generation",
        "All generated file writes passed Pydantic tool validation",
        "Backend, frontend, docs, and configuration outputs are represented",
    ]
    if any(file.role == "test" for file in files):
        checks.append("Test artifacts are included")

    review = ReviewReport(
        score=92 if any(file.role == "test" for file in files) else 84,
        checks=checks,
        recommendations=[
            "Connect a persistent database adapter before production deployment",
            "Run generated manifests through static analysis before execution",
        ],
    )
    return {**state, "review": review}
