from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)

    tasks = relationship(
        "Task",
        cascade="all,delete",
        backref="project",
    )
    links = relationship(
        "Link",
        cascade="all,delete",
        backref="project",
    )
