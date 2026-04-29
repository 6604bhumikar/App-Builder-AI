from app_builder_ai.agents.workflow import generate_project
from app_builder_ai.schemas.projects import GenerateProjectRequest


def test_generate_project_returns_valid_manifest() -> None:
    project = generate_project(
        GenerateProjectRequest(
            prompt="Build an agentic SaaS app builder with React, FastAPI, tests, and docs."
        )
    )

    assert project.blueprint.name
    assert project.review.score >= 90
    assert any(file.path == "backend/app/main.py" for file in project.files)
    assert any(call.name.value == "write_file" for call in project.tool_calls)
