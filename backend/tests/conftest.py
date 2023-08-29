import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from ..todos_app.database import Base
from ..todos_app.dependencies import get_db
from ..todos_app.main import app
from ..todos_app import models

DB_URL = "sqlite://"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)


@pytest.fixture()
def session():
    Base.metadata.create_all(engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(empty_session) -> TestClient:
    def override_get_db():
        yield empty_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


SAMPLE_DATA = [
    {
        'id': 1,
        'email': 'ivan@example.com',
        'hashed_password': 'qwerty+salt',
        'first_name': 'Ivan',
        'last_name': 'Petrov',
        'is_admin': True,
        'projects': [
            {
                'id': 1,
                'title': 'Groceries list',
                'description': 'Shopping list for groceries store',
                'todos': [
                    {'id': 1, 'text': 'tomatoes', 'is_done': True},
                    {'id': 2, 'text': 'cabbage', 'is_done': False},
                    {'id': 3, 'text': 'apples', 'is_done': False},
                    {'id': 4, 'text': 'oranges', 'is_done': False},
                ]
            }, {
                'id': 2,
                'title': 'Electronics',
                'description': 'Electronics shopping list',
                'todos': [
                    {'id': 10, 'text': 'iphone', 'is_done': False},
                    {'id': 11, 'text': 'tv', 'is_done': False},
                    {'id': 12, 'text': 'earphones', 'is_done': True},
                ]
            }, {
                'id': 3,
                'title': 'Empty',
                'description': '',
                'todos': []
            }, {
                'id': 4,
                'title': 'Empty2',
                'description': '',
                'todos': []
            }
        ],
    }, {
        'id': 2,
        'email': 'mary@example.com',
        'hashed_password': 'secret+salt',
        'first_name': 'Mary',
        'last_name': 'Ivanova',
        'is_admin': False,
        'projects': [
            {
                'id': 5,
                'title': 'Drawing owl',
                'description': 'How to draw an owl',
                'todos': [
                    {'id': 20, 'text': 'Draw head', 'is_done': True},
                    {'id': 21, 'text': 'Draw body', 'is_done': True},
                    {'id': 22, 'text': 'Draw wings', 'is_done': True},
                    {'id': 23, 'text': 'Draw the owl', 'is_done': True},
                ]
            }
        ],
    }, {
        'id': 3,
        'email': 'kate@example.com',
        'hashed_password': 'secret2+salt',
        'first_name': 'Kate',
        'last_name': '',
        'is_admin': False,
        'projects': []
    }
]


@pytest.fixture()
def sample_session(session: Session):
    for user_dict in SAMPLE_DATA:
        user_data = {
            key: value for key, value in user_dict.items()
            if key not in {'projects'}
        }
        db_user = models.User(**user_data)
        session.add(db_user)
        for proj_dict in user_dict['projects']:
            proj_data = {
                key: value for key, value in proj_dict.items()
                if key not in {'todos'}
            }
            db_proj = models.Project(**proj_data, creator_id=db_user.id)
            session.add(db_proj)
            for todo_dict in proj_dict['todos']:
                db_todo = models.ToDo(
                    **todo_dict, creator_id=db_user.id, project_id=db_proj.id)
                session.add(db_todo)
    session.commit()
    yield session
