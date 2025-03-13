from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreateBody(BaseModel):
    project_name: str
    location: str


class ProjectSchema(BaseModel):
    id: int
    name: str = Field(..., alias="project_name")
    location: str
    status: str
    tasks: List["TaskSchema"]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TaskSchema(BaseModel):
    name: str
    status: str

    model_config = ConfigDict(from_attributes=True)
