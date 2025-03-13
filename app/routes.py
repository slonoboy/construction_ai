from fastapi import APIRouter, Depends, HTTPException

from app.schemas import ProjectCreateBody, ProjectSchema
from app.services import GeminiService, ProjectService


router = APIRouter(prefix="/projects")


@router.post("/")
async def projects_create(
    body: ProjectCreateBody,
    project_service: ProjectService = Depends(ProjectService.get_project_service),
    gemini_service: GeminiService = Depends(GeminiService)
) -> ProjectSchema:
    tasks = await gemini_service.generate_tasks(body.project_name, body.location)
    if not tasks:
        raise HTTPException(status_code=400, detail="Could not generate tasks")

    return await project_service.create_project(
        body.project_name, body.location, tasks
    )


@router.get("/{project_id}")
async def projects_retrieve(
    project_id: int,
    project_service: ProjectService = Depends(ProjectService.get_project_service),
) -> ProjectSchema:
    project = await project_service.retrieve_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project
