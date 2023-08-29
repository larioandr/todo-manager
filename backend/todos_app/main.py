import uvicorn
from fastapi import FastAPI

from .routers import projects
from .routers import todos
from .routers import users


PREFIX_BASE = "/api/v1/"

app = FastAPI()
app.include_router(users.router, prefix=PREFIX_BASE+"users", tags=["users"])
app.include_router(projects.router, prefix=PREFIX_BASE+"proj",
                   tags=["projects"])
app.include_router(todos.router, prefix=PREFIX_BASE+"todos", tags=["todos"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
