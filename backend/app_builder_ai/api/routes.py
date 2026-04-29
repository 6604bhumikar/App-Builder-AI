from uuid import UUID

from fastapi import APIRouter, HTTPException

from app_builder_ai.agents.workflow import generate_project
from app_builder_ai.schemas.projects import GeneratedProject, GenerateProjectRequest
from app_builder_ai.services.project_store import project_store

router = APIRouter(tags=["projects"])


@router.post("/projects/generate", response_model=GeneratedProject, status_code=201)
def generate(request: GenerateProjectRequest) -> GeneratedProject:
    project = generate_project(request)
    return project_store.save(project)


@router.get("/projects", response_model=list[GeneratedProject])
def list_projects() -> list[GeneratedProject]:
    return project_store.list()


@router.get("/projects/{project_id}", response_model=GeneratedProject)
def get_project(project_id: UUID) -> GeneratedProject:
    project = project_store.get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
