import os
from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import get_db, links_icon_dir, valid_icon_file_types
from models.linkType import LinkType

link_types_router = APIRouter(prefix="/link_types", tags=["link_types"])


class ThemeTypes(str, Enum):
    light = "light"
    dark = "dark"


class LinkTypeResponse(BaseModel):
    id: int
    title: str
    lightIcon: str
    darkIcon: str
    color: str

    class Config:
        orm_mode = True


@link_types_router.post("/", response_model=LinkTypeResponse)
def create_link_type(title: str,
                     color: str,
                     lightIcon: UploadFile,
                     darkIcon: UploadFile = None,
                     db: Session = Depends(get_db)):
    try:
        if lightIcon.content_type in valid_icon_file_types:
            icon_path = os.path.join(links_icon_dir, lightIcon.filename)
            with open(icon_path, 'wb') as f:
                content = lightIcon.file.read()
                f.write(content)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid icon file type {lightIcon.content_type}. Expected one of {', '.join(valid_icon_file_types)}"
            )
    finally:
        lightIcon.file.close()

    if darkIcon:
        try:
            if darkIcon.content_type in valid_icon_file_types:
                icon_path = os.path.join(links_icon_dir, darkIcon.filename)
                with open(icon_path, 'wb') as f:
                    content = darkIcon.file.read()
                    f.write(content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid icon file type {darkIcon.content_type}. Expected one of {', '.join(valid_icon_file_types)}"
                )
        finally:
            darkIcon.file.close()

    link_type_model = LinkType()
    link_type_model.title = title
    link_type_model.lightIcon = lightIcon.filename
    if darkIcon:
        link_type_model.darkIcon = darkIcon.filename
    else:
        link_type_model.darkIcon = lightIcon.filename
    link_type_model.color = color

    db.add(link_type_model)
    db.commit()

    return get_link_type_by_id(link_type_model.id, db)


@link_types_router.get("/", response_model=List[LinkTypeResponse])
def get_all_link_types(db: Session = Depends(get_db)):
    all_link_types = db.query(LinkType).all()
    return all_link_types


@link_types_router.get("/{type_id}", response_model=LinkTypeResponse)
def get_link_type_by_id(type_id: int, db: Session = Depends(get_db)):
    link_type_model = db.query(LinkType).filter(LinkType.id == type_id).first()

    if link_type_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"LinkType with ID {type_id} is not exist"
        )

    return link_type_model


@link_types_router.get("/icon/{type_id}/{icon_theme}", response_class=FileResponse)
def get_icon_file_by_id(type_id: int, icon_theme: ThemeTypes, db: Session = Depends(get_db)):
    link_type_model = db.query(LinkType).filter(LinkType.id == type_id).first()
    icon_name = link_type_model.lightIcon
    if icon_theme == ThemeTypes.dark:
        icon_name = link_type_model.darkIcon
    return os.path.join(links_icon_dir, icon_name)


@link_types_router.put("/{type_id}", response_model=LinkTypeResponse)
def update_link_type(type_id: int,
                     title: str,
                     color: str,
                     lightIcon: UploadFile,
                     darkIcon: UploadFile = None,
                     db: Session = Depends(get_db)):
    link_type_model = db.query(LinkType).filter(LinkType.id == type_id).first()

    if link_type_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"LinkType with ID {type_id} is not exist"
        )

    if lightIcon:
        try:
            if lightIcon.content_type in valid_icon_file_types:
                icon_path = os.path.join(links_icon_dir, lightIcon.filename)
                with open(icon_path, 'wb') as f:
                    content = lightIcon.file.read()
                    f.write(content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid icon file type {lightIcon.content_type}. Expected one of {', '.join(valid_icon_file_types)}"
                )
        finally:
            lightIcon.file.close()

    if darkIcon:
        try:
            if darkIcon.content_type in valid_icon_file_types:
                icon_path = os.path.join(links_icon_dir, darkIcon.filename)
                with open(icon_path, 'wb') as f:
                    content = darkIcon.file.read()
                    f.write(content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid icon file type {darkIcon.content_type}. Expected one of {', '.join(valid_icon_file_types)}"
                )
        finally:
            darkIcon.file.close()

    link_type_model.title = title
    link_type_model.lightIcon = lightIcon.filename
    link_type_model.darkIcon = darkIcon.filename
    if not darkIcon:
        link_type_model.darkIcon = lightIcon.filename
    link_type_model.color = color

    db.add(link_type_model)
    db.commit()

    return get_link_type_by_id(link_type_model.id, db)


@link_types_router.delete("/{type_id}")
def delete_link_type(type_id: int, db: Session = Depends(get_db)):
    link_type_model = db.query(LinkType).filter(LinkType.id == type_id).first()

    if link_type_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"LinkType with ID {type_id} is not exist"
        )

    db.delete(link_type_model)
    db.commit()
