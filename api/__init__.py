from fastapi import APIRouter

from .auth import router as auth_router
from .post import router as post_router
from .user import router as user_router

router = APIRouter(prefix='/api')
router.include_router(user_router)
router.include_router(post_router)
router.include_router(auth_router)
