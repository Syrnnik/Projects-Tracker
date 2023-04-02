from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.link_types import LinkTypeResponse
from db import get_db
from models.link import Link

links_router = APIRouter(prefix="/links", tags=["links"])


class LinkResponse(BaseModel):
    id: int
    title: str
    url: str
    link_type_id: int
    project_id: int
    link_type: LinkTypeResponse

    class Config:
        orm_mode = True


@links_router.post("/", response_model=LinkResponse)
def create_link(title: str,
                url: str,
                link_type_id: int,
                project_id: int,
                db: Session = Depends(get_db)):
    link_model = Link()
    link_model.title = title
    link_model.url = url
    link_model.link_type_id = link_type_id
    link_model.project_id = project_id

    db.add(link_model)
    db.commit()

    return get_link_by_id(link_model.id, db)


@links_router.get("/", response_model=List[LinkResponse])
def get_all_links(db: Session = Depends(get_db)):
    all_links = db.query(Link).all()
    return all_links


@links_router.get("/{link_id}", response_model=LinkResponse)
def get_link_by_id(link_id: int, db: Session = Depends(get_db)):
    link_model = db.query(Link).filter(Link.id == link_id).first()

    if link_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Link with ID {link_id} is not exist"
        )

    return link_model


@links_router.get("/{project_id}", response_model=List[LinkResponse])
def get_links_by_project_id(project_id: int, db: Session = Depends(get_db)):
    project_links = db.query(Link).filter(Link.project_id == project_id).all()

    return project_links


@links_router.put("/{link_id}", response_model=LinkResponse)
def update_link(link_id: int,
                title: str,
                url: str,
                link_type_id: int,
                project_id: int,
                db: Session = Depends(get_db)):
    link_model = db.query(Link).filter(Link.id == link_id).first()

    if link_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Link with ID {link_id} is not exist"
        )

    if title:
        link_model.title = title
    if url:
        link_model.url = url
    if link_type_id:
        link_model.link_type_id = link_type_id
    if project_id:
        link_model.project_id = project_id

    db.add(link_model)
    db.commit()

    return get_link_by_id(link_model.id, db)


@links_router.delete("/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db)):
    link_model = db.query(Link).filter(Link.id == link_id).first()

    if link_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Link with ID {link_id} is not exist"
        )

    db.delete(link_model)
    db.commit()
