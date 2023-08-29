from sqlalchemy.orm import Session
from ..todos_app import crud
from ..todos_app import schemas


def test_user_create_and_get(session):
    user_create = schemas.UserCreate(
        first_name="Mary",
        last_name="Ivanova",
        email="mary@example.com",
        password="secret",
        is_admin=False
    )

    created_db_user = crud.create_user(
        session, user_create, hashed_password=user_create.password+'+salt')

    assert created_db_user.first_name == "Mary"
    assert created_db_user.last_name == "Ivanova"
    assert created_db_user.email == "mary@example.com"
    assert created_db_user.hashed_password == "secret+salt"
    assert created_db_user.id is not None

    db_user = crud.read_user(session, created_db_user.id)
    assert db_user is created_db_user


def test_list_users(sample_session: Session):
    db = sample_session
    users = crud.list_users(db)
    assert len(users) == 3
    assert users[0].email == 'ivan@example.com'
    assert users[1].email == 'mary@example.com'
    assert users[2].email == 'kate@example.com'

    mary_and_kate = crud.list_users(db, skip=1)
    assert len(mary_and_kate) == 2
    assert mary_and_kate[0].email == 'mary@example.com'
    assert mary_and_kate[1].email == 'kate@example.com'

    only_mary = crud.list_users(db, 1, 1)
    assert len(only_mary) == 1
    assert only_mary[0].email == 'mary@example.com'


def test_list_user_projects(sample_session: Session):
    db = sample_session

    all_ivan_projects = crud.list_user_projects(db, user_id=1)
    assert len(all_ivan_projects) == 4
    assert all_ivan_projects[0].title == 'Groceries list'
    assert all_ivan_projects[1].title == 'Electronics'
    assert all_ivan_projects[2].title == 'Empty'
    assert all_ivan_projects[3].title == 'Empty2'

    some_ivan_projects = crud.list_user_projects(db, user_id=1, skip=1, limit=2)
    assert len(some_ivan_projects) == 2
    assert some_ivan_projects[0].title == 'Electronics'
    assert some_ivan_projects[1].title == 'Empty'

    all_mary_projects = crud.list_user_projects(db, user_id=2)
    assert len(all_mary_projects) == 1
    assert all_mary_projects[0].title == 'Drawing owl'
