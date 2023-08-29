from typing import Annotated
from fastapi import Depends, Header, HTTPException, status

from . import schemas
from . import database


async def get_token(x_token: Annotated[str, Header()]) -> str:
    return x_token


async def get_current_user(token: Annotated[str, Depends(get_token)]):
    if token == "kate@example.com":
        user = schemas.User(
            id=42,
            first_name="Kate",
            last_name="Ivanova",
            email="kate@example.com"
        )
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized"
    )


CurrentUserDep = Annotated[schemas.User, Depends(get_current_user)]


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
