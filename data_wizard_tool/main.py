from .database import engine, Base
import uvicorn

from fastapi import FastAPI, APIRouter
import logging

logger = logging.getLogger('data-wizard-tool')

router = APIRouter()

Base.metadata.create_all(bind=engine)


@router.get("/")
async def get_root():
    return {"message": "Hello, this is your data engineering deployment app!"}


def create_app():
    from data_wizard_tool.routers.v1.google import auth
    app = FastAPI()
    app.include_router(router)
    app.include_router(auth.router, prefix="/auth")
    return app


def start():
    uvicorn.run("data_wizard_tool.main:create_app", host="0.0.0.0",
                port=8000, reload=True, factory=True)
