from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.links import LinkResponse
from api.tasks import TaskResponse
from db import get_db
from models.project import Project

projects_router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectStatus(str, Enum):
    all = "All"
    active = "Active"
    archived = "Archived"
    completed = "Completed"


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    tasks: List[TaskResponse]
    links: List[LinkResponse]

    class Config:
        orm_mode = True


@projects_router.post("/", response_model=ProjectResponse)
def create_project(title: str,
                   description: str,
                   db: Session = Depends(get_db)):
    project_model = Project()
    project_model.title = title
    project_model.description = description if description else ""
    project_model.status = ProjectStatus.active

    db.add(project_model)
    db.commit()

    return get_project_by_id(project_model.id, db)


@projects_router.get("/status/{status}", response_model=List[ProjectResponse])
def get_all_projects(status: ProjectStatus, db: Session = Depends(get_db)):
    if status == ProjectStatus.all:
        projectsList = db.query(Project).all()
    elif status == ProjectStatus.active:
        projectsList = db.query(Project).filter(Project.status == ProjectStatus.active).all()
    elif status == ProjectStatus.archived:
        projectsList = db.query(Project).filter(Project.status == ProjectStatus.archived).all()
    elif status == ProjectStatus.completed:
        projectsList = db.query(Project).filter(Project.status == ProjectStatus.completed).all()
    return projectsList


@projects_router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    project_model = db.query(Project).filter(Project.id == project_id).first()

    if project_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} is not exist"
        )

    return project_model


@projects_router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int,
                   title: str,
                   description: str,
                   #    status: ProjectStatus,
                   db: Session = Depends(get_db)):
    project_model = db.query(Project).filter(Project.id == project_id).first()

    if project_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} is not exist"
        )

    project_model.title = title
    project_model.description = description
    # project_model.status = status

    db.add(project_model)
    db.commit()

    return get_project_by_id(project_model.id, db)


@projects_router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project_model = db.query(Project).filter(Project.id == project_id).first()

    if project_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} is not exist"
        )

    db.delete(project_model)
    db.commit()
