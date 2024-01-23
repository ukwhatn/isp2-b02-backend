from fastapi import APIRouter, Request, Response, Depends
import json
from sqlalchemy.orm import Session

from crud import SessionCrud
from crud.schemas import ActorSessionSchema
from db import schemas
from db.crud import actor as actor_crud
from db.crud import note as note_crud
from db.session import get_db

from fastapi import APIRouter

# define router
router = APIRouter()


@router.get("/.well-known/nodeinfo", description="well-known/nodeinfo")
def well_known_node_info():
    return {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1",
                "href": "https://b02.isp2.ukwhatn.com/nodeinfo/2.1"
            }
        ]
    }


@router.get("/nodeinfo/2.1", description="nodeinfo/2.1")
def node_info_2_1():
    return {
        "openRegistrations": False,
        "protocols": [
            "activitypub"
        ],
        "software": {
            "name": "ISP2-B02",
            "version": "0.1.0"
        },
        "usage": {
            "users": {
                "total": 2
            }
        },
        "services": {
            "inbound": [],
            "outbound": []
        },
        "metadata": {},
        "version": "2.1"
    }


@router.get("/.well-known/webfinger")
def well_known_webfinger(resource: str):
    # :と@で挟まれた文字列を取得
    user_name = resource.split(":")[1].split("@")[0]

    data = {
        "subject": resource,
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": f"https://b02.isp2.ukwhatn.com/actor/{user_name}"
            }
        ]
    }

    return Response(content=json.dumps(data), media_type="application/jrd+json")


@router.get("/actor/{user_name}")
def actor(user_name: str, db: Session = Depends(get_db)):
    user = actor_crud.get_by_name(db, user_name)
    if user is None:
        return Response(status_code=404)

    data = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1"
        ],
        "id": f"https://b02.isp2.ukwhatn.com/actor/{user.name}",
        "type": "Person",
        "preferredUsername": user.name,
        "inbox": f"https://b02.isp2.ukwhatn.com/actor/{user.name}/inbox",
        "outbox": f"https://b02.isp2.ukwhatn.com/actor/{user.name}/outbox",
        "discoverable": True
    }

    return Response(content=json.dumps(data), media_type="application/activity+json")


@router.get("/actor/{user_name}/outbox")
def actor_outbox(user_name: str, db: Session = Depends(get_db)):
    user = actor_crud.get_by_name(db, user_name)
    if user is None:
        return Response(status_code=404)

    notes: list[schemas.NotePublic] = note_crud.get_by_actor(db, user.id)

    print(type(notes))

    data = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
            {
                "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
                "sensitive": "as:sensitive",
                "Hashtag": "as:Hashtag",
                "quoteUrl": "as:quoteUrl",
                "toot": "http://joinmastodon.org/ns#",
                "Emoji": "toot:Emoji",
                "featured": "toot:featured",
                "discoverable": "toot:discoverable",
                "schema": "http://schema.org#",
                "PropertyValue": "schema:PropertyValue",
                "value": "schema:value",
                "isCat": "misskey:isCat",
                "vcard": "http://www.w3.org/2006/vcard/ns#"
            }
        ],
        "id": "https://misskey.io/users/9bmype3osl/outbox?page=true",
        "partOf": "https://misskey.io/users/9bmype3osl/outbox",
        "type": "OrderedCollectionPage",
        "totalItems": len(notes),
        "orderedItems": [
            {
                "id": f"https://b02.isp2.ukwhatn.com/actor/{user.name}/activity",
                "actor": f"https://b02.isp2.ukwhatn.com/actor/{user.name}",
                "type": "Create",
                "published": note.created_at.isoformat(),
                "object": {
                    "id": f"https://b02.isp2.ukwhatn.com/actor/{user.name}/note/{note.id}",
                    "type": "Note",
                    "attributedTo": f"https://b02.isp2.ukwhatn.com/actor/{user.name}",
                    "content": f"<p><span>{note.content}</span></p>",
                    "source": {
                        "content": note.content,
                        "mediaType": "text/x.misskeymarkdown"
                    },
                    "published": note.created_at.isoformat(),
                    "to": [
                        "https://www.w3.org/ns/activitystreams#Public"
                    ],
                    "cc": [
                        "https://misskey.io/users/9bmype3osl/followers"
                    ],
                    "inReplyTo": None,
                    "attachment": [],
                    "sensitive": False,
                    "tag": []
                },
                "to": [
                    "https://www.w3.org/ns/activitystreams#Public"
                ]
            } for note in notes
        ]
    }

    return Response(content=json.dumps(data), media_type="application/activity+json")
