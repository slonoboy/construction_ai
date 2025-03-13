import json
from typing import Optional, List

from fastapi import Depends
from google import genai
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Project, Task
from app.schemas import ProjectSchema
from app.settings import settings


class GeminiService:
    def __init__(self):
        self.client = GeminiClient(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL,
        )

    async def generate_tasks(self, project_name: str, location: str) -> List[str]:
        prompt = f"""
            I am going to give a project name and a location.
            You need to generate the tasks required to realize the project at the desired location.
            Tasks should be as brief as possible with no more than 10 words.
            You response should be a plain valid json list in the following format: ["task 1", "task 2", ...].
            Do not use markdown, only plan text

            project name: {project_name}
            location: {location}
        """

        try:
            text = await self.client.request(prompt)
            result = json.loads(text)
        except Exception:
            return []

        return result


class GeminiClient:
    def __init__(self, api_key: str, model: str):
        self.model = model
        self.api_key = api_key

        self._client = genai.Client(api_key=api_key)

    async def request(self, text: str, model: Optional[str] = None) -> str:
        model = model or self.model

        response = await self._client.aio.models.generate_content(
            model=model, contents=text,
        )

        return response.text


class ProjectService:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    @classmethod
    def get_project_service(cls, db_session: AsyncSession = Depends(get_db)) -> "ProjectService":
        return cls(db_session)

    async def create_project(self, project_name: str, location: str, tasks: List[str]) -> ProjectSchema:
        async with self.session.begin():
            project = Project(
                name=project_name,
                location=location,
                status="in_progress",
            )

            tasks = [
                Task(project=project, name=task_name, status="pending")
                for task_name in tasks
            ]

            self.session.add_all([project] + tasks)

        await self.session.refresh(project)

        return ProjectSchema.model_validate(project)

    async def retrieve_project(self, project_id: int) -> Optional[ProjectSchema]:
        project = await self.session.get(Project, project_id)

        if not project:
            return None

        return ProjectSchema.model_validate(project)
