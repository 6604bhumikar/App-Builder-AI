from uuid import UUID

from app_builder_ai.schemas.projects import GeneratedProject


class ProjectStore:
    def __init__(self) -> None:
        self._projects: dict[UUID, GeneratedProject] = {}

    def save(self, project: GeneratedProject) -> GeneratedProject:
        self._projects[project.id] = project
        return project

    def list(self) -> list[GeneratedProject]:
        return sorted(self._projects.values(), key=lambda item: item.created_at, reverse=True)

    def get(self, project_id: UUID) -> GeneratedProject | None:
        return self._projects.get(project_id)


project_store = ProjectStore()
