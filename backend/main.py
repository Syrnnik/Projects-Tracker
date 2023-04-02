import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.link_types import link_types_router
from api.links import links_router
from api.projects import projects_router
from api.tasks import tasks_router
from data.config import HOST, PORT
from db import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(links_router)
app.include_router(link_types_router)
app.include_router(projects_router)
app.include_router(tasks_router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
