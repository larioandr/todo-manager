from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


# ---------------------------------------------------------------------------
# Users CRUD
# ---------------------------------------------------------------------------

def read_user(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)


def list_users(
        db: Session, skip: int = 0, limit: int = 100
):
    return db.execute(
        select(models.User)
        .offset(skip)
        .limit(limit)
        .order_by(models.User.id)
    ).scalars().all()


def delete_user(db: Session, user_id: int) -> int:
    user = read_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return 1
    return 0


def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    db_user = models.User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.User) -> models.User:
    db_user = read_user(db, user.id)

    for key, value in user.model_dump(exclude={'id'}).items():
        if value is not None:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(
        db: Session, user_id: int, hashed_password: str) -> models.User | None:
    if (db_user := read_user(db, user_id)) is not None:
        db_user.hashed_password = hashed_password
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


# ---------------------------------------------------------------------------
# Projects CRUD
# ---------------------------------------------------------------------------
def read_project(db: Session, proj_id: int) -> models.Project | None:
    return db.get(models.Project, proj_id)


def list_user_projects(
        db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.execute(
        select(models.Project)
        .where(models.Project.creator_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(models.Project.id)
    ).scalars().all()


def create_project(
        db: Session, user_id: int, data: schemas.ProjectCreate
) -> models.Project:
    db_proj = models.Project(**data.model_dump(), creator_id=user_id)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj


def delete_project(db: Session, proj_id: int) -> int:
    if (db_proj := read_project(db, proj_id)) is not None:
        db.delete(db_proj)
        db.commit()
        return 1
    return 0


def update_project(db: Session, proj: schemas.Project) -> models.Project | None:
    if (db_proj := read_project(db, proj.id)) is not None:
        for key, value in proj.model_dump(exclude={'id'}).items():
            setattr(db_proj, key, value)
        db.commit()
        db.refresh(db_proj)
        return db_proj
    return None


# ---------------------------------------------------------------------------
# TODOs CRUD
# ---------------------------------------------------------------------------
def read_todo(db: Session, todo_id: int) -> models.ToDo | None:
    return db.get(models.ToDo, todo_id)


# TODO: write the rest of CRUD
