from sqlalchemy import Column, Integer, String

from db import Base


class LinkType(Base):
    __tablename__ = "link_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    lightIcon = Column(String, nullable=False)
    darkIcon = Column(String, nullable=False)
    color = Column(String, nullable=False)
