from fastapi import APIRouter

from ..dependencies import CurrentUserDep
from .. import schemas


router = APIRouter()


@router.post("/", response_model=schemas.Project)
def create_project(proj: schemas.ProjectCreate, user: CurrentUserDep):
    pass


@router.get("/{proj_id}", response_model=schemas.Project)
def project_details(proj_id: int, user: CurrentUserDep):
    pass


@router.put("/{proj_id}", response_model=schemas.Project)
def update_project(proj_id: int, update: schemas.ProjectUpdate,
                   user: CurrentUserDep):
    pass


@router.delete("/{proj_id}", response_model=schemas.Project)
def delete_project(proj_id: int, user: CurrentUserDep):
    pass


@router.get("/", response_model=list[schemas.Project])
def list_projects(*, skip: int = 0, limit: int = 100, user: CurrentUserDep):
    pass
