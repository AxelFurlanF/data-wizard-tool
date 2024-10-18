# model imports
from .models.user import User

from .database import engine, Base, SessionLocal
import uvicorn

from fastapi import FastAPI, APIRouter
import logging

logger = logging.getLogger('data-wizard-tool')

router = APIRouter()


@router.get("/")
async def get_root():
    return {"message": "Hello, this is your data engineering deployment app!"}


def create_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    existing_user = db.query(User).filter(User.id == 1).first()
    if not existing_user:
        hashed_password = hash("mock_password")  # Hash a mock password
        mock_user = User(
            id=1,
            username="mock_user",
            email="mock_user@example.com",
            hashed_password=hashed_password,
        )
        db.add(mock_user)
        db.commit()
    db.close()


def create_app():
    from data_wizard_tool.routers.v1.google import auth
    app = FastAPI()
    app.include_router(router)
    app.include_router(auth.router, prefix="/auth")
    return app


def start():
    create_db()
    uvicorn.run("data_wizard_tool.main:create_app", host="0.0.0.0",
                port=8000, reload=True, factory=True)
