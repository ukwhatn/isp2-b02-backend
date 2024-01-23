from fastapi import APIRouter, Request, Response, Depends
import json
from sqlalchemy.orm import Session

from crud import SessionCrud
from crud.schemas import ActorSessionSchema
from db import schemas
from db.crud import actor as actor_crud
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
