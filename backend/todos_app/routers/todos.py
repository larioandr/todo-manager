from fastapi import APIRouter

from ..dependencies import CurrentUserDep
from .. import schemas

router = APIRouter()


@router.post("/", response_model=schemas.ToDo)
def create_todo(
        proj_id: int,
        todo: schemas.ToDoCreate,
        user: CurrentUserDep):
    pass


@router.get("/{todo_id}", response_model=schemas.ToDo)
def todo_details(todo_id: int, user: CurrentUserDep):
    pass


@router.get("/", response_model=list[schemas.ToDo])
def list_todos(
        *, proj_id: int | None = None, offset: int = 0, skip: int = 100,
        user: CurrentUserDep
):
    pass


@router.put("/{todo_id}", response_model=schemas.ToDo)
def update_todo(todo_id: int, update: schemas.ToDoUpdate, user: CurrentUserDep):
    pass


@router.delete("/{todo_id}", response_model=schemas.ToDo)
def delete_todo(todo_id: int, user: CurrentUserDep):
    pass


@router.post("/{todo_id}/toggle", response_model=schemas.ToDo)
def toggle_done(todo_id: int, user: CurrentUserDep):
    pass


@router.post("/{todo_id}/move", response_model=schemas.ToDo)
def change_todo_project(todo_id: int, proj_id: int, user: CurrentUserDep):
    pass
