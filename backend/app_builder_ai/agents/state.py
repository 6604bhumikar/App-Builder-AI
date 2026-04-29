from typing import TypedDict

from app_builder_ai.schemas.projects import (
    Blueprint,
    GeneratedFile,
    GenerateProjectRequest,
    ReviewReport,
    WorkflowStep,
)
from app_builder_ai.schemas.tools import ToolCall


class BuilderState(TypedDict, total=False):
    request: GenerateProjectRequest
    brief: str
    blueprint: Blueprint
    tool_calls: list[ToolCall]
    files: list[GeneratedFile]
    review: ReviewReport
    workflow_trace: list[WorkflowStep]
