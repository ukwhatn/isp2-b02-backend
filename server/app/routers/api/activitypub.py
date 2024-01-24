from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session

from db import schemas
from db.crud import actor as actor_crud
from db.crud import note as note_crud
from db.session import get_db

# define router
router = APIRouter(
    tags=["ActivityPub関連"]
)

# ここを変更
host = "b02.isp2.ukwhatn.com"


# /api/activitypub/users/{user_name} : get
@router.get("/users/{user_name}", description="[Actor]エンドポイント")
async def get(
        response: Response,
        user_name: str,
        db: Session = Depends(get_db)
):
    # actorを取得
    actor = actor_crud.get_by_name(db, user_name)
    if actor is None:
        response.status_code = 404
        return schemas.ErrorResponse(message="User not found")

    activitypub_actor = {
        "@context": ["https://www.w3.org/ns/activitystreams"],
        "type": "Person",
        "id": f"https://{host}/api/activitypub/users/{actor.name}",
        "inbox": f"https://{host}/api/activitypub/users/{actor.name}/inbox",
        "outbox": f"https://{host}/api/activitypub/users/{actor.name}/outbox",
        "preferredUsername": f"{actor.name}",
        "discoverable": True
    }
    return activitypub_actor


# /api/activitypub/notes/{note_id} : get
@router.get("/notes/{note_id}", description="[Note]エンドポイント")
async def get(
        response: Response,
        note_id: int,
        db: Session = Depends(get_db)
):
    # actorを取得
    note = note_crud.get(db, note_id)
    if note is None:
        response.status_code = 404
        return schemas.ErrorResponse(message="Note not found")

    # ! urlを書き換える
    #   - id
    #   - inbox
    #   - outbox
    activitypub_note = {
        "@context": ["https://www.w3.org/ns/activitystreams"],
        "type": "Note",
        "id": f"https://{host}/api/activitypub/notes/{note.id}",
        "content": note.content,
        "attributedTo": f"https://{host}/actor/{note.actor.name}",
        "published": note.created_at.isoformat(),
    }
    return activitypub_note
