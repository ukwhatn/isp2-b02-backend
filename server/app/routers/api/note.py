from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session

from crud import SessionCrud
from crud.schemas import ActorSessionSchema
from db import schemas
from db.crud import note as note_crud
from db.session import get_db

# define router
router = APIRouter(
    tags=["Note管理"]
)


@router.post("/", description="Note作成")
def create(
        request: Request,
        data: schemas.NoteBase,
        db: Session = Depends(get_db)
) -> schemas.NotePublic | None:
    with SessionCrud() as session_crud:
        session: ActorSessionSchema = session_crud.get(request)
    if session is None:
        return None

    note_create: schemas.NoteCreate = schemas.NoteCreate(
        actor_id=session.actor_id,
        title=data.title,
        content=data.content
    )
    note = note_crud.create(db, note_create)
    return note


@router.get("/", description="ログイン中ActorのNote一覧取得")
async def get(
        request: Request,
        db: Session = Depends(get_db)
) -> list[schemas.NotePublic] | None:
    with SessionCrud() as session_crud:
        session: ActorSessionSchema = session_crud.get(request)
    if session is None:
        return None

    return note_crud.get_by_actor(db, session.actor_id)


@router.get("/{note_id}", description="ログイン中ActorのNote取得")
async def get(
        request: Request,
        note_id: int,
        db: Session = Depends(get_db)
) -> schemas.NotePublic | None:
    with SessionCrud() as session_crud:
        session: ActorSessionSchema = session_crud.get(request)
    if session is None:
        return None

    return note_crud.get_by_actor_and_id(db, session.actor_id, note_id)
