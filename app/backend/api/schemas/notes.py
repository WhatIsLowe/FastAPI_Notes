from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NoteCreateSchema(BaseModel):
    title: str
    content: str


class NoteUpdateSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]


class NoteSchema(BaseModel):
    user_id: int
    title: str
    content: str
    updated_at: datetime
    created_at: Optional[datetime]
