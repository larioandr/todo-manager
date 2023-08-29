from pydantic import BaseModel, EmailStr, Field


# ----------------------------------------------------------------------------
# Users
# ----------------------------------------------------------------------------
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_admin: bool = False


class User(UserBase):
    id: int


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    is_admin: bool | None = None


# ----------------------------------------------------------------------------
# Projects
# ----------------------------------------------------------------------------
class ProjectBase(BaseModel):
    title: str = Field(max_length=1024)
    description: str = ""
    created_by: User | None = None


class Project(ProjectBase):
    id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(max_length=1024)
    description: str | None = None


# ----------------------------------------------------------------------------
# ToDos
# ----------------------------------------------------------------------------
class ToDoBase(BaseModel):
    text: str
    done: bool = False
    project: Project | None = None
    created_by: User | None = None


class ToDo(ToDoBase):
    id: int


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(BaseModel):
    text: str | None = None
    done: bool | None = None
