from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session

from crud import SessionCrud
from crud.schemas import ActorSessionSchema
from db import schemas
from db.crud import actor as actor_crud
from db.session import get_db

# define router
router = APIRouter(
    tags=["ActivityPub関連"]
)


@router.post("/", description="Actor作成")
def create(
        response: Response,
        data: schemas.ActorCreate,
        db: Session = Depends(get_db)
) -> schemas.ActorPublic | schemas.ErrorResponse:
    actor = actor_crud.get_by_name(db, data.name)
    if actor is not None:
        response.status_code = 409
        return schemas.ErrorResponse(message="Name already exists")

    actor = actor_crud.create(db, data)

    with SessionCrud() as session_crud:
        session_crud.create(response, ActorSessionSchema(actor_id=actor.id))

    return actor


@router.get("/", description="ログイン中Actor取得")
async def get(
        request: Request,
        db: Session = Depends(get_db)
) -> schemas.ActorPublic | None:
    with SessionCrud() as session_crud:
        session: ActorSessionSchema = session_crud.get(request)
    if session is None:
        return None

    return actor_crud.get(db, session.actor_id)
