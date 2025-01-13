from fastapi import APIRouter, Depends

from app.routes import r_root, r_cat, r_book

router = APIRouter()

router.include_router(r_root.router,                 tags=["Root"])
router.include_router(r_cat.router,  prefix="/cat",  tags=["Category"])
router.include_router(r_book.router, prefix="/book", tags=["Book"])
