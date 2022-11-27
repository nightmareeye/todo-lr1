"""Todo models
"""
from enum import Enum

from sqlalchemy import Column, Integer, Boolean, Text

from database import Base


class Tag(str, Enum):
    """Todo enum tags
    """
    STUDY = "Учеба"
    PERSONAL = "Личное"
    FUTURE = "Планы"


class Todo(Base):
    """Todo model
    """
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    details = Column(Text)
    completed = Column(Boolean, default=False)
    tag = Column(Text, default="")

    def __repr__(self):
        return f'<Todo {self.id}>'
    def __len__(self):
        return f'<Todo\'s size {len(self.title)}>'
