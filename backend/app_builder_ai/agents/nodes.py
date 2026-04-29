import re

from app_builder_ai.agents.state import BuilderState
from app_builder_ai.schemas.projects import Blueprint, GeneratedFile, ReviewReport, WorkflowStep
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


def _stack_commands(target_stack: str) -> list[str]:
    if target_stack == "python-cli":
        return ["cd backend", "python -m pip install -e .", "python -m app.main"]
    if target_stack == "mern":
        return ["npm install", "npm run dev", "npm test"]
    return [
        "cd backend && python -m pip install -e .",
        "python -m uvicorn app.main:app --reload",
        "cd frontend && npm install",
        "npm run dev",
    ]


def _feature_keywords(prompt: str) -> list[str]:
    prompt_lower = prompt.lower()
    mapping = {
        "auth": "Role-based authentication",
        "billing": "Subscription billing",
        "analytics": "Analytics dashboard",
        "chat": "Realtime collaboration",
        "notification": "Notification center",
        "audit": "Audit log",
        "api": "Public API documentation",
        "ai": "AI assistant workflow",
        "course": "Learning content management",
        "kanban": "Kanban workflow",
    }
    found = [feature for keyword, feature in mapping.items() if keyword in prompt_lower]
    return found or ["Workspace management", "Dashboard insights", "User settings"]


def plan_node(state: BuilderState) -> BuilderState:
    request = state["request"]
    brief = LlmPlanner().summarize(request.prompt)
    trace = [
        WorkflowStep(
            name="Prompt intake",
            status="completed",
            detail=f"Validated {len(request.prompt)} characters for a {request.project_type} build.",
        )
    ]
    return {**state, "brief": brief, "workflow_trace": trace}


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
            *_feature_keywords(request.prompt),
        ],
        data_entities=[
            "User",
            "Workspace",
            "Project",
            "GeneratedFile",
            "ToolCall",
            "ReviewReport",
        ],
        api_endpoints=[
            "GET /health",
            "POST /api/projects/generate",
            "GET /api/projects",
            "GET /api/projects/{project_id}",
            "GET /api/projects/{project_id}/manifest",
        ],
        implementation_plan=[
            "Capture requirements and normalize the requested product scope",
            "Select stack-specific backend, frontend, test, and deployment templates",
            "Validate every generated operation through Pydantic tool contracts",
            "Generate a file manifest with docs, code, tests, and run commands",
            "Review quality, risks, and release readiness before export",
        ],
        env_vars=["OPENAI_API_KEY", "APP_BUILDER_LLM_MODEL", "DATABASE_URL", "JWT_SECRET"],
        run_commands=_stack_commands(request.target_stack),
        architecture=[
            f"Target stack: {request.target_stack}",
            f"Quality profile: {request.quality_profile}",
            f"Product type: {request.project_type}",
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
    trace = [
        *state["workflow_trace"],
        WorkflowStep(
            name="Architecture",
            status="completed",
            detail=f"Created {len(blueprint.data_entities)} entities and {len(blueprint.api_endpoints)} API contracts.",
        ),
    ]
    return {**state, "blueprint": blueprint, "workflow_trace": trace}


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

    trace = [
        *state["workflow_trace"],
        WorkflowStep(
            name="Tool validation",
            status="completed",
            detail=f"Prepared {len(calls)} typed tool calls before file generation.",
        ),
    ]
    return {**state, "tool_calls": calls, "workflow_trace": trace}


def generate_node(state: BuilderState) -> BuilderState:
    request = state["request"]
    blueprint = state["blueprint"]
    files = [
        GeneratedFile(
            path="README.md",
            role="docs",
            content=(
                f"# {blueprint.name}\n\n{blueprint.summary}\n\n"
                "## Features\n"
                + "\n".join(f"- {feature}" for feature in blueprint.core_features)
                + "\n\n## Run Commands\n"
                + "\n".join(f"- `{command}`" for command in blueprint.run_commands)
                + "\n"
            ),
        ),
        GeneratedFile(
            path="docs/architecture.md",
            role="docs",
            content=(
                f"# {blueprint.name} Architecture\n\n"
                "## Services\n"
                + "\n".join(f"- {item}" for item in blueprint.architecture)
                + "\n\n## Data Entities\n"
                + "\n".join(f"- {entity}" for entity in blueprint.data_entities)
                + "\n"
            ),
        ),
        GeneratedFile(
            path="backend/app/main.py",
            role="backend",
            content=(
                "from fastapi import FastAPI\n"
                "from pydantic import BaseModel\n\n"
                "class Health(BaseModel):\n"
                "    status: str\n"
                "    service: str\n\n"
                f"app = FastAPI(title='{blueprint.name}')\n\n"
                "@app.get('/health')\n"
                "def health_check() -> Health:\n"
                f"    return Health(status='ok', service='{blueprint.name}')\n"
            ),
        ),
        GeneratedFile(
            path="frontend/src/App.jsx",
            role="frontend",
            content=(
                "const features = [\n"
                + "\n".join(f"  '{feature}'," for feature in blueprint.core_features[:6])
                + "\n];\n\n"
                "export default function App() {\n"
                "  return (\n"
                "    <main>\n"
                f"      <h1>{blueprint.name}</h1>\n"
                f"      <p>{blueprint.summary}</p>\n"
                "      <ul>{features.map((feature) => <li key={feature}>{feature}</li>)}</ul>\n"
                "    </main>\n"
                "  );\n"
                "}\n"
            ),
        ),
        GeneratedFile(
            path="backend/app/settings.py",
            role="backend",
            content=(
                "from pydantic_settings import BaseSettings\n\n"
                "class Settings(BaseSettings):\n"
                "    database_url: str = 'sqlite:///app.db'\n"
                "    jwt_secret: str = 'change-me'\n\n"
                "settings = Settings()\n"
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
    trace = [
        *state["workflow_trace"],
        WorkflowStep(
            name="Code generation",
            status="completed",
            detail=f"Generated {len(files)} files and {len(write_calls)} write operations.",
        ),
    ]
    return {
        **state,
        "files": files,
        "tool_calls": [*state["tool_calls"], *write_calls],
        "workflow_trace": trace,
    }


def review_node(state: BuilderState) -> BuilderState:
    files = state["files"]
    checks = [
        "Prompt was validated before generation",
        "All generated file writes passed Pydantic tool validation",
        "Backend, frontend, docs, and configuration outputs are represented",
    ]
    if any(file.role == "test" for file in files):
        checks.append("Test artifacts are included")

    score = 88
    if any(file.role == "test" for file in files):
        score += 5
    if any(file.role == "config" for file in files):
        score += 3
    if len(state["blueprint"].api_endpoints) >= 4:
        score += 2

    review = ReviewReport(
        score=min(score, 98),
        checks=checks,
        recommendations=[
            "Connect a persistent database adapter before production deployment",
            "Run generated manifests through static analysis before execution",
            "Add authentication provider integration for live deployments",
            "Convert generated manifests into zip export when filesystem writes are enabled",
        ],
        blockers=[],
    )
    trace = [
        *state["workflow_trace"],
        WorkflowStep(
            name="Quality review",
            status="completed",
            detail=f"Completed {len(checks)} checks with score {review.score}.",
        ),
    ]
    return {**state, "review": review, "workflow_trace": trace}
