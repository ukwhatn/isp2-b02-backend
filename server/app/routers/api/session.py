from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session

from crud.schemas import ActorSessionSchema
from crud.session import SessionCrud
from db import schemas
from db.crud import actor as actor_crud
from db.session import get_db

# define router
router = APIRouter(
    tags=["Actorセッション管理"]
)


@router.post("/", description="Actorログイン")
def login(
        response: Response,
        data: schemas.ActorLogin,
        db: Session = Depends(get_db)
) -> schemas.ActorPublic | schemas.ErrorResponse:
    actor = actor_crud.get_by_name(db, data.name)
    if actor is None:
        response.status_code = 401
        return schemas.ErrorResponse(message="Invalid name or password")

    if not actor_crud.verify_password(actor, data.password):
        response.status_code = 401
        return schemas.ErrorResponse(message="Invalid name or password")

    with SessionCrud() as session_crud:
        session_crud.create(response, ActorSessionSchema(actor_id=actor.id))

    return actor


@router.delete("/", description="Actorログアウト")
async def logout(
        request: Request,
        response: Response
) -> schemas.MessageResponse:
    with SessionCrud() as session_crud:
        session_crud.delete(request, response)
    return schemas.MessageResponse(message="OK")
