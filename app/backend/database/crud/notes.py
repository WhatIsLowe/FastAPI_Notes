from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import Note
from ...api.schemas.notes import NoteCreateSchema, NoteUpdateSchema


async def get_notes(db: AsyncSession, user_id: int) -> list[Note]:
    result = await db.execute(
        select(Note)
        .where(Note.user_id == user_id)
    )
    return result.scalars().all()


async def get_note(db: AsyncSession, user_id: int, note_id: int) -> Note:
    result = await db.execute(
        select(Note)
        .where(Note.id == note_id, Note.user_id == user_id)
    )
    return result.scalars().first()


async def create_note(db: AsyncSession, user_id: int, note: NoteCreateSchema) -> Note:
    db_note = Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


async def update_note(db: AsyncSession, note: Note, new_note_data: NoteUpdateSchema) -> Note:
    if new_note_data.title is not None:
        note.title = new_note_data.title
    if new_note_data.content is not None:
        note.content = new_note_data.content

    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note: Note) -> None:
    await db.delete(note)
    await db.commit()
