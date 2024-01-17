from fastapi import APIRouter

# define router
router = APIRouter()


# nodeinfo
@router.get("/nodeinfo", description="NodeInfo")
def node_info():
    return {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1",
                "href": "https://b02.isp2.ukwhatn.com/nodeinfo/2.1"
            }
        ]
    }
