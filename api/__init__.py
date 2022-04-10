from fastapi import APIRouter

from .post import router as post_router
from .user import router as user_router

router = APIRouter()
router.include_router(user_router)
router.include_router(post_router)
