from fastapi import APIRouter

from . import session, actor, note, activitypub

# define router
router = APIRouter()

# add routers
router.include_router(
    actor.router,
    prefix="/actor"
)
router.include_router(
    session.router,
    prefix="/session"
)
router.include_router(
    note.router,
    prefix="/note"
)
router.include_router(
    activitypub.router,
    prefix="/activitypub"
)