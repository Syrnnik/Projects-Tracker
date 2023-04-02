from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from db import Base
from models.linkType import LinkType
from models.project import Project


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    link_type_id = Column(Integer, ForeignKey(LinkType.id, ondelete='CASCADE'), nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id, ondelete='CASCADE'), nullable=False)

    link_type = relationship(
        "LinkType",
        backref=backref("links", cascade="all,delete"),
    )
