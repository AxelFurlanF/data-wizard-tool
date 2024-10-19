from data_wizard_tool.models import *
from data_wizard_tool.database import engine, Base, SessionLocal
import uvicorn
from fastapi import FastAPI, APIRouter
import logging

# model imports


router = APIRouter()


def get_logger():
    logger = logging.getLogger('data-wizard-tool')
    return logger


@router.get("/")
async def get_root():
    return {"message": "Hello, this is your data engineering deployment app!"}


def create_db():
    Base.metadata.create_all(bind=engine)


def create_app():
    from data_wizard_tool.controllers.v1.google import auth
    from data_wizard_tool.controllers.v1 import security
    app = FastAPI()
    app.include_router(router)
    app.include_router(auth.router, prefix="/gcp")
    app.include_router(security.router, prefix="/auth")
    return app


def start():
    create_db()
    uvicorn.run("data_wizard_tool.main:create_app", host="0.0.0.0",
                port=8000, reload=True, factory=True)
