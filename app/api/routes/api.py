from fastapi import APIRouter

from app.api.routes import authentication
from app.api.routes import posts
from app.api.routes import comments

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(posts.router, tags=["posts"], prefix='/posts')
router.include_router(comments.router,
                      tags=["comments"],
                      prefix='/posts/{post_id}/comments'
                      )
