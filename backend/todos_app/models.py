from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)

    projects = relationship("Project", back_populates="created_by")
    todos = relationship("ToDo", back_populates="created_by")

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r}, " \
               f"first_name={self.first_name!r}, " \
               f"last_name={self.last_name!r}, " \
               f"is_admin={self.is_admin!r})"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1024), nullable=False)
    description = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_by = relationship(User, back_populates="projects")
    todos = relationship("ToDo", back_populates="project")

    def __repr__(self):
        return f"Project(id={self.id!r}, title=\"{self.title!r}\", " \
               f"creator_id={self.creator_id!r})"


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete='CASCADE'),
        nullable=False)
    creator_id = Column(
        Integer,
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=False)

    project = relationship(
        Project, back_populates="todos", passive_deletes=True)
    created_by = relationship(
        User, back_populates='todos', passive_deletes=True)

    def __repr__(self):
        return f"ToDo(id={self.id!r}, text={self.text!r}, " \
               f"is_done={self.is_done!r}, project={self.project_id!r}, " \
               f"creator_id={self.creator_id!r})"
