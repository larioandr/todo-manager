from ..todos_app import crud
from ..todos_app import schemas


def test_user_create_and_get(session):
    user_create = schemas.UserCreate(
        first_name="Mary",
        last_name="Ivanova",
        email="mary@example.com",
        hashed_password="secret+hashed_pass",
        is_admin=False
    )

    created_db_user = crud.create_user(session, user_create)
    assert created_db_user.first_name == "Mary"
    assert created_db_user.last_name == "Ivanova"
    assert created_db_user.email == "mary@example.com"
    assert created_db_user.hashed_password == "secret+hashed_pass"
    assert created_db_user.id is not None

    db_user = crud.read_user(session, created_db_user.id)
    assert db_user is created_db_user
