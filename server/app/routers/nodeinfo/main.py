from fastapi import APIRouter

# define router
router = APIRouter()


# nodeinfo
@router.get("/2.1", description="NodeInfo")
def node_info():
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


