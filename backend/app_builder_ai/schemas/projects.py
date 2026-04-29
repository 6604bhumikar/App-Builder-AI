from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app_builder_ai.schemas.tools import ToolCall


class GenerateProjectRequest(BaseModel):
    prompt: str = Field(..., min_length=20, max_length=4000)
    target_stack: Literal["react-fastapi", "nextjs-fastapi", "mern", "python-cli"] = "react-fastapi"
    include_tests: bool = True
    include_docker: bool = True


class Blueprint(BaseModel):
    name: str
    summary: str
    personas: list[str]
    core_features: list[str]
    architecture: list[str]
    risks: list[str]


class GeneratedFile(BaseModel):
    path: str
    role: str
    content: str


class ReviewReport(BaseModel):
    score: int = Field(..., ge=0, le=100)
    checks: list[str]
    recommendations: list[str]


class GeneratedProject(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    prompt: str
    target_stack: str
    blueprint: Blueprint
    tool_calls: list[ToolCall]
    files: list[GeneratedFile]
    review: ReviewReport
