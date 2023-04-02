from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import get_db
from models.task import Task

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskStatus(str, Enum):
    done = "Done"
    not_done = "Not Done"


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    project_id: int

    class Config:
        orm_mode = True


@tasks_router.post("/", response_model=TaskResponse)
def create_task(title: str,
                description: str,
                status: TaskStatus,
                project_id: int,
                db: Session = Depends(get_db)):
    task_model = Task()
    task_model.title = title
    task_model.description = description
    task_model.status = status
    task_model.project_id = project_id

    db.add(task_model)
    db.commit()

    return get_task_by_id(task_model.id, db)


@tasks_router.get("/", response_model=List[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    all_tasks = db.query(Task).all()
    return all_tasks


@tasks_router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task_model = db.query(Task).filter(Task.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} is not exist"
        )

    return task_model


@tasks_router.get("/{project_id}", response_model=List[TaskResponse])
def get_tasks_by_project_id(project_id: int, db: Session = Depends(get_db)):
    project_tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return project_tasks


@tasks_router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int,
                title: str,
                description: str,
                status: TaskStatus,
                db: Session = Depends(get_db)):
    task_model = db.query(Task).filter(Task.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} is not exist"
        )

    task_model.title = title
    task_model.description = description
    task_model.status = status

    db.add(task_model)
    db.commit()

    return get_task_by_id(task_model.id, db)


@tasks_router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_model = db.query(Task).filter(Task.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} is not exist"
        )

    db.delete(task_model)
    db.commit()
