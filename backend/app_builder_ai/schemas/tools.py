from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class FileRole(str, Enum):
    frontend = "frontend"
    backend = "backend"
    test = "test"
    docs = "docs"
    config = "config"


class ToolName(str, Enum):
    create_file = "create_file"
    write_file = "write_file"
    create_api_route = "create_api_route"
    create_frontend_component = "create_frontend_component"
    create_test = "create_test"


class CreateFileArgs(BaseModel):
    path: str = Field(..., min_length=3, examples=["backend/app/main.py"])
    role: FileRole
    purpose: str = Field(..., min_length=8)


class WriteFileArgs(BaseModel):
    path: str = Field(..., min_length=3)
    content: str = Field(..., min_length=1)
    overwrite: bool = True


class CreateApiRouteArgs(BaseModel):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    path: str = Field(..., pattern=r"^/")
    handler_name: str = Field(..., min_length=3)
    description: str


class CreateFrontendComponentArgs(BaseModel):
    name: str = Field(..., pattern=r"^[A-Z][A-Za-z0-9]+$")
    route: str = Field(..., pattern=r"^/")
    state_requirements: list[str] = Field(default_factory=list)


class CreateTestArgs(BaseModel):
    path: str
    target: str
    scenario: str


class ToolCall(BaseModel):
    name: ToolName
    args: CreateFileArgs | WriteFileArgs | CreateApiRouteArgs | CreateFrontendComponentArgs | CreateTestArgs

    def summary(self) -> str:
        return f"{self.name.value}: {self.args.model_dump()}"
