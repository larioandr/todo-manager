from fastapi import APIRouter

from ..dependencies import CurrentUserDep
from .. import schemas


router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def user_details(user_id: int):
    pass


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    pass


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        user_id: int, update: schemas.UserUpdate, curr_user: CurrentUserDep):
    pass


@router.put("/", response_model=schemas.User)
def update_current_user(update: schemas.User, curr_user: CurrentUserDep):
    pass


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, curr_user: CurrentUserDep):
    pass


@router.delete("/", response_model=schemas.User)
def delete_current_user(curr_user: CurrentUserDep):
    pass
